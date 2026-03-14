"""Order placement logic for market and limit orders."""

import logging
from typing import Any

from binance.client import Client

from bot.client import place_order

logger = logging.getLogger(__name__)


def place_market_order(
    client: Client, symbol: str, side: str, quantity: float
) -> dict[str, Any]:
    """Execute a futures MARKET order."""
    logger.info("Placing MARKET order: symbol=%s side=%s qty=%s", symbol, side, quantity)

    return place_order(
        client,
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=str(quantity),
    )


def place_limit_order(
    client: Client, symbol: str, side: str, quantity: float, price: float
) -> dict[str, Any]:
    """Execute a futures LIMIT GTC order."""
    logger.info(
        "Placing LIMIT order: symbol=%s side=%s qty=%s price=%s",
        symbol, side, quantity, price,
    )

    return place_order(
        client,
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=str(quantity),
        price=str(price),
        timeInForce="GTC",
    )
