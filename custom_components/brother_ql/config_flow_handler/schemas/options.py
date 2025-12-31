"""
Options flow schemas.

Schemas for the options flow that allows users to modify settings
after initial configuration.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.brother_ql.const import (
    DEFAULT_CURRENT_FONT_SIZE,
    DEFAULT_FONT_SIZE,
    DEFAULT_UPDATE_INTERVAL_SECONDS,
    GOOBER_FONT_SIZE,
)
from homeassistant.helpers import selector


def get_options_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Get schema for options flow.

    Args:
        defaults: Optional dictionary of current option values.

    Returns:
        Voluptuous schema for options configuration.

    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Optional(
                "update_interval_seconds",
                default=defaults.get("update_interval_seconds", DEFAULT_UPDATE_INTERVAL_SECONDS),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=10,
                    max=3600,
                    step=10,
                    unit_of_measurement="s",
                    mode=selector.NumberSelectorMode.BOX,
                ),
            ),
            vol.Optional(
                "default_font_size",
                default=defaults.get("default_font_size", DEFAULT_FONT_SIZE),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=10,
                    max=500,
                    step=10,
                    mode=selector.NumberSelectorMode.BOX,
                ),
            ),
            vol.Optional(
                "goober_font_size",
                default=defaults.get("goober_font_size", GOOBER_FONT_SIZE),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=10,
                    max=500,
                    step=10,
                    mode=selector.NumberSelectorMode.BOX,
                ),
            ),
            vol.Optional(
                "current_font_size",
                default=defaults.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=10,
                    max=500,
                    step=10,
                    mode=selector.NumberSelectorMode.BOX,
                ),
            ),
        },
    )


__all__ = [
    "get_options_schema",
]
