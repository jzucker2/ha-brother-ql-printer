"""Sensor platform for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntityDescription

from .host_url import ENTITY_DESCRIPTION as HOST_URL_DESCRIPTION, BrotherQLHostURLSensor
from .status import ENTITY_DESCRIPTIONS as STATUS_DESCRIPTIONS, BrotherQLStatusSensor

if TYPE_CHECKING:
    from custom_components.brother_ql.data import BrotherQLConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Combine all entity descriptions from different modules
ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (*STATUS_DESCRIPTIONS,)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator

    # Add status sensors
    entities = [
        BrotherQLStatusSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in STATUS_DESCRIPTIONS
    ]

    # Add host URL sensor
    entities.append(BrotherQLHostURLSensor(coordinator, HOST_URL_DESCRIPTION))

    async_add_entities(entities)
