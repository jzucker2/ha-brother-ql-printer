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

# Font size configuration defaults
DEFAULT_FONT_SIZE = 50
GOOBER_FONT_SIZE = 20
DEFAULT_CURRENT_FONT_SIZE = DEFAULT_FONT_SIZE

# Label size configuration defaults
DEFAULT_LABEL_SIZE = "17x54"

# Print text configuration defaults
DEFAULT_PRINT_TEXT = ""

# Datetime format configuration defaults
DEFAULT_DATETIME_FORMAT = "Date and Time"
