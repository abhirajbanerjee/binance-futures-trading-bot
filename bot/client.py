"""Binance Futures API client wrapper."""

import logging
from typing import Any

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.config import load_config
from bot.exceptions import APIError, NetworkError

logger = logging.getLogger(__name__)


def create_client() -> Client:
    """Initialise a Binance client pointed at the Futures Testnet."""
    config = load_config()

    try:
        client = Client(
            api_key=config["api_key"],
            api_secret=config["secret_key"],
            testnet=True,
        )
        client.FUTURES_URL = config["base_url"]
        logger.info("Binance Futures Testnet client initialised")
        return client

    except Exception as exc:
        logger.error("Failed to initialise client: %s", exc)
        raise NetworkError(f"Could not connect to Binance Testnet: {exc}") from exc


def place_order(client: Client, **params: Any) -> dict[str, Any]:
    """Send a futures order to Binance and return the response."""
    logger.info("Sending order: %s", params)

    try:
        response = client.futures_create_order(**params)
        logger.info(
            "Order response: orderId=%s status=%s",
            response.get("orderId"),
            response.get("status"),
        )
        logger.debug("Full response: %s", response)
        return response

    except BinanceAPIException as exc:
        logger.error("API error [%s]: %s", exc.status_code, exc.message)
        raise APIError(f"Binance API error: {exc.message}", exc.status_code) from exc

    except BinanceRequestException as exc:
        logger.error("Request error: %s", exc)
        raise NetworkError(f"Request to Binance failed: {exc}") from exc

    except Exception as exc:
        logger.error("Unexpected error: %s", exc)
        raise NetworkError(f"Network error while placing order: {exc}") from exc
