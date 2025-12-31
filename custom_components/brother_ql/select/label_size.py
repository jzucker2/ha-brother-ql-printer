"""Label size select entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_LABEL_SIZE, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import callback

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

# All available label sizes from brother_ql library
LABEL_SIZE_OPTIONS = [
    "12",
    "12+17",
    "18",
    "29",
    "38",
    "50",
    "54",
    "62",
    "62red",
    "102",
    "103",
    "104",
    "17x54",
    "17x87",
    "23x23",
    "29x42",
    "29x90",
    "39x90",
    "39x48",
    "52x29",
    "54x29",
    "60x86",
    "62x29",
    "62x100",
    "102x51",
    "102x152",
    "103x164",
    "d12",
    "d24",
    "d58",
    "pt12",
    "pt18",
    "pt24",
    "pt36",
]

ENTITY_DESCRIPTION = SelectEntityDescription(
    key="label_size",
    translation_key="label_size",
    icon="mdi:label",
    entity_category=EntityCategory.CONFIG,
    has_entity_name=True,
    options=LABEL_SIZE_OPTIONS,
)


class BrotherQLLabelSizeSelect(SelectEntity, BrotherQLEntity):
    """Label size select entity for Brother QL Printer integration."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry
        # Default to "17x54" if not set
        self._attr_current_option = entry.options.get("label_size", DEFAULT_LABEL_SIZE)

    @property
    def current_option(self) -> str:
        """Return the current selected label size."""
        return self._entry.options.get("label_size", DEFAULT_LABEL_SIZE)

    async def async_select_option(self, option: str) -> None:
        """
        Change the selected label size.

        Args:
            option: The label size option to select
        """
        if option not in LABEL_SIZE_OPTIONS:
            LOGGER.warning("Invalid label size option: %s", option)
            return

        # Update options with new label size
        options = dict(self._entry.options)
        options["label_size"] = option

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.info("Label size set to: %s", option)

        # Update local value
        self._attr_current_option = option
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Label size is stored in options, not coordinator data
        self._attr_current_option = self._entry.options.get("label_size", DEFAULT_LABEL_SIZE)
        self.async_write_ha_state()
