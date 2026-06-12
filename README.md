# 🐋 Polymarket Whale Tracker v2

Track large ("whale") trades on Polymarket, follow *smart money*, detect volume
*spikes*, store trade history, and get **automatic alerts on Telegram/Discord** —
running 24/7 via GitHub Actions, no PC required.

> **100% read-only & legit.** This tool only reads public data from the
> Polymarket Data API (`data-api.polymarket.com`). It never touches or modifies
> anyone's transactions. **Not financial advice — always DYOR.**

## ✨ Features
1. 🔔 **Telegram/Discord alerts** — real-time notifications for every signal.
2. ⏰ **GitHub Actions scheduler** — runs automatically every 10 minutes in the cloud, for free.
3. 🧠 **Smart-money filter** — only alert on wallets with strong PnL & win-rate.
4. 📈 **Spike/momentum detection** — alert when a market suddenly heats up in volume.
5. 💾 **History database (SQLite)** — every trade recorded for analysis/backtesting.
6. ⭐ **Watchlist & PnL tracking** — favorite wallets list + performance summary.

## 🚀 Quick start
Requires **Python 3** only. **No dependencies to install** (uses Python's standard library).

```bash
git clone https://github.com/0xsteve-00/polymarket-tracker.git
cd polymarket-tracker

# Scan recent trades, flag whales >= $1000
python3 whale_tracker.py scan --min-usd 1000

# Real-time monitor + smart-money alerts (if alert env vars are set)
python3 whale_tracker.py watch --min-usd 5000 --smart --min-pnl 5000 --min-winrate 0.55

# Smart-money score for a wallet
python3 whale_tracker.py score 0xWALLET

# Watchlist
python3 whale_tracker.py watchlist add 0xWALLET --label "OG trader"
python3 whale_tracker.py watchlist pnl
```

## 🔔 Alert setup (Telegram)
1. Chat with **@BotFather** on Telegram → `/newbot` → get your **bot token**.
2. Get your **chat id** (message **@userinfobot** or **@RawDataBot**).
3. Set env vars (local):
   ```bash
   export TELEGRAM_BOT_TOKEN="123456:ABC..."
   export TELEGRAM_CHAT_ID="123456789"
   ```
   (Discord optional: create a channel webhook → set `DISCORD_WEBHOOK_URL`.)
4. Test it: `python3 whale_tracker.py poll --min-usd 2000`

See `.env.example` for a template.

## ⏰ Run 24/7 (GitHub Actions)
The workflow is ready at `.github/workflows/tracker.yml` (runs every 10 minutes).

Just set **Secrets** in the repo (`Settings → Secrets and variables → Actions`):
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `DISCORD_WEBHOOK_URL` *(optional)*

That's it — Actions will poll Polymarket every 10 minutes and send alerts to you.
The DB (`tracker.db`) is cached between runs to avoid duplicate alerts and to
enable spike detection. You can also trigger it manually from the **Actions →
Run workflow** tab.

## 🧠 How the filters work
- **whale**: `--min-usd` → trades with USD value (= shares × price) above the threshold.
- **smart**: `--smart` + `--min-pnl`/`--min-winrate`/`--min-closed` → only wallets
  whose historical realized PnL & win-rate pass. Scores are cached in the DB (saves API calls).
- **watchlist**: every wallet on the watchlist is always alerted, regardless of size.
- **spike**: `--spike-usd` + `--spike-window` (minutes) → one alert per market when
  total volume in the window crosses the threshold. Deduped per window, no spam.

## 🗂️ Structure
```
whale_tracker.py     # main CLI (scan/watch/poll/wallet/leaderboard/score/watchlist)
polymarket_api.py    # read-only Polymarket Data API client
db.py                # SQLite (trades, alerts, scores, watchlist)
notifier.py          # Telegram + Discord
smartmoney.py        # wallet scoring (PnL & win-rate)
.github/workflows/tracker.yml   # scheduler
```

## ⚠️ Disclaimer
This tool is for research & informational purposes only. Trading prediction
markets is risky — all decisions and risks are your own responsibility. A big
whale entering a market is a sentiment signal, **not** a guarantee of winning.
