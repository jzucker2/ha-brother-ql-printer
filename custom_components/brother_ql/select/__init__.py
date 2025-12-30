"""Select entities for Brother QL Printer integration."""

from __future__ import annotations

from custom_components.brother_ql.coordinator import BrotherQLDataUpdateCoordinator
from custom_components.brother_ql.select.label_size import BrotherQLLabelSizeSelect
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

PLATFORM = Platform.SELECT


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up select entities for the integration.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        async_add_entities: Callback to add entities
    """
    coordinator: BrotherQLDataUpdateCoordinator = entry.runtime_data.coordinator

    async_add_entities([BrotherQLLabelSizeSelect(coordinator, entry)])
