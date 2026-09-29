import os
from datetime import date, datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import Date, DateTime, ForeignKey, String, Text, create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.pool import NullPool

load_dotenv()

url = os.environ["DATABASE_URL"]
if url.startswith(("postgres://", "postgresql://")):  # format dari Neon/Supabase -> driver psycopg 3
    url = "postgresql+psycopg://" + url.split("://", 1)[1]

# Serverless (Vercel): jangan menahan koneksi antar request
engine = create_engine(url, pool_pre_ping=True, **({"poolclass": NullPool} if os.getenv("VERCEL") else {}))
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

    # --- data pendaftaran ---
    # role: "siswa" | "kontributor". status: kontributor "pending" sampai ditinjau admin.
    role: Mapped[str] = mapped_column(String(20), default="siswa", server_default="siswa")
    status: Mapped[str] = mapped_column(String(20), default="active", server_default="active")
    nickname: Mapped[str | None] = mapped_column(String(60))
    country: Mapped[str | None] = mapped_column(String(10))
    city: Mapped[str | None] = mapped_column(String(80))
    phone: Mapped[str | None] = mapped_column(String(30))
    birthdate: Mapped[date | None] = mapped_column(Date)
    # khusus kontributor (file belum di-upload sungguhan: baru nama file yang disimpan)
    digital_trail: Mapped[str | None] = mapped_column(Text)
    expertise: Mapped[str | None] = mapped_column(String(200))
    cv_name: Mapped[str | None] = mapped_column(String(255))
    cert_name: Mapped[str | None] = mapped_column(String(255))


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


def add_missing_columns() -> None:
    """Tambah kolom baru ke tabel `users` yang SUDAH ada (create_all tidak mengubah tabel lama).
    Aman dijalankan berulang. Untuk perubahan skema yang lebih rumit, pindah ke Alembic."""
    existing = {c["name"] for c in inspect(engine).get_columns("users")}
    with engine.begin() as conn:
        for col in User.__table__.columns:
            if col.name in existing:
                continue
            ddl = f"ALTER TABLE users ADD COLUMN {col.name} {col.type.compile(dialect=engine.dialect)}"
            if col.server_default is not None:
                ddl += f" DEFAULT '{col.server_default.arg}'"
            conn.execute(text(ddl))
