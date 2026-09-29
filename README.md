# StartMuslim — fullstack (Vue 3 + Vite / FastAPI + SQLAlchemy 2 / Postgres)

    src/       Frontend Vue 3 + Vite + vue-router  (/, /masuk, /daftar, /dashboard)
    backend/   FastAPI + SQLAlchemy 2.x            (auth cookie httpOnly, catatan per user)
    docker-compose.yml   Postgres + pgAdmin

## Jalankan lokal
    docker compose up -d                       # Postgres :5433, pgAdmin http://localhost:5051

    cd backend
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    uvicorn app:app --reload --port 8001       # API :8001 (docs: /docs)

    # Reset kata sandi lokal menampilkan tautan sekali pakai di halaman (tanpa mengirim email).
    # Untuk pengiriman email sungguhan, isi SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
    # dan SMTP_FROM; lalu set PASSWORD_RESET_DEBUG=false.

    # terminal lain, dari root
    npm install && npm run dev                 # http://localhost:5173  (/api diproxy ke :8001)

## Masuk dengan Google
1. Buat OAuth 2.0 Client ID bertipe **Web application** di Google Cloud Console.
2. Tambahkan `http://localhost:5173` sebagai Authorized JavaScript origin.
3. Isi Client ID yang sama di `.env.local` pada root (`VITE_GOOGLE_CLIENT_ID=...`) dan `backend/.env` (`GOOGLE_CLIENT_ID=...`). Contoh frontend tersedia di `.env.example`.
4. Restart Vite dan Uvicorn. Pengguna baru Google akan dibuat sebagai siswa; untuk login ke domain produksi, tambahkan origin produksi di Google Cloud dan set kedua variabel di environment deployment.

## pgAdmin
Buka http://localhost:5051 (admin@startmuslim.com / admin) → Register Server:
Host `db`, Port 5432 (port di DALAM Docker, bukan 5433 — itu port dari luar), DB/User/Password `startmuslim`. Tabel `users` dan `notes` dibuat otomatis saat API pertama jalan.

## Deploy Vercel (2 project dari 1 repo)
1. Buat Postgres (Neon/Supabase) → salin connection string.
2. Project **backend**: Root Directory `backend`. Env: `DATABASE_URL`, `JWT_SECRET` (acak, 32+ karakter), `COOKIE_SECURE=true`.
3. Project **frontend**: Root Directory `.` (Vite terdeteksi). Ganti `GANTI-NAMA-BACKEND` di `vercel.json` dengan domain backend.
Browser hanya bicara ke domain frontend; `/api/*` diteruskan ke backend, jadi cookie login aman tanpa CORS.

## Catatan
- Tabel dibuat lewat `create_all`. Begitu skema mulai berubah, pindah ke Alembic.
- Bagian landing (`src/views/Landing.vue`, `src/data/content.js`) isinya dari deck.
