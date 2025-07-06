import logging

class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "/health" not in record.getMessage()