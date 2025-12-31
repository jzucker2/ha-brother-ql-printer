"""Font size number entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_CURRENT_FONT_SIZE, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = NumberEntityDescription(
    key="font_size",
    translation_key="font_size",
    icon="mdi:format-size",
    entity_category=EntityCategory.CONFIG,
    native_min_value=10,
    native_max_value=500,
    native_step=10,
)


class BrotherQLFontSizeNumber(NumberEntity, BrotherQLEntity):
    """Font size number entity for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry
        self._attr_native_value = float(entry.options.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE))

    @property
    def native_value(self) -> float:
        """Return the current font size."""
        # Get from options (updated via service calls)
        return float(self._entry.options.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE))

    async def async_set_native_value(self, value: float) -> None:
        """
        Set the font size value.

        Args:
            value: The font size to set
        """
        # Update options with new font size
        options = dict(self._entry.options)
        options["current_font_size"] = int(value)

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.info("Font size set to %s via number entity", int(value))

        # Update local value
        self._attr_native_value = float(value)
        self.async_write_ha_state()
