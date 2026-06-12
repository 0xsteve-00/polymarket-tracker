# 🐋 Polymarket Whale Tracker v2

Pantau trade gede ("whale") di Polymarket, follow *smart money*, deteksi *spike*
volume, simpan history, dan kirim **alert otomatis ke Telegram/Discord** — 24/7
lewat GitHub Actions, tanpa PC nyala.

> **100% read-only & legit.** Cuma baca data publik dari Polymarket Data API
> (`data-api.polymarket.com`). Gak nyentuh / gak ngubah transaksi siapapun.
> **Bukan jaminan profit — tetap DYOR.**

## ✨ Fitur
1. 🔔 **Alert Telegram/Discord** — notif real-time tiap ada sinyal.
2. ⏰ **Scheduler GitHub Actions** — jalan otomatis tiap 10 menit di cloud, gratis.
3. 🧠 **Filter smart-money** — cuma alert wallet yg PnL & win-rate-nya bagus.
4. 📈 **Deteksi spike/momentum** — alert kalau satu market tiba-tiba rame volume.
5. 💾 **History database (SQLite)** — semua trade kerekam buat analisa/backtest.
6. ⭐ **Watchlist & PnL tracking** — daftar wallet favorit + summary performa.

## 🚀 Quick start
Butuh **Python 3** saja. **Gak perlu install dependency** (pakai library bawaan Python).

```bash
git clone https://github.com/0xsteve-00/polymarket-tracker.git
cd polymarket-tracker

# Scan trade terbaru, flag whale >= $1000
python3 whale_tracker.py scan --min-usd 1000

# Monitor real-time + alert smart-money (kalau env alert di-set)
python3 whale_tracker.py watch --min-usd 5000 --smart --min-pnl 5000 --min-winrate 0.55

# Skor smart-money sebuah wallet
python3 whale_tracker.py score 0xWALLET

# Watchlist
python3 whale_tracker.py watchlist add 0xWALLET --label "OG trader"
python3 whale_tracker.py watchlist pnl
```

## 🔔 Setup alert (Telegram)
1. Chat **@BotFather** di Telegram → `/newbot` → dapet **bot token**.
2. Dapetin **chat id** kamu (chat ke **@userinfobot** atau **@RawDataBot**).
3. Set env var (lokal):
   ```bash
   export TELEGRAM_BOT_TOKEN="123456:ABC..."
   export TELEGRAM_CHAT_ID="123456789"
   ```
   (Discord opsional: bikin webhook di channel → set `DISCORD_WEBHOOK_URL`.)
4. Test: `python3 whale_tracker.py poll --min-usd 2000`

Lihat `.env.example` buat contoh.

## ⏰ Jalan otomatis 24/7 (GitHub Actions)
Workflow udah disiapin di `.github/workflows/tracker.yml` (jalan tiap 10 menit).

Tinggal set **Secrets** di repo (`Settings → Secrets and variables → Actions`):
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `DISCORD_WEBHOOK_URL` *(opsional)*

Selesai — Actions bakal nge-poll Polymarket tiap 10 menit & kirim alert ke kamu.
DB (`tracker.db`) di-cache antar run biar gak dobel alert + bisa deteksi spike.
Bisa juga trigger manual di tab **Actions → Run workflow**.

## 🧠 Cara kerja filter
- **whale**: `--min-usd` → trade dgn nilai USD (= share × price) di atas threshold.
- **smart**: `--smart` + `--min-pnl`/`--min-winrate`/`--min-closed` → hanya wallet
  yg realized PnL & win-rate historisnya lolos. Skor di-cache di DB (hemat API).
- **watchlist**: tiap wallet di watchlist selalu di-alert apapun ukurannya.
- **spike**: `--spike-usd` + `--spike-window` (menit) → 1 alert per market kalau
  total volume window-nya nembus threshold. Dedup per window, gak spam.

## 🗂️ Struktur
```
whale_tracker.py     # CLI utama (scan/watch/poll/wallet/leaderboard/score/watchlist)
polymarket_api.py    # client read-only Polymarket Data API
db.py                # SQLite (trades, alerts, scores, watchlist)
notifier.py          # Telegram + Discord
smartmoney.py        # scoring wallet (PnL & win-rate)
.github/workflows/tracker.yml   # scheduler
```

## ⚠️ Disclaimer
Tool ini cuma buat riset & informasi. Trading prediction market berisiko —
keputusan & risikonya tanggung jawab kamu sendiri. Whale gede masuk = sinyal
sentimen, **bukan** jaminan menang.
