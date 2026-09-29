export async function api(path, opts = {}) {
  const res = await fetch('/api' + path, {
    credentials: 'same-origin',
    ...opts,
    headers: { 'Content-Type': 'application/json' },
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  })
  if (res.status === 204) return null
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    let msg = 'Terjadi kesalahan. Coba lagi.'
    if (typeof data.detail === 'string') msg = data.detail
    else if (Array.isArray(data.detail) && data.detail.length) {
      // error validasi FastAPI: sebut kolom yang bermasalah
      const d = data.detail[0]
      const field = d.loc && d.loc[d.loc.length - 1]
      msg = field && field !== 'body' ? `Isian "${field}" belum valid. ${d.msg || ''}`.trim() : 'Isian belum valid. Periksa kembali form Anda.'
    }
    throw new Error(msg)
  }
  return data
}
