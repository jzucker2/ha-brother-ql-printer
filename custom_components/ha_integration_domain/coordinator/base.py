"""
Core DataUpdateCoordinator implementation for Brother QL Printer integration.

This module contains the main coordinator class that manages data fetching
and updates for all entities in the integration. It handles refresh cycles,
error handling, and triggers reauthentication when needed.

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.ha_integration_domain.api import (
    BrotherQLApiClientAuthenticationError,
    BrotherQLApiClientError,
)
from custom_components.ha_integration_domain.const import DOMAIN, LOGGER
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

if TYPE_CHECKING:
    from custom_components.ha_integration_domain.data import BrotherQLConfigEntry


class BrotherQLDataUpdateCoordinator(DataUpdateCoordinator):
    """
    Class to manage fetching data from the Brother QL Web API.

    This coordinator handles all data fetching for the integration and distributes
    updates to all entities. It manages:
    - Periodic data updates based on update_interval
    - Error handling and recovery
    - Connection failure detection
    - Data distribution to all entities

    For more information:
    https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities

    Attributes:
        config_entry: The config entry for this integration instance.
    """

    config_entry: BrotherQLConfigEntry

    async def _async_setup(self) -> None:
        """
        Set up the coordinator.

        This method is called automatically during async_config_entry_first_refresh()
        and is the ideal place for one-time initialization tasks such as:
        - Loading device information
        - Setting up event listeners
        - Initializing caches

        This runs before the first data fetch, ensuring any required setup
        is complete before entities start requesting data.
        """
        # Fetch printer info once at startup
        try:
            printer_info = await self.config_entry.runtime_data.client.async_get_printer_info()
            LOGGER.debug("Printer info: %s", printer_info)
        except Exception as exception:  # noqa: BLE001
            LOGGER.warning("Could not fetch printer info during setup: %s", exception)
        LOGGER.debug("Coordinator setup complete for %s", self.config_entry.entry_id)

    async def _async_update_data(self) -> Any:
        """
        Fetch data from API endpoint.

        This is the only method that should be implemented in a DataUpdateCoordinator.
        It is called automatically based on the update_interval.

        The API client uses the connection details from config_entry:
        - host: from config_entry.data["host"]
        - port: from config_entry.data["port"]

        Expected API response structure from /api/status:
        {
            "status": "ready" | "printing" | "error",
            "printer": {
                "model": "QL-800",
                "connected": true
            },
            "last_print": "2024-01-01T12:00:00Z"
        }

        Returns:
            The data from the API as a dictionary.

        Raises:
            ConfigEntryAuthFailed: If connection fails persistently, triggers reauth.
            UpdateFailed: If data fetching fails for other reasons.
        """
        try:
            # Fetch printer status
            status = await self.config_entry.runtime_data.client.async_get_status()
            return status
        except BrotherQLApiClientAuthenticationError as exception:
            LOGGER.warning("Connection error - %s", exception)
            raise ConfigEntryAuthFailed(
                translation_domain=DOMAIN,
                translation_key="connection_failed",
            ) from exception
        except BrotherQLApiClientError as exception:
            LOGGER.exception("Error communicating with printer API")
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
            ) from exception
