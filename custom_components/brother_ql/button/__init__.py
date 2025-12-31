"""Button entities for Brother QL Printer integration."""

from __future__ import annotations

from custom_components.brother_ql.button.goober_font_size import BrotherQLGooberFontSizeButton
from custom_components.brother_ql.button.print_datetime import BrotherQLPrintDatetimeButton
from custom_components.brother_ql.button.print_text import BrotherQLPrintTextButton
from custom_components.brother_ql.button.reset_font_size import BrotherQLResetFontSizeButton
from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

PLATFORM = Platform.BUTTON


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up button entities for the integration.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        async_add_entities: Callback to add entities
    """
    coordinator: BrotherQLDataUpdateCoordinator = entry.runtime_data.coordinator

    async_add_entities(
        [
            BrotherQLResetFontSizeButton(coordinator, entry),
            BrotherQLGooberFontSizeButton(coordinator, entry),
            BrotherQLPrintTextButton(coordinator, entry),
            BrotherQLPrintDatetimeButton(coordinator, entry),
        ]
    )
