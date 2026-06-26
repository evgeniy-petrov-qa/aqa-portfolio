import json

from pathlib import Path
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings


class URLs(BaseModel):
    """Test environment URLs."""

    qa_playground: str
    firstplaidypusbank: str
    nomads: str


    @field_validator("*", mode="before")
    @classmethod
    def must_be_http(cls, v: str) -> str:
        """Validates that all fields are valid HTTP URLs."""
        if not v.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL: {v}")
        return v


class Settings(BaseSettings):
    """Global project settings."""

    CONFIGS_PATH: Path = Path(__file__).parent.parent / "configs"
    DOWNLOAD_PATH: Path = Path(__file__).parent.parent / "downloads"
    SCREENS_PATH: Path = Path(__file__).parent.parent / "screenshots"

    JS_LOG_IGNORE_LIST: list[str] = [
        "www.googleadservices.com",
        "stats.g.doubleclick.net",
        "www.facebook.com",
        "cm.g.doubleclick.net",
    ]

    def load_urls(self, environ: str) -> URLs:
        """Loads URLs from the environment config file.

        :param environ: environment name, matches a folder in configs/
        :raises FileNotFoundError: if config file is not found
        :return: validated environment URLs
        """
        config_file = self.CONFIGS_PATH / f"{environ}_cfg" / f"{environ}_common_cfg.json"

        if not config_file.exists():
            raise FileNotFoundError(
                f"Config file not found: {config_file}\n"
                f"Available environments: {[p.name for p in self.CONFIGS_PATH.iterdir()]}"
            )

        data = json.loads(config_file.read_text(encoding="utf-8"))
        return URLs(**data)


settings = Settings()