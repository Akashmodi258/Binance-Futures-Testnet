# Trading Bot — Binance Futures Testnet

A Python CLI application to place **Market** and **Limit** orders on the Binance Futures Testnet (USDT-M).

---

## Setup

### 1. Register on Binance Futures Testnet

Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com), register, and generate API credentials.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

```bash
export BINANCE_TESTNET_API_KEY="your_api_key_here"
export BINANCE_TESTNET_API_SECRET="your_api_secret_here"
```

---

## How to Run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.01 --price 70000
```

### All arguments

| Argument       | Required          | Description                          |
|----------------|-------------------|--------------------------------------|
| `--symbol`     | Yes               | Trading pair, e.g. `BTCUSDT`         |
| `--side`       | Yes               | `BUY` or `SELL`                      |
| `--order-type` | Yes               | `MARKET` or `LIMIT`                  |
| `--quantity`   | Yes               | Order quantity                       |
| `--price`      | LIMIT orders only | Limit price                          |

---

## Example Output

```
===== Order Request Summary =====
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
=================================

===== Order Response =====
  Order ID     : 3865432
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 67842.50
==========================

[SUCCESS] Order placed successfully.
```

---

## Logging

All API requests, responses, and errors are logged to `trading_bot.log` in the project root.

- **Console**: INFO level and above
- **File**: DEBUG level and above (includes full request/response details)

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── cli.py                 # CLI entry point (argparse)
├── trading_bot.log        # Sample log file
├── requirements.txt
└── README.md
```

---

## Assumptions

- Uses direct REST calls (`requests`) — no third-party Binance SDK.
- API credentials are passed via environment variables (not CLI flags) to avoid accidental exposure in shell history.
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default.
- Quantity precision is passed as-is; users are responsible for matching the symbol's tick/step size rules on the testnet.
