"""Font size button entities for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_CURRENT_FONT_SIZE, DEFAULT_FONT_SIZE, GOOBER_FONT_SIZE, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN, EntityCategory
from homeassistant.helpers import entity_registry as er

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

RESET_FONT_SIZE_DESCRIPTION = ButtonEntityDescription(
    key="reset_font_size",
    translation_key="reset_font_size",
    icon="mdi:restore",
    entity_category=EntityCategory.CONFIG,
    has_entity_name=True,
)

GOOBER_FONT_SIZE_DESCRIPTION = ButtonEntityDescription(
    key="goober_font_size",
    translation_key="goober_font_size",
    icon="mdi:format-size",
    entity_category=EntityCategory.CONFIG,
    has_entity_name=True,
)

PRINT_TEXT_DESCRIPTION = ButtonEntityDescription(
    key="print_text",
    translation_key="print_text",
    icon="mdi:printer",
    entity_category=EntityCategory.CONFIG,
    has_entity_name=True,
)


class BrotherQLResetFontSizeButton(ButtonEntity, BrotherQLEntity):
    """Button to reset font size to default."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator, RESET_FONT_SIZE_DESCRIPTION)
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


class BrotherQLGooberFontSizeButton(ButtonEntity, BrotherQLEntity):
    """Button to set font size to goober preset."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator, GOOBER_FONT_SIZE_DESCRIPTION)
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


class BrotherQLPrintTextButton(ButtonEntity, BrotherQLEntity):
    """Button to print text using current font size."""

    def __init__(
        self,
        coordinator: BrotherQLDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator, PRINT_TEXT_DESCRIPTION)
        self._entry = entry

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get print text from the text entity
        # Find the text entity for this config entry using entity registry
        entity_registry = er.async_get(self.hass)
        text_entity_id = None

        # Find the print_text text entity for this config entry
        for entity_id, entity_entry in entity_registry.entities.items():
            if (
                entity_entry.config_entry_id == self._entry.entry_id
                and entity_entry.domain == "text"
                and entity_entry.unique_id == f"{self._entry.entry_id}_print_text"
            ):
                text_entity_id = entity_id
                break

        if not text_entity_id:
            LOGGER.error("Print text entity not found")
            return

        # Get the text value from the entity state
        state = self.hass.states.get(text_entity_id)
        if not state:
            LOGGER.warning("Print text entity not found in state registry")
            return

        state_value = state.state
        if not state_value or state_value in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            LOGGER.warning("No text to print - text entity is %s", state_value if state_value else "empty")
            return

        text_to_print = state_value.strip()
        if not text_to_print:
            LOGGER.warning("No text to print - text entity is empty")
            return

        # Get current font size
        current_font_size = self._entry.options.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE)

        # Call the service using hass.services.async_call (proper way to call services programmatically)
        try:
            await self.hass.services.async_call(
                "brother_ql",
                "print_text",
                {
                    "text": text_to_print,
                    "font_size": int(current_font_size),
                },
                blocking=True,
            )
            LOGGER.info("Text printed successfully: %s (font size: %s)", text_to_print, current_font_size)
        except Exception as exception:
            LOGGER.exception("Failed to print text: %s", exception)
            raise
