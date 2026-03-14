"""Load API credentials from .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

from bot.exceptions import ConfigurationError

TESTNET_BASE_URL = "https://testnet.binancefuture.com"

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_config() -> dict[str, str]:
    """Load and validate Binance API keys from .env."""
    load_dotenv(dotenv_path=_ENV_PATH)

    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")

    if not api_key:
        raise ConfigurationError(
            "BINANCE_API_KEY is not set. Add it to your .env file."
        )
    if not secret_key:
        raise ConfigurationError(
            "BINANCE_SECRET_KEY is not set. Add it to your .env file."
        )

    return {
        "api_key": api_key,
        "secret_key": secret_key,
        "base_url": TESTNET_BASE_URL,
    }
