"""Print text entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.text import TextEntity, TextEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import callback

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = TextEntityDescription(
    key="print_text",
    translation_key="print_text",
    icon="mdi:text",
    entity_category=EntityCategory.CONFIG,
    has_entity_name=True,
    native_min=0,
    native_max=1000,
)


class BrotherQLPrintText(TextEntity, BrotherQLEntity):
    """Text entity for entering text to print."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the text entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry
        self._attr_native_value = ""

    @property
    def native_value(self) -> str:
        """Return the current text value."""
        return self._attr_native_value

    async def async_set_value(self, value: str) -> None:
        """
        Set the text value.

        Args:
            value: The text to set
        """
        self._attr_native_value = value
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Text entity doesn't depend on coordinator data
        # But we should still update state if needed
        self.async_write_ha_state()
