"""
Input sanitizers and normalizers.

Functions for cleaning and normalizing user inputs.

When adding many sanitizers, consider organizing by type:
- text.py: Text input sanitizers
- network.py: URL, host, port sanitizers
- identifiers.py: Device ID, serial number normalizers
"""

from __future__ import annotations

import re


def sanitize_username(username: str) -> str:
    """
    Sanitize username input.

    This function can be extended to normalize usernames (e.g., lowercase,
    trim whitespace) depending on API requirements.

    Args:
        username: Raw username input.

    Returns:
        Sanitized username.

    """
    return username.strip()


def sanitize_host(host: str) -> str:
    """
    Sanitize host input by removing protocol prefixes and trailing slashes.

    Removes common protocol prefixes (http://, https://) and trailing slashes
    that users might accidentally include when entering hostnames or IP addresses.

    Args:
        host: Raw host input (may include protocol prefix).

    Returns:
        Sanitized host (hostname or IP address only).

    Examples:
        >>> sanitize_host("http://localhost")
        'localhost'
        >>> sanitize_host("https://192.168.1.1/")
        '192.168.1.1'
        >>> sanitize_host("  example.com  ")
        'example.com'

    """
    # Strip whitespace
    host = host.strip()

    # Remove protocol prefixes (case-insensitive)
    host = re.sub(r"^https?://", "", host, flags=re.IGNORECASE)

    # Remove trailing slashes
    host = host.rstrip("/")

    # Remove any remaining whitespace
    return host.strip()


__all__ = [
    "sanitize_host",
    "sanitize_username",
]
