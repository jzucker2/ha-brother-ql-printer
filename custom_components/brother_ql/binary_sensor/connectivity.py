"""Connectivity binary sensor for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import (
        BrotherQLDataUpdateCoordinator,
    )

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="printer_connectivity",
        translation_key="printer_connectivity",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:printer",
        has_entity_name=True,
    ),
)


class BrotherQLConnectivitySensor(BinarySensorEntity, BrotherQLEntity):
    """Connectivity sensor for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def is_on(self) -> bool:
        """Return true if the printer connection is established."""
        # Connection is considered established if coordinator has valid data
        if not self.coordinator.last_update_success:
            return False
        
        # Check if printer is connected according to API response
        data = self.coordinator.data
        if data and isinstance(data, dict):
            printer = data.get("printer", {})
            return printer.get("connected", False)
        
        return False

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return additional state attributes."""
        data = self.coordinator.data or {}
        printer = data.get("printer", {})
        
        return {
            "update_interval": str(self.coordinator.update_interval),
            "printer_model": printer.get("model", "Unknown"),
            "api_endpoint": f"http://{self.coordinator.config_entry.data.get('host', 'localhost')}:{self.coordinator.config_entry.data.get('port', 8013)}",
        }
