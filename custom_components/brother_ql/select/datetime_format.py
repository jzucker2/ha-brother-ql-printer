"""Date/time format select entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_DATETIME_FORMAT, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import callback

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

# Date/time format options
DATETIME_FORMAT_OPTIONS = [
    "Date",
    "Time",
    "Date and Time",
]

ENTITY_DESCRIPTION = SelectEntityDescription(
    key="datetime_format",
    translation_key="datetime_format",
    icon="mdi:calendar-clock",
    entity_category=EntityCategory.CONFIG,
    options=DATETIME_FORMAT_OPTIONS,
)


class BrotherQLDatetimeFormatSelect(SelectEntity, BrotherQLEntity):
    """Date/time format select entity for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry
        # Default to "Date and Time" if not set
        self._attr_current_option = entry.options.get("datetime_format", DEFAULT_DATETIME_FORMAT)

    @property
    def current_option(self) -> str:
        """Return the current selected datetime format."""
        return self._entry.options.get("datetime_format", DEFAULT_DATETIME_FORMAT)

    async def async_select_option(self, option: str) -> None:
        """
        Change the selected datetime format.

        Args:
            option: The datetime format option to select
        """
        if option not in DATETIME_FORMAT_OPTIONS:
            LOGGER.warning("Invalid datetime format option: %s", option)
            return

        # Update options with new datetime format
        options = dict(self._entry.options)
        options["datetime_format"] = option

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.info("Datetime format set to: %s", option)

        # Update local value
        self._attr_current_option = option
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Datetime format is stored in options, not coordinator data
        self._attr_current_option = self._entry.options.get("datetime_format", DEFAULT_DATETIME_FORMAT)
        self.async_write_ha_state()
