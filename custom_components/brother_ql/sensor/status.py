"""Printer status sensor for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="printer_status",
        translation_key="printer_status",
        icon="mdi:printer",
        entity_category=EntityCategory.DIAGNOSTIC,
        has_entity_name=True,
    ),
)


class BrotherQLStatusSensor(SensorEntity, BrotherQLEntity):
    """Printer status sensor for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def native_value(self) -> str | None:
        """Return the current printer status."""
        if not self.coordinator.data:
            return None

        data = self.coordinator.data
        if isinstance(data, dict):
            return data.get("status", "unknown")

        return None

    @property
    def extra_state_attributes(self) -> dict[str, str | int | None]:
        """Return additional state attributes."""
        data = self.coordinator.data or {}
        printer = data.get("printer", {})
        last_print = data.get("last_print")

        return {
            "printer_model": printer.get("model", "Unknown"),
            "printer_connected": printer.get("connected", False),
            "last_print": last_print,
        }
