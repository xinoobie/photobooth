"""Customer Interface package — PySide6 touchscreen UI shell.

Exports core classes for use by applications:
- Config: application configuration singleton
- ScreenId: screen identifier constants
- BaseScreen: base class for all customer screens
"""
from __future__ import annotations

from app_core.config import Config

# Re-export screen base class and identifiers
# (screens/__init__.py imports PySide6 at module level, so we lazy-import)
try:
    from .screens import BaseScreen, ScreenId
except ImportError:
    # PySide6 not installed — screens not available
    BaseScreen = None
    ScreenId = None

config = Config.instance()

__all__ = ["Config", "BaseScreen", "ScreenId", "config"]
