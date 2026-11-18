"""Configuration loader for Xinoobie Photobooth.

Loading order (first match wins):
  1. Environment variables (APP_*, DB_*, etc.)
  2. config/config.json (or config/config.yaml)
  3. Default values in code
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

try:
    import toml
    _HAVE_TOML = True
except ImportError:
    _HAVE_TOML = False

try:
    import yaml
    _HAVE_YAML = True
except ImportError:
    _HAVE_YAML = False

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_NAME = "Xinoobie Photobooth"
APP_VERSION = "0.1.0"
DEFAULT_DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / APP_NAME


def _env_path(prefix: str, name: str, default: str) -> str:
    """Get a value from environment variable, fallback to default."""
    env_name = f"{prefix}_{name}".upper()
    val = os.environ.get(env_name)
    return val if val is not None else default


def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return bool(value) if value is not None else default


def _as_int(value: Any, default: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return int(value) if value is not None else default


def _as_float(value: Any, default: float) -> float:
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return default
    return float(value) if value is not None else default


class Config:
    """Application configuration singleton."""

    _instance: "Config" | None = None

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._load_files()
        self._apply_env_overrides()

    @classmethod
    def instance(cls) -> "Config":
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def _load_files(self) -> None:
        # Try config.yaml
        for config_file in ["config.yaml", "config.yml", "config.toml", "config.json"]:
            config_path = BASE_DIR / "config" / config_file
            if config_path.exists():
                self._load_file(config_path)
                break
        else:
            self._load_file(BASE_DIR / "config.json")

    def _load_file(self, path: Path) -> None:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"[config] Failed to read {path}: {exc}")
            return

        if path.suffix in (".yaml", ".yml"):
            if not _HAVE_YAML:
                print("[config] PyYAML not installed; ignoring config.yaml")
                return
            try:
                self._data.update(yaml.safe_load(content) or {})
            except Exception as exc:
                print(f"[config] YAML parse error in {path}: {exc}")
        elif path.suffix == ".toml":
            if not _HAVE_TOML:
                print("[config] tomli not installed; ignoring config.toml")
                return
            try:
                self._data.update(toml.loads(content))
            except Exception as exc:
                print(f"[config] TOML parse error in {path}: {exc}")
        elif path.suffix == ".json":
            try:
                self._data.update(json.loads(content))
            except Exception as exc:
                print(f"[config] JSON parse error in {path}: {exc}")

    def _apply_env_overrides(self) -> None:
        """Override config with environment variables (highest priority)."""
        env_map = {
            "app_name": ("APP_NAME", self.app_name),
            "language": ("APP_LANGUAGE", self.language),
            "data_dir": ("DATA_DIR", str(self.data_dir)),
            "kiosk_mode": ("KIOSK_MODE", self.kiosk_mode),
            "auto_start": ("AUTO_START", self.auto_start),
        }
        for key, (env_name, default) in env_map.items():
            if env_name in os.environ:
                self._data[key] = os.environ[env_name]

    @property
    def app_name(self) -> str:
        app = self._data.get("app", {})
        if isinstance(app, dict):
            return str(app.get("name", self._data.get("app_name", APP_NAME)))
        return str(self._data.get("app_name", APP_NAME))

    @property
    def app_version(self) -> str:
        app = self._data.get("app", {})
        if isinstance(app, dict):
            return str(app.get("version", self._data.get("app_version", APP_VERSION)))
        return str(self._data.get("app_version", APP_VERSION))

    @property
    def language(self) -> str:
        return str(self._data.get("language", "id"))

    @property
    def kiosk_mode(self) -> bool:
        return _as_bool(self._data.get("kiosk_mode"), False)

    @property
    def auto_start(self) -> bool:
        return _as_bool(self._data.get("auto_start"), False)

    @property
    def data_dir(self) -> Path:
        raw = self._data.get("data_dir", str(DEFAULT_DATA_DIR))
        return Path(raw).expanduser().resolve()

    @property
    def storage_dir(self) -> Path:
        """Permanent storage for session photos."""
        dir_path = self.data_dir / "storage"
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @property
    def temp_dir(self) -> Path:
        dir_path = self.data_dir / "temp"
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @property
    def backup_dir(self) -> Path:
        dir_path = self.data_dir / "backup"
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @property
    def log_dir(self) -> Path:
        dir_path = self.data_dir / "logs"
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @property
    def db_path(self) -> Path:
        return self.data_dir / "xinoobie.db"

    @property
    def camera_profiles(self) -> dict[str, Any]:
        return self._data.get("camera", {}).get("profiles", {})

    @property
    def printer_profiles(self) -> dict[str, Any]:
        return self._data.get("printer", {}).get("profiles", {})

    @property
    def session_defaults(self) -> dict[str, Any]:
        return self._data.get("session", {})

    @property
    def payment_settings(self) -> dict[str, Any]:
        return self._data.get("payment", {})

    @property
    def theme(self) -> str:
        ui = self._data.get("ui", {})
        return str(ui.get("theme", self._data.get("theme", "dark")))

    @property
    def window_width(self) -> int:
        display = self._data.get("display", {})
        return _as_int(display.get("window_width"), 1920)

    @property
    def window_height(self) -> int:
        display = self._data.get("display", {})
        return _as_int(display.get("window_height"), 1080)

    @property
    def dpi(self) -> int:
        display = self._data.get("display", {})
        return _as_int(display.get("dpi"), 96)

    @property
    def fullscreen(self) -> bool:
        display = self._data.get("display", {})
        return _as_bool(display.get("fullscreen"), self.kiosk_mode)

    @property
    def exception_handler(self):
        from app_core.error_handler import handle_exception
        return handle_exception

    def as_dict(self) -> dict[str, Any]:
        return dict(self._data)


# Module-level singleton for convenience
config = Config.instance()

__all__ = ["Config", "config", "APP_NAME", "APP_VERSION"]
