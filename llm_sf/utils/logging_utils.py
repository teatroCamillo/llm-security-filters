# logging_utils.py
import logging

# Configure a simple logger for filter-related events
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("security_filters")


def log_filter_event(event_type: str, details: str):
    logger.info(f"{event_type} - {details}")
