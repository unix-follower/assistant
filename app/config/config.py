import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from app import APP_DIR, constants


def get_profile():
    return os.environ.get("ENV", "prod")


def _get_env_file_paths():
    paths = [f"{APP_DIR}/config/.env"]
    match get_profile():
        case "local":
            paths.append(f"{APP_DIR}/config/local.env")
    return paths


class Settings(BaseSettings):
    app_name: str = "assistant"
    version: str = "1.0"

    model_config = SettingsConfigDict(
        extra="allow", env_file=_get_env_file_paths(), env_file_encoding=constants.UTF_8
    )
