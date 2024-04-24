import pytest
from unittest.mock import MagicMock, AsyncMock


@pytest.fixture(scope="function")
def mock_update(create_first_user):
    mock_update = AsyncMock()
    mock_update.effective_chat = create_first_user
    mock_update.effective_user = create_first_user
    mock_update.reply_text = AsyncMock()
    return mock_update


@pytest.fixture(scope="function")
def mock_context():
    mock_context = AsyncMock()
    mock_context.args = []
    return mock_context
