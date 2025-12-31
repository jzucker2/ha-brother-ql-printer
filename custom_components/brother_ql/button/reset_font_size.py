"""Reset font size button entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_FONT_SIZE, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = ButtonEntityDescription(
    key="reset_font_size",
    translation_key="reset_font_size",
    icon="mdi:restore",
    entity_category=EntityCategory.CONFIG,
)


class BrotherQLResetFontSizeButton(ButtonEntity, BrotherQLEntity):
    """Button to reset font size to default."""

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
        # Get default font size from options or use constant
        default_font_size = self._entry.options.get("default_font_size", DEFAULT_FONT_SIZE)

        # Update options with default font size
        options = dict(self._entry.options)
        options["current_font_size"] = int(default_font_size)

        self.hass.config_entries.async_update_entry(self._entry, options=options)
        LOGGER.info("Font size reset to default: %s", default_font_size)

        # Trigger entity update
        await self.hass.config_entries.async_reload(self._entry.entry_id)
