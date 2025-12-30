"""
Connection validators.

Validation functions for testing connection to brother_ql_web service.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.api import (
    BrotherQLApiClient,
    BrotherQLApiClientError,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_connection(hass: HomeAssistant, host: str, port: int) -> None:
    """
    Validate connection to brother_ql_web service by testing API connection.

    Args:
        hass: Home Assistant instance.
        host: The hostname or IP address of the brother_ql_web service.
        port: The port number of the brother_ql_web service.

    Raises:
        BrotherQLApiClientError: If connection fails or service is unreachable.

    """
    client = BrotherQLApiClient(
        host=host,
        port=port,
        session=async_get_clientsession(hass),
    )
    # Test connection by getting printer status
    await client.async_get_status()


__all__ = [
    "validate_connection",
]
