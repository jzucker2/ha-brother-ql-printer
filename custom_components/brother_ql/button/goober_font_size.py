"""Goober font size button entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import GOOBER_FONT_SIZE, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = ButtonEntityDescription(
    key="goober_font_size",
    translation_key="goober_font_size",
    icon="mdi:format-size",
    entity_category=EntityCategory.CONFIG,
)


class BrotherQLGooberFontSizeButton(ButtonEntity, BrotherQLEntity):
    """Button to set font size to goober preset."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator, ENTITY_DESCRIPTION)
        self._entry = entry

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get goober font size from options or use constant
        goober_font_size = self._entry.options.get("goober_font_size", GOOBER_FONT_SIZE)

        # Update options with goober font size
        options = dict(self._entry.options)
        options["current_font_size"] = int(goober_font_size)

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.info("Font size set to goober: %s", goober_font_size)

        # Trigger entity update
        await self.hass.config_entries.async_reload(self._entry.entry_id)
