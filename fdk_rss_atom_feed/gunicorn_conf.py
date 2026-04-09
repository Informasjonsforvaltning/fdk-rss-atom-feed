import logging
import sys
from typing import Any

from gunicorn import glogging
from pythonjsonlogger import json

# Gunicorn config variables
loglevel = "INFO"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"  # noqa: S108
graceful_timeout = 120
timeout = 120
keepalive = 5
threads = 3


class StackdriverJsonFormatter(json.JsonFormatter, object):
    """JSON log formatter."""

    def __init__(
        self: Any,
        fmt: str = "%(levelname) %(message)",
        style: str = "%",
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Init json-logger."""
        json.JsonFormatter.__init__(self, *args, fmt=fmt, **kwargs)

    def process_log_record(self: Any, log_record: Any) -> Any:
        """Process log record to a json-format compatible with Stackdriver."""
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        log_record["serviceContext"] = {"service": "fdk-organization-bff"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


# Override the logger to remove health check from the access log and format logs as json
class CustomGunicornLogger(glogging.Logger):
    """Custom Gunicorn Logger class."""

    def setup(self: Any, cfg: Any) -> None:
        """Set up function."""
        super().setup(cfg)

        access_logger = logging.getLogger("gunicorn.access")
        access_logger.addFilter(LivezFilter())
        access_logger.addFilter(ReadyzFilter())

        root_logger = logging.getLogger()
        root_logger.setLevel(loglevel)

        other_loggers = [
            "gunicorn",
            "gunicorn.error",
            "gunicorn.http",
            "gunicorn.http.wsgi",
        ]
        loggers = [logging.getLogger(name) for name in other_loggers]
        loggers.append(root_logger)
        loggers.append(access_logger)

        json_handler = logging.StreamHandler(sys.stdout)
        json_handler.setFormatter(StackdriverJsonFormatter())

        for logger in loggers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger.addHandler(json_handler)


class LivezFilter(logging.Filter):
    """Custom Livez Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /livez" not in record.getMessage()


class ReadyzFilter(logging.Filter):
    """Custom Readyz Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /readyz" not in record.getMessage()


logger_class = CustomGunicornLogger
