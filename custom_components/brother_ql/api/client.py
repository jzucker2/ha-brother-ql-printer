"""
API Client for Brother QL Printer integration.

This module provides the API client for communicating with the brother_ql_web service.
It handles HTTP requests to the Docker-hosted web service for printing labels.

For more information on creating API clients:
https://developers.home-assistant.io/docs/api_lib_index
"""

from __future__ import annotations

import asyncio
import json
import socket
from typing import Any
from urllib.parse import urlencode

import aiohttp


class BrotherQLApiClientError(Exception):
    """Base exception to indicate a general API error."""


class BrotherQLApiClientCommunicationError(BrotherQLApiClientError):
    """Exception to indicate a communication error with the API."""


class BrotherQLApiClientAuthenticationError(BrotherQLApiClientError):
    """Exception to indicate an authentication error with the API."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """
    Verify that the API response is valid.

    Raises appropriate exceptions for authentication and HTTP errors.

    Args:
        response: The aiohttp ClientResponse to verify.

    Raises:
        BrotherQLApiClientAuthenticationError: For 401/403 errors.
        aiohttp.ClientResponseError: For other HTTP errors.

    """
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise BrotherQLApiClientAuthenticationError(msg)
    response.raise_for_status()


class BrotherQLApiClient:
    """
    API Client for Brother QL Printer integration.

    This client communicates with the brother_ql_web Docker service to:
    - Get printer status
    - Print labels (text, images, barcodes, QR codes)
    - Manage printer configuration

    The brother_ql_web service typically runs on port 8013 and provides
    a REST API for label printing operations.

    Attributes:
        _host: The hostname or IP address of the brother_ql_web service.
        _port: The port number of the brother_ql_web service.
        _session: The aiohttp ClientSession for making requests.
        _base_url: The base URL for API requests.

    """

    def __init__(
        self,
        host: str,
        port: int,
        session: aiohttp.ClientSession,
    ) -> None:
        """
        Initialize the API Client with connection details.

        Args:
            host: The hostname or IP address of the brother_ql_web service.
            port: The port number of the brother_ql_web service.
            session: The aiohttp ClientSession to use for requests.

        """
        self._host = host
        self._port = int(port)  # Cast to int in case NumberSelector returns float
        self._session = session
        self._base_url = f"http://{host}:{self._port}"

    async def async_get_status(self) -> dict[str, Any]:
        """
        Get printer status from the API.

        Returns:
            A dictionary containing the printer status information.

        Raises:
            BrotherQLApiClientAuthenticationError: If authentication fails.
            BrotherQLApiClientCommunicationError: If communication fails.
            BrotherQLApiClientError: For other API errors.

        """
        return await self._api_wrapper(
            method="get",
            url=f"{self._base_url}/labeldesigner/api/printer_status",
        )

    async def async_print_text(
        self,
        text: str,
        font_size: int = 100,
        font_family: str = "DejaVu Math TeX Gyre,Regular",
        alignment: str = "center",
        line_spacing: str = "100",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Print a text label.

        Args:
            text: The text to print on the label.
            font_size: Font size (default: 100).
            font_family: Font family name (default: "DejaVu Math TeX Gyre,Regular").
            alignment: Text alignment (default: "center").
            line_spacing: Line spacing (default: "100").
            **kwargs: Additional print parameters (label_size, orientation, etc.).

        Returns:
            A dictionary containing the print job response.

        Raises:
            BrotherQLApiClientAuthenticationError: If authentication fails.
            BrotherQLApiClientCommunicationError: If communication fails.
            BrotherQLApiClientError: For other API errors.

        """
        # Format text as JSON array matching brother_ql_web API format
        text_object = {
            "font": font_family,
            "size": str(font_size),
            "inverted": False,
            "todo": False,
            "align": alignment,
            "line_spacing": line_spacing,
            "color": "black",
            "text": text,
        }
        formatted_text = json.dumps([text_object])

        # Build form data as dict (will be encoded as application/x-www-form-urlencoded)
        data: dict[str, Any] = {
            "text": formatted_text,
            "label_size": kwargs.get("label_size", "17x54"),
            "orientation": kwargs.get("orientation", "standard"),
            "margin_top": kwargs.get("margin_top", "24"),
            "margin_bottom": kwargs.get("margin_bottom", "24"),
            "margin_left": kwargs.get("margin_left", "35"),
            "margin_right": kwargs.get("margin_right", "35"),
            "print_type": kwargs.get("print_type", "text"),
            "barcode_type": kwargs.get("barcode_type", "QR"),
            "qrcode_size": kwargs.get("qrcode_size", "10"),
            "qrcode_correction": kwargs.get("qrcode_correction", "L"),
            "image_bw_threshold": kwargs.get("image_bw_threshold", "70"),
            "image_mode": kwargs.get("image_mode", "grayscale"),
            "image_fit": kwargs.get("image_fit", "1"),
            "print_count": kwargs.get("print_count", "1"),
            "log_level": kwargs.get("log_level", "WARNING"),
            "cut_once": kwargs.get("cut_once", "0"),
            "border_thickness": kwargs.get("border_thickness", "0"),
            "border_roundness": kwargs.get("border_roundness", "0"),
            "border_distance_x": kwargs.get("border_distance_x", "0"),
            "border_distance_y": kwargs.get("border_distance_y", "0"),
            "high_res": kwargs.get("high_res", "0"),
            "image_scaling_factor": kwargs.get("image_scaling_factor", "100"),
            "image_rotation": kwargs.get("image_rotation", "0"),
        }

        # Encode data as URL-encoded string (matching Node-RED URLSearchParams.toString())
        encoded_data = urlencode(data, doseq=False)

        # Set Content-Type header for form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "keep-alive",
            "Accept": "*/*",
        }

        return await self._api_wrapper(
            method="post",
            url=f"{self._base_url}/labeldesigner/api/print",
            data=encoded_data,
            headers=headers,
        )

    async def async_print_image(
        self,
        image_data: bytes,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Print an image label.

        Args:
            image_data: The image data as bytes.
            **kwargs: Additional print parameters (label_size, orientation, etc.).

        Returns:
            A dictionary containing the print job response.

        Raises:
            BrotherQLApiClientAuthenticationError: If authentication fails.
            BrotherQLApiClientCommunicationError: If communication fails.
            BrotherQLApiClientError: For other API errors.

        """
        data = aiohttp.FormData()
        data.add_field("image", image_data, filename="label.png", content_type="image/png")
        for key, value in kwargs.items():
            data.add_field(key, str(value))

        return await self._api_wrapper(
            method="post",
            url=f"{self._base_url}/labeldesigner/api/print/image",
            data=data,
        )

    async def async_print_barcode(
        self,
        barcode_data: str,
        barcode_type: str = "CODE128",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Print a barcode label.

        Args:
            barcode_data: The data to encode in the barcode.
            barcode_type: The barcode type (CODE128, QR, EAN13, etc.).
            **kwargs: Additional print parameters.

        Returns:
            A dictionary containing the print job response.

        Raises:
            BrotherQLApiClientAuthenticationError: If authentication fails.
            BrotherQLApiClientCommunicationError: If communication fails.
            BrotherQLApiClientError: For other API errors.

        """
        params = {
            "data": barcode_data,
            "type": barcode_type,
            **kwargs,
        }
        return await self._api_wrapper(
            method="get",
            url=f"{self._base_url}/labeldesigner/api/print/barcode",
            params=params,
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: aiohttp.FormData | dict[str, Any] | str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """
        Wrapper for API requests with error handling.

        This method handles all HTTP requests and translates exceptions
        into integration-specific exceptions.

        Args:
            method: The HTTP method (get, post, patch, etc.).
            url: The URL to request.
            data: Optional data to send in the request body (FormData, dict, or str).
            params: Optional query parameters.
            headers: Optional headers to include in the request.

        Returns:
            The JSON response from the API, or None if response is empty.

        Raises:
            BrotherQLApiClientAuthenticationError: If authentication fails.
            BrotherQLApiClientCommunicationError: If communication fails.
            BrotherQLApiClientError: For other API errors.

        """
        try:
            async with asyncio.timeout(30):
                # When using FormData, aiohttp automatically sets Content-Type to multipart/form-data
                # When using dict, aiohttp will encode as application/x-www-form-urlencoded
                # If headers are provided with Content-Type, use them (for form-urlencoded)
                request_headers = headers
                if isinstance(data, aiohttp.FormData) and headers:
                    # If FormData is used, merge headers but don't override Content-Type
                    request_headers = {**headers}
                    if "Content-Type" in request_headers:
                        # Remove Content-Type from headers - let FormData set it with boundary
                        del request_headers["Content-Type"]

                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    data=data,
                    params=params,
                )
                _verify_response_or_raise(response)
                # Handle empty responses
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return await response.json()
                # For non-JSON responses, return text or None
                text = await response.text()
                return {"status": "success", "message": text} if text else None

        except BrotherQLApiClientAuthenticationError:
            # Re-raise authentication errors directly so coordinator can handle them
            raise
        except BrotherQLApiClientCommunicationError:
            # Re-raise communication errors directly
            raise
        except TimeoutError as exception:
            msg = f"Timeout error communicating with printer - {exception}"
            raise BrotherQLApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error communicating with printer - {exception}"
            raise BrotherQLApiClientCommunicationError(msg) from exception
        except Exception as exception:
            msg = f"Unexpected error - {exception}"
            raise BrotherQLApiClientError(msg) from exception
