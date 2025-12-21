"""Constants for Brother QL Printer integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

# Integration metadata
DOMAIN = "brother_ql"
ATTRIBUTION = "Data provided by Brother QL Web Service"

# Platform parallel updates - applied to all platforms
PARALLEL_UPDATES = 1

# Default configuration values
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8013
DEFAULT_UPDATE_INTERVAL_SECONDS = 30
