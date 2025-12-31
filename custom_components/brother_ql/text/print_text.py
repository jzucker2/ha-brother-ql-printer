"""Print text entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_PRINT_TEXT, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.text import TextEntity, TextEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = TextEntityDescription(
    key="print_text",
    translation_key="print_text",
    icon="mdi:text",
    entity_category=EntityCategory.CONFIG,
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
        # Load value from options or use default
        self._attr_native_value = entry.options.get("print_text", DEFAULT_PRINT_TEXT)

    @property
    def native_value(self) -> str:
        """Return the current text value."""
        # Get from options (persisted across reloads)
        return self._entry.options.get("print_text", DEFAULT_PRINT_TEXT)

    async def async_set_value(self, value: str) -> None:
        """
        Set the text value.

        Args:
            value: The text to set
        """
        # Update options with new text value
        options = dict(self._entry.options)
        options["print_text"] = value

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.debug("Print text updated: %s", value)

        # Update local value
        self._attr_native_value = value
        self.async_write_ha_state()
