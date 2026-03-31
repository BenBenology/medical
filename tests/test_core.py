import logging

from app.core.config import Settings
from app.core.logging import configure_logging, get_logger


def test_settings_uses_defaults_when_env_not_provided() -> None:
    settings = Settings()

    assert settings.app_name == "Medical Consultation System"
    assert settings.app_env == "dev"
    assert settings.log_level == "INFO"


def test_settings_can_be_overridden_by_constructor_values() -> None:
    settings = Settings(app_env="test", log_level="DEBUG")

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"


def test_configure_logging_sets_root_level() -> None:
    configure_logging("DEBUG")

    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG


def test_get_logger_returns_same_named_logger_without_duplicate_handlers() -> None:
    configure_logging("INFO")

    logger = get_logger("medical.test")
    same_logger = get_logger("medical.test")

    assert logger is same_logger
    assert logger.name == "medical.test"
