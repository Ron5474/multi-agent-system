import pytest
import sys
from unittest.mock import patch, MagicMock, AsyncMock


def pytest_configure(config):
    patcher = patch("openai.OpenAI", MagicMock())
    patcher.start()
