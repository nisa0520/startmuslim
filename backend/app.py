import os
import hashlib
import secrets
import smtplib
from datetime import date, datetime, timedelta, timezone
from email.message import EmailMessage
from types import SimpleNamespace
from typing import Literal
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request as UrlRequest, urlopen

import jwt
from google.oauth2 import id_token
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from pwdlib import PasswordHash
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import Base, Note, PasswordResetToken, SessionLocal, User, add_missing_columns, engine

SECRET = os.environ["JWT_SECRET"]
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"
DAYS = 7
hasher = PasswordHash.recommended()

app = FastAPI(title="StartMuslim API")
Base.metadata.create_all(engine)  # tahap awal; ganti dengan Alembic saat skema mulai berubah
add_missing_columns()  # tabel users lama otomatis dapat kolom baru (role, status, dst)


def get_db():
    with SessionLocal() as db:
        yield db


def current_user(token: str | None = Cookie(default=None), db: Session = Depends(get_db)) -> User:
    try:
        uid = int(jwt.decode(token or "", SECRET, algorithms=["HS256"])["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(401, "Silakan masuk terlebih dahulu.")
    user = db.get(User, uid)
    if not user:
        raise HTTPException(401, "Silakan masuk terlebih dahulu.")
    return user


def login_cookie(res: Response, user: User):
    exp = datetime.now(timezone.utc) + timedelta(days=DAYS)
    token = jwt.encode({"sub": str(user.id), "exp": exp}, SECRET, algorithm="HS256")
    res.set_cookie("token", token, httponly=True, samesite="lax", secure=COOKIE_SECURE, max_age=DAYS * 86400, path="/")


def public(u: User):
    return {"id": u.id, "name": u.name, "nickname": u.nickname, "email": u.email,
            "role": u.role, "status": u.status}


class RegisterIn(BaseModel):
    # nama field dari frontend memakai camelCase (digitalTrail, cvName, certName)
    model_config = ConfigDict(populate_by_name=True)

    role: Literal["siswa", "kontributor"] = "siswa"
    name: str = Field(min_length=1, max_length=100)
    nickname: str | None = Field(default=None, max_length=60)
    country: str | None = Field(default=None, max_length=10)
    city: str | None = Field(default=None, max_length=80)
    phone: str | None = Field(default=None, max_length=30)
    birthdate: date | None = None
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    digital_trail: str | None = Field(default=None, alias="digitalTrail", max_length=2000)
    expertise: str | None = Field(default=None, max_length=200)
    cv_name: str | None = Field(default=None, alias="cvName", max_length=255)
    cert_name: str | None = Field(default=None, alias="certName", max_length=255)

    @field_validator("nickname", "country", "city", "phone", "birthdate", "digital_trail",
                     "expertise", "cv_name", "cert_name", mode="before")
    @classmethod
    def kosong_jadi_none(cls, v):
        # form mengirim "" untuk kolom yang tidak diisi
        if isinstance(v, str):
            v = v.strip()
            return v or None
        return v

    @model_validator(mode="after")
    def kontributor_wajib_sertifikat(self):
        if self.role == "kontributor" and not self.cert_name:
            raise ValueError("Sertifikat / bukti riwayat wajib untuk kontributor.")
        return self


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class GoogleLoginIn(BaseModel):
    credential: str = Field(min_length=20, max_length=8192)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str = Field(min_length=20, max_length=200)
    password: str = Field(min_length=8, max_length=128)


class NoteIn(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/auth/register", status_code=201)
def register(body: RegisterIn, res: Response, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(409, "Email sudah terdaftar.")
    user = User(
        name=body.name.strip(),
        email=email,
        password_hash=hasher.hash(body.password),
        role=body.role,
        # sementara semua peran langsung aktif. Nanti kalau kontributor perlu ditinjau admin,
        # ganti jadi: status="pending" if body.role == "kontributor" else "active"
        status="active",
        nickname=body.nickname,
        country=body.country,
        city=body.city,
        phone=body.phone,
        birthdate=body.birthdate,
        digital_trail=body.digital_trail,
        expertise=body.expertise,
        cv_name=body.cv_name,
        cert_name=body.cert_name,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # dua pendaftaran dengan email sama di detik yang sama
        db.rollback()
        raise HTTPException(409, "Email sudah terdaftar.")
    login_cookie(res, user)
    return public(user)


@app.post("/api/auth/login")
def login(body: LoginIn, res: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if not user or not hasher.verify(body.password, user.password_hash):
        raise HTTPException(401, "Email atau password salah.")
    login_cookie(res, user)
    return public(user)


def google_certificate_request(url, method="GET", body=None, headers=None, timeout=10):
    request = UrlRequest(url, data=body, headers=headers or {}, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            return SimpleNamespace(status=response.status, data=response.read())
    except HTTPError as response:
        return SimpleNamespace(status=response.code, data=response.read())


@app.post("/api/auth/google")
def google_login(body: GoogleLoginIn, res: Response, db: Session = Depends(get_db)):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise HTTPException(503, "Google Sign-In belum dikonfigurasi di server.")

    try:
        claims = id_token.verify_oauth2_token(body.credential, google_certificate_request, client_id)
    except (ValueError, Exception) as exc:
        raise HTTPException(401, "Token Google tidak valid atau sudah kedaluwarsa.") from exc

    email = claims.get("email", "").lower()
    if not email or not claims.get("email_verified"):
        raise HTTPException(401, "Akun Google belum memiliki email terverifikasi.")

    user = db.scalar(select(User).where(User.email == email))
    is_new = user is None
    if is_new:
        display_name = (claims.get("name") or email.split("@", 1)[0]).strip()[:100]
        user = User(
            name=display_name,
            nickname=display_name[:60],
            email=email,
            password_hash=hasher.hash(secrets.token_urlsafe(32)),
            role="siswa",
            status="active",
        )
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            user = db.scalar(select(User).where(User.email == email))
            is_new = False
    if not user:
        raise HTTPException(500, "Akun Google gagal diproses.")

    login_cookie(res, user)
    return {"user": public(user), "is_new": is_new}


def send_password_reset_email(email: str, reset_url: str) -> None:
    message = EmailMessage()
    message["Subject"] = "Atur ulang kata sandi StartMuslim"
    message["From"] = os.environ.get("SMTP_FROM", os.environ["SMTP_USER"])
    message["To"] = email
    message.set_content(
        "Kami menerima permintaan untuk mengatur ulang kata sandi akun StartMuslim Anda.\n\n"
        f"Buka tautan ini dalam 30 menit: {reset_url}\n\n"
        "Jika Anda tidak meminta reset kata sandi, abaikan email ini."
    )

    host = os.environ["SMTP_HOST"]
    port = int(os.getenv("SMTP_PORT", "587"))
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=15) as smtp:
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(message)


@app.post("/api/auth/password-reset/request")
def request_password_reset(body: PasswordResetRequest, db: Session = Depends(get_db)):
    debug_mode = os.getenv("PASSWORD_RESET_DEBUG", "false").lower() == "true"
    smtp_configured = all(os.getenv(key) for key in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD"))
    if not debug_mode and not smtp_configured:
        raise HTTPException(503, "Layanan email reset belum dikonfigurasi.")

    result = {"message": "Jika email terdaftar, instruksi reset kata sandi akan dikirim."}
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if not user:
        return result

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None))
        .values(used_at=datetime.now(timezone.utc))
    )
    db.add(PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    ))
    db.commit()

    base_url = os.getenv("APP_BASE_URL", "http://localhost:5173").rstrip("/")
    reset_url = f"{base_url}/reset-password?{urlencode({'token': raw_token})}"
    if debug_mode:
        result["reset_url"] = reset_url
    else:
        try:
            send_password_reset_email(user.email, reset_url)
        except (OSError, smtplib.SMTPException, KeyError, ValueError):
            db.execute(
                update(PasswordResetToken)
                .where(PasswordResetToken.token_hash == token_hash)
                .values(used_at=datetime.now(timezone.utc))
            )
            db.commit()
            raise HTTPException(503, "Email reset gagal dikirim. Coba lagi nanti.")
    return result


@app.post("/api/auth/password-reset/confirm")
def confirm_password_reset(body: PasswordResetConfirm, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(body.token.encode()).hexdigest()
    reset_token = db.scalar(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
        )
    )
    now = datetime.now(timezone.utc)
    if not reset_token or reset_token.expires_at <= now:
        raise HTTPException(400, "Tautan reset tidak valid atau sudah kedaluwarsa.")

    user = db.get(User, reset_token.user_id)
    if not user:
        raise HTTPException(400, "Tautan reset tidak valid atau sudah kedaluwarsa.")
    user.password_hash = hasher.hash(body.password)
    db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None))
        .values(used_at=now)
    )
    db.commit()
    return {"message": "Kata sandi berhasil diubah."}


@app.post("/api/auth/logout", status_code=204)
def logout(res: Response):
    res.delete_cookie("token", path="/")


@app.get("/api/auth/me")
def me(user: User = Depends(current_user)):
    return public(user)


@app.get("/api/notes")
def list_notes(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(Note).where(Note.user_id == user.id).order_by(Note.id.desc()))
    return [{"id": n.id, "text": n.text, "created_at": n.created_at} for n in rows]


@app.post("/api/notes", status_code=201)
def add_note(body: NoteIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    n = Note(user_id=user.id, text=body.text.strip())
    db.add(n)
    db.commit()
    return {"id": n.id, "text": n.text, "created_at": n.created_at}


@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    n = db.get(Note, note_id)
    if not n or n.user_id != user.id:
        raise HTTPException(404, "Catatan tidak ditemukan.")
    db.delete(n)
    db.commit()
