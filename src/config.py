"""Configuration utilities for server integrations.

This module loads environment variables to configure
connections for the Model Context Protocol server integrations.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class IntegrationsConfig:
    """Configuration values for server integrations."""

    notion_api_key: str = field(default_factory=lambda: os.getenv("NOTION_API_KEY", ""))
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    slack_token: str = field(default_factory=lambda: os.getenv("SLACK_TOKEN", ""))
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))


def load_integrations_config() -> IntegrationsConfig:
    """Return a populated :class:`IntegrationsConfig` instance."""

    return IntegrationsConfig()
