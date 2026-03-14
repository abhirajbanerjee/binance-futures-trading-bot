"""CLI entry point for the Binance Futures Testnet trading bot."""

import argparse
import logging
import sys
from typing import Any

from bot.client import create_client
from bot.exceptions import APIError, ConfigurationError, NetworkError, ValidationError
from bot.logging_config import setup_logging
from bot.orders import place_limit_order, place_market_order
from bot.validators import validate_order_params

logger = logging.getLogger(__name__)


def print_order_request(params: dict[str, Any]) -> None:
    """Print a formatted summary of the outgoing order."""
    print("\nOrder Request")
    print("-------------")
    print(f"Symbol:   {params['symbol']}")
    print(f"Side:     {params['side']}")
    print(f"Type:     {params['order_type']}")
    print(f"Quantity: {params['quantity']}")
    if params.get("price") is not None:
        print(f"Price:    {params['price']}")
    print()


def print_order_response(response: dict[str, Any]) -> None:
    """Print a formatted summary of the Binance response."""
    print("Order Response")
    print("--------------")
    print(f"Order ID:          {response.get('orderId', 'N/A')}")
    print(f"Status:            {response.get('status', 'N/A')}")
    print(f"Executed Quantity:  {response.get('executedQty', 'N/A')}")
    print(f"Average Price:     {response.get('avgPrice', 'N/A')}")
    print()
    print("SUCCESS: Order placed successfully")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Place MARKET and LIMIT orders on Binance Futures Testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity (e.g. 0.002)")
    parser.add_argument("--price", default=None, help="Limit price (required for LIMIT orders)")
    return parser


def main() -> None:
    """Parse args, validate, place the order, and print results."""
    setup_logging()
    args = build_parser().parse_args()

    logger.info(
        "Received order request: symbol=%s side=%s type=%s qty=%s price=%s",
        args.symbol, args.side, args.order_type, args.quantity, args.price,
    )

    try:
        params = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        print_order_request(params)

        client = create_client()

        if params["order_type"] == "MARKET":
            response = place_market_order(
                client, params["symbol"], params["side"], params["quantity"],
            )
        else:
            response = place_limit_order(
                client, params["symbol"], params["side"],
                params["quantity"], params["price"],
            )

        print_order_response(response)

    except (ValidationError, ConfigurationError, APIError, NetworkError) as exc:
        logger.error("%s: %s", type(exc).__name__, exc.message)
        print(f"\nERROR: {exc.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
