# Contributing

Thanks for your interest in contributing! 🐋

## Getting started
1. Fork the repo and clone your fork.
2. No dependencies needed — just Python 3.9+.
3. Run the tracker locally:
   ```bash
   python3 whale_tracker.py scan --min-usd 1000
   ```

## How to contribute
- **Bug reports / feature requests** — open an [issue](../../issues) with steps
  to reproduce or a clear description of the idea.
- **Pull requests** — fork → create a branch → make your change → open a PR.
  Keep PRs small and focused. Describe what changed and why.

## Guidelines
- Keep the project **dependency-free** (standard library only) so anyone can
  run it with plain Python.
- This tool must stay **read-only**: it only reads public Polymarket data and
  sends notifications. PRs that place trades, touch wallets, or automate any
  on-chain actions will not be accepted.
- Test your changes against the live API before submitting
  (`python3 whale_tracker.py scan` is a quick smoke test).
- Match the existing code style (small functions, clear names, no heavy
  abstractions).

## Ideas welcome
Good first contributions: new notification channels (Slack, email), better
smart-money scoring, market category filters, export to CSV, simple web
dashboard for the SQLite history.
