"""
logging_utils.py
Centralized logging example for demonstration
"""

import logging

# Configure a simple logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("security_filters")

def log_filter_event(event_type: str, details: str):
    """
    event_type could be: 'BLOCK', 'SANITIZE', 'ALLOW', etc.
    details: some relevant info
    """
    logger.info(f"{event_type} - {details}")
