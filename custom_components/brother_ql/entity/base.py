"""
Base entity class for Brother QL Printer integration.

This module provides the base entity class that all integration entities inherit from.
It handles common functionality like device info, unique IDs, and coordinator integration.

For more information on entities:
https://developers.home-assistant.io/docs/core/entity
https://developers.home-assistant.io/docs/core/entity/index/#common-properties
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.brother_ql.const import ATTRIBUTION
from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class BrotherQLEntity(CoordinatorEntity[BrotherQLDataUpdateCoordinator]):
    """
    Base entity class for Brother QL Printer integration.

    All entities in this integration inherit from this class, which provides:
    - Automatic coordinator updates
    - Device info management
    - Unique ID generation
    - Attribution and naming conventions

    For more information:
    https://developers.home-assistant.io/docs/core/entity
    https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True  # Required for translation_key to work

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """
        Initialize the base entity.

        Args:
            coordinator: The data update coordinator for this entity.
            entity_description: The entity description defining characteristics.

        """
        super().__init__(coordinator)
        self.entity_description = entity_description
        # Include entity description key in unique_id to support multiple entities
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"

        # Get printer info from coordinator data
        data = coordinator.data
        if isinstance(data, dict):
            printer_info = data.get("printer", {})
        else:
            printer_info = {}
        model = printer_info.get("model", "Brother QL Printer")

        # Get integration version from runtime data
        # Only set sw_version if we have a valid version string (not None or empty)
        sw_version: str | None = None
        try:
            if hasattr(coordinator.config_entry, "runtime_data") and coordinator.config_entry.runtime_data:
                integration = getattr(coordinator.config_entry.runtime_data, "integration", None)
                if integration and hasattr(integration, "version"):
                    version_value = integration.version
                    if version_value and isinstance(version_value, str) and version_value.strip():
                        sw_version = version_value.strip()
        except (AttributeError, TypeError):
            # If we can't get the version (missing attributes or None values), just skip it
            pass

        # Build DeviceInfo - only include sw_version if it's a valid non-empty string
        # Home Assistant's device registry requires sw_version to be a valid version string or omitted
        device_info_kwargs: dict[str, Any] = {
            "identifiers": {
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            "name": coordinator.config_entry.title,
            "manufacturer": "Brother",
            "model": model,
            "configuration_url": f"http://{coordinator.config_entry.data.get('host', 'localhost')}:{int(coordinator.config_entry.data.get('port', 8013))}/labeldesigner",
        }

        # Only add sw_version if we have a valid non-empty string value
        # This prevents AwesomeVersion errors when comparing with existing devices
        if sw_version:
            device_info_kwargs["sw_version"] = sw_version

        self._attr_device_info = DeviceInfo(**device_info_kwargs)
