"""Score a wallet as 'smart money' from its Polymarket position history.

We use realized PnL on resolved/closed positions to estimate skill:
  - realized_pnl : sum of realizedPnl across positions (USDC)
  - winrate      : fraction of closed positions with realizedPnl > 0
  - n_closed     : number of closed positions considered
  - cur_value    : current open portfolio value
"""
from polymarket_api import fetch_positions, fetch_value


def score_wallet(wallet):
    positions = fetch_positions(wallet, limit=200)
    realized = 0.0
    closed = 0
    wins = 0
    for p in positions:
        rp = float(p.get("realizedPnl", 0) or 0)
        # treat a position as "closed" if it's resolved/redeemable or fully realized
        is_closed = bool(p.get("redeemable")) or abs(float(p.get("currentValue", 0) or 0)) < 0.01
        if is_closed and (rp != 0 or float(p.get("totalBought", 0) or 0) > 0):
            closed += 1
            realized += rp
            if rp > 0:
                wins += 1
    winrate = (wins / closed) if closed else 0.0
    cur_value = fetch_value(wallet)
    return {
        "wallet": wallet.lower(),
        "realized_pnl": round(realized, 2),
        "winrate": round(winrate, 4),
        "n_closed": closed,
        "cur_value": round(float(cur_value), 2),
    }


def is_smart(score, min_pnl=0.0, min_winrate=0.0, min_closed=5):
    """Whether a wallet passes the smart-money filter."""
    if score["n_closed"] < min_closed:
        return False
    return score["realized_pnl"] >= min_pnl and score["winrate"] >= min_winrate
