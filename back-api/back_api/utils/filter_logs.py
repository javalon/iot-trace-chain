import logging

class HealthCheckFilter(logging.Filter):
    """
    Custom filter to silence logs for health check endpoint.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        # Filter out logs that contain the health check path
        return "/health" not in record.getMessage()