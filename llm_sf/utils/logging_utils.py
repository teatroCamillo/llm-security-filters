# logging_utils.py
import logging

# Configure a simple logger for filter-related events
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("security_filters")


def log_filter_event(event_type: str, details: str):
    """
    Logs a filtering event with a specific type and detail message.

    Intended for tracking actions taken by filters (e.g., blocking, allowing, sanitizing),
    and useful for monitoring, auditing, or debugging filter behavior.

    Args:
        event_type (str): A label for the type of event. Example values: 'BLOCK', 'ALLOW', 'SANITIZE'.
        details (str): A message containing additional context or metadata about the event.
    """
    logger.info(f"{event_type} - {details}")
