"""Default font size number entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_FONT_SIZE, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = NumberEntityDescription(
    key="default_font_size",
    translation_key="default_font_size",
    icon="mdi:format-size",
    entity_category=EntityCategory.CONFIG,
    native_min_value=10,
    native_max_value=500,
    native_step=10,
)


class BrotherQLDefaultFontSizeNumber(NumberEntity, BrotherQLEntity):
    """Default font size number entity for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry
        self._attr_native_value = float(entry.options.get("default_font_size", DEFAULT_FONT_SIZE))

    @property
    def native_value(self) -> float:
        """Return the current default font size."""
        # Get from options (updated via number entity or options flow)
        return float(self._entry.options.get("default_font_size", DEFAULT_FONT_SIZE))

    async def async_set_native_value(self, value: float) -> None:
        """
        Set the default font size value.

        Args:
            value: The default font size to set
        """
        # Update options with new default font size
        options = dict(self._entry.options)
        options["default_font_size"] = int(value)

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.info("Default font size set to %s via number entity", int(value))

        # Update local value
        self._attr_native_value = float(value)
        self.async_write_ha_state()
