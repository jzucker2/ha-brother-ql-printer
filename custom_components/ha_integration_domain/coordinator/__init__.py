"""
Data update coordinator package for Brother QL Printer integration.

This package provides the coordinator infrastructure for managing periodic
data updates and distributing them to all entities in the integration.

Package structure:
- base.py: Main coordinator class (BrotherQLDataUpdateCoordinator)

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from .base import BrotherQLDataUpdateCoordinator

__all__ = ["BrotherQLDataUpdateCoordinator"]
