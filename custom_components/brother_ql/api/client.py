"""
API Client for Brother QL Printer integration.

This module provides the API client for communicating with the brother_ql_web service.
It handles HTTP requests to the Docker-hosted web service for printing labels.

For more information on creating API clients:
https://developers.home-assistant.io/docs/api_lib_index
"""

from __future__ import annotations

import asyncio
import socket
from typing import Any

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
        font_family: str = "Arial",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Print a text label.

        Args:
            text: The text to print on the label.
            font_size: Font size (default: 100).
            font_family: Font family name (default: "Arial").
            **kwargs: Additional print parameters (label_size, orientation, etc.).

        Returns:
            A dictionary containing the print job response.

        Raises:
            BrotherQLApiClientAuthenticationError: If authentication fails.
            BrotherQLApiClientCommunicationError: If communication fails.
            BrotherQLApiClientError: For other API errors.

        """
        params = {
            "text": text,
            "font_size": font_size,
            "font_family": font_family,
            **kwargs,
        }
        return await self._api_wrapper(
            method="get",
            url=f"{self._base_url}/labeldesigner/api/print",
            params=params,
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
            url=f"{self._base_url}/api/print/image",
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
            url=f"{self._base_url}/api/print/barcode",
            params=params,
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: aiohttp.FormData | dict[str, Any] | None = None,
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
            data: Optional data to send in the request body (FormData or dict).
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
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
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
