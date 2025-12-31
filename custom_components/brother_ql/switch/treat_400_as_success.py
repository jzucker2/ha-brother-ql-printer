"""Switch to treat 400 errors as success for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import callback

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = SwitchEntityDescription(
    key="treat_400_as_success",
    translation_key="treat_400_as_success",
    icon="mdi:bug-check",
    entity_category=EntityCategory.CONFIG,
)


class BrotherQLTreat400AsSuccessSwitch(SwitchEntity, BrotherQLEntity):
    """Switch to treat HTTP 400 errors as success for print operations."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry
        # Default to True (on) if not set
        self._attr_is_on = entry.options.get("treat_400_as_success", True)

    @property
    def is_on(self) -> bool:
        """Return True if the switch is on."""
        return self._entry.options.get("treat_400_as_success", True)

    async def async_turn_on(self) -> None:
        """Turn the switch on."""
        options = dict(self._entry.options)
        options["treat_400_as_success"] = True
        self.hass.config_entries.async_update_entry(self._entry, options=options)
        self._attr_is_on = True
        self.async_write_ha_state()
        LOGGER.info("Treat 400 as success enabled")

    async def async_turn_off(self) -> None:
        """Turn the switch off."""
        options = dict(self._entry.options)
        options["treat_400_as_success"] = False
        self.hass.config_entries.async_update_entry(self._entry, options=options)
        self._attr_is_on = False
        self.async_write_ha_state()
        LOGGER.info("Treat 400 as success disabled")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Switch state is stored in options, not coordinator data
        self._attr_is_on = self._entry.options.get("treat_400_as_success", True)
        self.async_write_ha_state()
