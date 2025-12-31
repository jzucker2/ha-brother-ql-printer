"""Print label service action handlers for Brother QL Printer integration."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import aiohttp

from custom_components.brother_ql.api import BrotherQLApiClientCommunicationError
from custom_components.brother_ql.const import (
    DEFAULT_CURRENT_FONT_SIZE,
    DEFAULT_DATETIME_FORMAT,
    DEFAULT_FONT_SIZE,
    DEFAULT_LABEL_SIZE,
    GOOBER_FONT_SIZE,
    LOGGER,
)

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

    # Use provided font_size or fall back to stored current_font_size or default
    font_size = call.data.get("font_size")
    if font_size is None:
        font_size = entry.options.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE)
    font_family = call.data.get("font_family", "DejaVu Math TeX Gyre,Regular")
    alignment = call.data.get("alignment", "center")
    line_spacing = call.data.get("line_spacing", "100")
    # Use provided label_size or fall back to stored label_size from select entity or default
    label_size = call.data.get("label_size")
    if label_size is None:
        label_size = entry.options.get("label_size", DEFAULT_LABEL_SIZE)
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
            alignment=alignment,
            line_spacing=line_spacing,
            **kwargs,
        )
        LOGGER.info("Text label printed successfully: %s", text)
    except Exception as exception:
        # Check if we should treat 400 errors as success
        treat_400_as_success = entry.options.get("treat_400_as_success", True)

        # Check if this is a 400 error
        # The exception may be wrapped in BrotherQLApiClientCommunicationError,
        # so we need to check the exception chain (__cause__)
        is_400_error = False

        # Check if exception is directly a ClientResponseError with status 400
        if isinstance(exception, aiohttp.ClientResponseError) and exception.status == 400:
            is_400_error = True
        # Check if exception is wrapped and the original cause is a ClientResponseError with status 400
        elif isinstance(exception, BrotherQLApiClientCommunicationError) and hasattr(exception, "__cause__"):
            original_exception = exception.__cause__
            if isinstance(original_exception, aiohttp.ClientResponseError) and original_exception.status == 400:
                is_400_error = True
        # Fallback: check any exception's cause for ClientResponseError with status 400
        elif hasattr(exception, "__cause__") and isinstance(exception.__cause__, aiohttp.ClientResponseError):
            original_exception = exception.__cause__
            if original_exception.status == 400:
                is_400_error = True

        if treat_400_as_success and is_400_error:
            LOGGER.info(
                "Received HTTP 400 error but treating as success (switch enabled): %s",
                text,
            )
            return

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
    # Use provided label_size or fall back to stored label_size from select entity or default
    label_size = call.data.get("label_size")
    if label_size is None:
        label_size = entry.options.get("label_size", DEFAULT_LABEL_SIZE)
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


async def async_handle_print_datetime(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the print_datetime service action call.

    Prints a datetime label on the Brother QL printer.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    LOGGER.info("Print datetime service called with data: %s", call.data)

    # Get datetime format from service call or fall back to select entity value or default
    datetime_format = call.data.get("datetime_format")
    if datetime_format is None:
        datetime_format = entry.options.get("datetime_format", DEFAULT_DATETIME_FORMAT)

    # Validate datetime format
    valid_formats = ["Date", "Time", "Date and Time"]
    if datetime_format not in valid_formats:
        msg = f"Invalid datetime format: {datetime_format}. Must be one of: {', '.join(valid_formats)}"
        raise ValueError(msg)

    # Generate datetime text based on format
    now = datetime.now()
    if datetime_format == "Date":
        datetime_text = now.strftime("%m/%d/%Y")  # e.g., 12/04/2025
    elif datetime_format == "Time":
        datetime_text = now.strftime("%I:%M:%S %p")  # e.g., 03:18:55 AM
    else:  # "Date and Time"
        datetime_text = f"{now.strftime('%I:%M:%S %p')}, {now.strftime('%m/%d/%Y')}"  # e.g., 03:18:55 AM, 12/04/2025

    # Use provided font_size or fall back to stored current_font_size or default
    font_size = call.data.get("font_size")
    if font_size is None:
        font_size = entry.options.get("current_font_size", DEFAULT_CURRENT_FONT_SIZE)
    font_family = call.data.get("font_family", "DejaVu Math TeX Gyre,Regular")
    alignment = call.data.get("alignment", "center")
    line_spacing = call.data.get("line_spacing", "100")
    # Use provided label_size or fall back to stored label_size from select entity or default
    label_size = call.data.get("label_size")
    if label_size is None:
        label_size = entry.options.get("label_size", DEFAULT_LABEL_SIZE)
    orientation = call.data.get("orientation", "standard")

    client = entry.runtime_data.client

    try:
        kwargs = {}
        if label_size:
            kwargs["label_size"] = label_size
        if orientation:
            kwargs["orientation"] = orientation

        await client.async_print_text(
            text=datetime_text,
            font_size=font_size,
            font_family=font_family,
            alignment=alignment,
            line_spacing=line_spacing,
            **kwargs,
        )
        LOGGER.info("Datetime label printed successfully: %s (format: %s)", datetime_text, datetime_format)
    except Exception as exception:
        # Check if we should treat 400 errors as success
        treat_400_as_success = entry.options.get("treat_400_as_success", True)

        # Check if this is a 400 error
        # The exception may be wrapped in BrotherQLApiClientCommunicationError,
        # so we need to check the exception chain (__cause__)
        is_400_error = False

        # Check if exception is directly a ClientResponseError with status 400
        if isinstance(exception, aiohttp.ClientResponseError) and exception.status == 400:
            is_400_error = True
        # Check if exception is wrapped and the original cause is a ClientResponseError with status 400
        elif isinstance(exception, BrotherQLApiClientCommunicationError) and hasattr(exception, "__cause__"):
            original_exception = exception.__cause__
            if isinstance(original_exception, aiohttp.ClientResponseError) and original_exception.status == 400:
                is_400_error = True
        # Fallback: check any exception's cause for ClientResponseError with status 400
        elif hasattr(exception, "__cause__") and isinstance(exception.__cause__, aiohttp.ClientResponseError):
            original_exception = exception.__cause__
            if original_exception.status == 400:
                is_400_error = True

        if treat_400_as_success and is_400_error:
            LOGGER.info(
                "Received HTTP 400 error but treating as success (switch enabled): %s",
                datetime_text,
            )
            return

        LOGGER.exception("Failed to print datetime label: %s", exception)
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


async def async_handle_set_font_size(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the set_font_size service call.

    Sets the current font size for printing.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """

    font_size = call.data.get("font_size")
    if font_size is None:
        msg = "Font size parameter is required"
        raise ValueError(msg)

    # Update options with new font size
    options = dict(entry.options)
    options["current_font_size"] = int(font_size)

    hass.config_entries.async_update_entry(entry, options=options)
    LOGGER.info("Font size set to %s", font_size)

    # Trigger entity update
    await hass.config_entries.async_reload(entry.entry_id)


async def async_handle_reset_font_size(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the reset_font_size service call.

    Resets the current font size to the default value.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    # Get default font size from options or use constant
    default_font_size = entry.options.get("default_font_size", DEFAULT_FONT_SIZE)

    # Update options with default font size
    options = dict(entry.options)
    options["current_font_size"] = int(default_font_size)

    hass.config_entries.async_update_entry(entry, options=options)
    LOGGER.info("Font size reset to default: %s", default_font_size)

    # Trigger entity update
    await hass.config_entries.async_reload(entry.entry_id)


async def async_handle_set_font_size_preset(
    hass: HomeAssistant,
    entry: BrotherQLConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the set_font_size_preset service call.

    Sets the current font size to a preset value.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    preset = call.data.get("preset")
    if not preset:
        msg = "Preset parameter is required"
        raise ValueError(msg)

    # Determine font size based on preset
    preset_lower = str(preset).lower()
    if preset_lower == "goober":
        font_size = entry.options.get("goober_font_size", GOOBER_FONT_SIZE)
    elif preset_lower == "default":
        font_size = entry.options.get("default_font_size", DEFAULT_FONT_SIZE)
    else:
        # Try to parse as number
        try:
            font_size = int(preset)
        except ValueError as exc:
            msg = f"Invalid preset value: {preset}"
            raise ValueError(msg) from exc

        # Validate font size is within valid range (10-500)
        if font_size < 10 or font_size > 500:
            msg = f"Font size must be between 10 and 500, got {font_size}"
            raise ValueError(msg)

    # Update options with preset font size
    options = dict(entry.options)
    options["current_font_size"] = int(font_size)

    hass.config_entries.async_update_entry(entry, options=options)
    LOGGER.info("Font size set to preset '%s': %s", preset, font_size)

    # Trigger entity update
    await hass.config_entries.async_reload(entry.entry_id)
