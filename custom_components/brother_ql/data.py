"""Custom types for Brother QL Printer integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import BrotherQLApiClient
    from .coordinator import BrotherQLDataUpdateCoordinator


type BrotherQLConfigEntry = ConfigEntry[BrotherQLData]


@dataclass
class BrotherQLData:
    """Data for Brother QL Printer integration."""

    client: BrotherQLApiClient
    coordinator: BrotherQLDataUpdateCoordinator
    integration: Integration
