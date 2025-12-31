"""Host URL sensor for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_PORT
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator

ENTITY_DESCRIPTION = SensorEntityDescription(
    key="host_url",
    translation_key="host_url",
    icon="mdi:link",
    entity_category=EntityCategory.DIAGNOSTIC,
    has_entity_name=True,
)


class BrotherQLHostURLSensor(SensorEntity, BrotherQLEntity):
    """Host URL sensor for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def native_value(self) -> str:
        """Return the host URL."""
        host = self.coordinator.config_entry.data.get("host", "localhost")
        port = int(self.coordinator.config_entry.data.get("port", DEFAULT_PORT))
        return f"http://{host}:{port}"

    @property
    def extra_state_attributes(self) -> dict[str, str | int]:
        """Return additional state attributes."""
        host = self.coordinator.config_entry.data.get("host", "localhost")
        port = int(self.coordinator.config_entry.data.get("port", DEFAULT_PORT))
        return {
            "host": host,
            "port": port,
        }
