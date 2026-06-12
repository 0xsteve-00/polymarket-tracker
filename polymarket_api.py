"""Thin read-only client for Polymarket's public Data API (stdlib only)."""
import json
import urllib.parse
import urllib.request

BASE = "https://data-api.polymarket.com"
_UA = {"User-Agent": "polymarket-whale-tracker/2.0"}


def _get(path, params=None, timeout=20):
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_trades(limit=500, offset=0):
    """Recent trades across all markets. size=shares, price=0..1, USD=size*price."""
    return _get("/trades", {"limit": limit, "offset": offset})


def fetch_positions(wallet, limit=200):
    return _get("/positions", {"user": wallet, "limit": limit,
                               "sortBy": "CURRENT", "sortDirection": "DESC"})


def fetch_value(wallet):
    data = _get("/value", {"user": wallet})
    return data[0]["value"] if data else 0.0


def usd(trade):
    return float(trade.get("size", 0)) * float(trade.get("price", 0))


def trade_key(t):
    return f"{t.get('transactionHash','')}:{t.get('asset','')}:{t.get('timestamp','')}"
