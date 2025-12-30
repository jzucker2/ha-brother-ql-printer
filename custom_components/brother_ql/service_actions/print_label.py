"""Print label service action handlers for Brother QL Printer integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.brother_ql.const import LOGGER

if TYPE_CHECKING:
    from custom_components.brother_ql.data import BrotherQLConfigEntry
    from homeassistant.core import HomeAssistant, ServiceCall


async def async_handle_print_text(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the print_text service action call.

    Prints a text label on the Brother QL printer.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    LOGGER.info("Print text service called with data: %s", call.data)

    text = call.data.get("text")
    if not text:
        msg = "Text parameter is required"
        raise ValueError(msg)

    font_size = call.data.get("font_size", 100)
    font_family = call.data.get("font_family", "Arial")
    label_size = call.data.get("label_size")
    orientation = call.data.get("orientation", "standard")

    client = entry.runtime_data.client

    try:
        kwargs = {}
        if label_size:
            kwargs["label_size"] = label_size
        if orientation:
            kwargs["orientation"] = orientation

        await client.async_print_text(
            text=text,
            font_size=font_size,
            font_family=font_family,
            **kwargs,
        )
        LOGGER.info("Text label printed successfully: %s", text)
    except Exception as exception:
        LOGGER.exception("Failed to print text label: %s", exception)
        raise


async def async_handle_print_barcode(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the print_barcode service action call.

    Prints a barcode label on the Brother QL printer.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    LOGGER.info("Print barcode service called with data: %s", call.data)

    data = call.data.get("data")
    if not data:
        msg = "Data parameter is required"
        raise ValueError(msg)

    barcode_type = call.data.get("barcode_type", "CODE128")
    label_size = call.data.get("label_size")
    orientation = call.data.get("orientation", "standard")

    client = entry.runtime_data.client

    try:
        kwargs = {}
        if label_size:
            kwargs["label_size"] = label_size
        if orientation:
            kwargs["orientation"] = orientation

        await client.async_print_barcode(
            barcode_data=data,
            barcode_type=barcode_type,
            **kwargs,
        )
        LOGGER.info("Barcode label printed successfully: %s", data)
    except Exception as exception:
        LOGGER.exception("Failed to print barcode label: %s", exception)
        raise


async def async_handle_reload_data(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the reload_data service call.

    Forces a refresh of the integration data.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    LOGGER.info("Reload data service called")

    coordinator = entry.runtime_data.coordinator
    await coordinator.async_request_refresh()
    LOGGER.info("Data reload completed")
