# Kamus Preprocessing

Letakkan file-file kamus custom dari penelitian NB02 di folder ini:

| File | Sumber | Keterangan |
|---|---|---|
| `kamus_alay_mbg.csv` | NB02 penelitian | Kamus slang/alay custom domain MBG (override Nasal) |
| `demoji_code_mbg.csv` | NB02 penelitian | Mapping emoji → frasa Bahasa Indonesia |
| `akun_x_mbg.csv` | NB02 penelitian | Mapping mention akun penting → nama asli |
| `whitelist_hashtag_mbg.csv` | NB02 penelitian | Hashtag MBG yang dipertahankan |
| `colloquial-indonesian-lexicon.csv` | Auto-download | Kamus Nasal (diunduh otomatis saat pertama run) |

## Format kolom CSV

Semua file kamus (kecuali whitelist & Nasal) menggunakan dua kolom:
- `original_term`: kata/frasa asli
- `replacement`: pengganti yang dinormalisasi

File whitelist menggunakan satu kolom: `hashtag`

## Fallback
Jika file custom tidak tersedia, pipeline tetap berjalan
menggunakan kamus Nasal saja. Kamus Nasal diunduh otomatis
dari GitHub (nasalsabila/kamus-alay) saat pertama kali dijalankan.
