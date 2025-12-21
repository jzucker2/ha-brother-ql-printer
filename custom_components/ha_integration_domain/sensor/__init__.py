"""Sensor platform for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.ha_integration_domain.const import PARALLEL_UPDATES
from homeassistant.components.sensor import SensorEntityDescription

from .status import (
    ENTITY_DESCRIPTIONS as STATUS_DESCRIPTIONS,
    BrotherQLStatusSensor,
)

if TYPE_CHECKING:
    from custom_components.ha_integration_domain.data import BrotherQLConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Combine all entity descriptions from different modules
ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    *STATUS_DESCRIPTIONS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    # Add status sensors
    async_add_entities(
        BrotherQLStatusSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in STATUS_DESCRIPTIONS
    )
