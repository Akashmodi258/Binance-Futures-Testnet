import argparse
import os
import sys

from bot.client import BinanceAPIError, BinanceClient
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import ValidationError, validate_inputs

logger = setup_logging().getChild("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M).",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, default=None, help="Limit price (required for LIMIT orders)")
    return parser


def print_summary(symbol, side, order_type, quantity, price):
    print("\n===== Order Request Summary =====")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"  Price      : {price}")
    print("=================================\n")


def print_response(response: dict):
    print("\n===== Order Response =====")
    print(f"  Order ID     : {response.get('orderId')}")
    print(f"  Status       : {response.get('status')}")
    print(f"  Executed Qty : {response.get('executedQty')}")
    avg_price = response.get('avgPrice')
    if avg_price:
        print(f"  Avg Price    : {avg_price}")
    print("==========================\n")


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Validate inputs
    try:
        symbol, side, order_type, quantity, price = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)

    print_summary(symbol, side, order_type, quantity, price)

    # Load credentials from environment
    api_key = "hMKaod4zxVRoRvW5vmE6oP9BeZM9a1zL0Y2CFNdD30AlwFg97gj5k8TsfpgTHKzi"
    api_secret = "QtYvijIV8ham7sovFZXm8dIhgcDHd4JZzWLMKYTnsqhkPRO55ptuV1JdoFeMPA0z"

    if not api_key or not api_secret:
        msg = (
            "API credentials not set. "
            "Export BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET."
        )
        logger.error(msg)
        print(f"\n[ERROR] {msg}\n")
        sys.exit(1)

    client = BinanceClient(api_key=api_key, api_secret=api_secret)

    # Place the order
    try:
        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
        print_response(response)
        print("[SUCCESS] Order placed successfully.")
        logger.info("CLI completed successfully.")
    except ValidationError as e:
        logger.error("Validation error: %s", e)
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)
    except BinanceAPIError as e:
        logger.error("Binance API error: %s", e)
        print(f"\n[FAILURE] {e}\n")
        sys.exit(1)
    except (ConnectionError, TimeoutError) as e:
        logger.error("Network error: %s", e)
        print(f"\n[FAILURE] Network error: {e}\n")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        print(f"\n[FAILURE] Unexpected error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
