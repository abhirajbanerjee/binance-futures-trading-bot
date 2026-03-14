"""Validate CLI inputs before placing orders."""

import logging
import re

from bot.exceptions import ValidationError

logger = logging.getLogger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
SYMBOL_PATTERN = re.compile(r"^[A-Z]{2,10}USDT$")


def validate_symbol(symbol: str) -> None:
    """Ensure symbol matches a valid USDT-M pair like BTCUSDT."""
    if not symbol or not SYMBOL_PATTERN.match(symbol.upper()):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. "
            "Expected uppercase pair ending in USDT (e.g. BTCUSDT)."
        )


def validate_side(side: str) -> None:
    """Ensure side is BUY or SELL."""
    if side.upper() not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side '{side}'. Allowed: {', '.join(sorted(VALID_SIDES))}."
        )


def validate_order_type(order_type: str) -> None:
    """Ensure order type is MARKET or LIMIT."""
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. "
            f"Allowed: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )


def validate_quantity(quantity: str | float) -> float:
    """Parse quantity and ensure it's a positive number."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a positive number.")

    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got {quantity}.")
    return qty


def validate_price(price: str | float | None, order_type: str) -> float | None:
    """Validate price — required and positive for LIMIT orders, ignored for MARKET."""
    if order_type.upper() == "MARKET":
        return None

    if price is None:
        raise ValidationError("Price is required for LIMIT orders. Use --price <value>.")

    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid price '{price}'. Must be a positive number.")

    if p <= 0:
        raise ValidationError(f"Price must be greater than 0, got {price}.")
    return p


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float,
    price: str | float | None = None,
) -> dict:
    """Run all validations and return a normalised parameter dict."""
    validate_symbol(symbol)
    validate_side(side)
    validate_order_type(order_type)
    validated_qty = validate_quantity(quantity)
    validated_price = validate_price(price, order_type)

    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "order_type": order_type.upper(),
        "quantity": validated_qty,
        "price": validated_price,
    }

    logger.debug("Validated params: %s", params)
    return params
