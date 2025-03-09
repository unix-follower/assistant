import os
import logging.config
import json

from app import APP_DIR
from app.logging.access_log import AccessLogFormatter
from app import constants


def configure_logging():
    with open(f"{APP_DIR}/config/logging.json", encoding=constants.UTF_8) as file:
        config = json.load(file)

        format_mode = os.environ.get("APP_LOG_FORMAT_MODE", "json")
        if "text" == format_mode:
            config["handlers"]["default"]["formatter"] = format_mode
            config["formatters"]["access"][
                "class"
            ] = f"{AccessLogFormatter.__module__}.{AccessLogFormatter.__name__}"

        logging.config.dictConfig(config)
