# Binance Futures Testnet Trading Bot

CLI tool to place MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M).

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Add your Binance Futures Testnet API keys to `.env`:

```
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
```

Get testnet keys from [testnet.binancefuture.com](https://testnet.binancefuture.com).

## Usage

**Market order:**

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.002
```

**Limit order:**

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.002 --price 65000
```

| Argument       | Required | Description                      |
|----------------|----------|----------------------------------|
| `--symbol`     | Yes      | Trading pair (e.g. `BTCUSDT`)    |
| `--side`       | Yes      | `BUY` or `SELL`                  |
| `--order-type` | Yes      | `MARKET` or `LIMIT`              |
| `--quantity`   | Yes      | Order size (e.g. `0.002`)        |
| `--price`      | No       | Required for LIMIT orders        |

## Example Output

```
Order Request
-------------
Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.002

Order Response
--------------
Order ID:          12345678
Status:            FILLED
Executed Quantity:  0.002
Average Price:     62340.20

SUCCESS: Order placed successfully
```

## Logs

All activity is logged to `trading_bot.log`:

```
2026-03-14 12:10:01 | INFO  | orders | Placing MARKET order: symbol=BTCUSDT side=BUY qty=0.002
2026-03-14 12:10:02 | INFO  | client | Order response: orderId=12345678 status=FILLED
```
