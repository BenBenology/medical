import logging


LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging(level: str = "INFO") -> None:
    root_logger = logging.getLogger()
    normalized_level = getattr(logging, level.upper(), logging.INFO)

    if not root_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        root_logger.addHandler(handler)

    root_logger.setLevel(normalized_level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
