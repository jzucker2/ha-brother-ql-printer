"""Print datetime button entity for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import DEFAULT_CURRENT_FONT_SIZE, DEFAULT_DATETIME_FORMAT, LOGGER
from custom_components.brother_ql.entity import BrotherQLEntity
from custom_components.brother_ql.service_actions.print_label import async_handle_print_datetime
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import Context, ServiceCall

if TYPE_CHECKING:
    from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
    from homeassistant.config_entries import ConfigEntry

ENTITY_DESCRIPTION = ButtonEntityDescription(
    key="print_datetime",
    translation_key="print_datetime",
    icon="mdi:calendar-clock",
    entity_category=EntityCategory.CONFIG,
)


class BrotherQLPrintDatetimeButton(ButtonEntity, BrotherQLEntity):
    """Button to print datetime using current format selection."""

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
        # Get datetime format from select entity (stored in options)
        datetime_format = self._entry.options.get("datetime_format", DEFAULT_DATETIME_FORMAT)

        # Get current font size
        current_font_size = self._entry.options.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE)

        # Call the handler directly with this entry's context
        context = Context()
        service_call = ServiceCall(
            self.hass,
            "brother_ql",
            "print_datetime",
            {
                "datetime_format": datetime_format,
                "font_size": int(current_font_size),
            },
            context=context,
        )

        try:
            await async_handle_print_datetime(self.hass, self._entry, service_call)
            LOGGER.info(
                "Datetime printed successfully (format: %s, font size: %s)",
                datetime_format,
                current_font_size,
            )
        except Exception as exception:
            LOGGER.exception("Failed to print datetime: %s", exception)
            raise
