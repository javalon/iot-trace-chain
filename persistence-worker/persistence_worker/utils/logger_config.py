import datetime
import json
import logging

import json_log_formatter


class CustomJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra["component"] = record.name
        extra["level"] = record.levelname
        extra["message"] = message
        extra["time"] = datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc).isoformat()
        return extra

    def format(self, record):
        json_record = self.json_record(record.getMessage(), {}, record)
        return json.dumps(json_record, ensure_ascii=False)


def setup_logger(name):
    formatter = CustomJSONFormatter()
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(json_handler)
    logger.propagate = False

    return logger
