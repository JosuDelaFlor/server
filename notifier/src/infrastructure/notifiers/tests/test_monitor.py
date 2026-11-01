import pytest
from unittest.mock import Mock, call
from src.core.monitor import TunnelMonitor

@pytest.fixture
def mock_provider():
    return Mock()

@pytest.fixture
def mock_notifier():
    return Mock()

def test_monitor_detects_new_url_and_notifies(mock_provider, mock_notifier):
    # Arrange
    mock_provider.get_tunnel_url.return_value = "tcp://0.tcp.eu.ngrok.io:12345"
    monitor = TunnelMonitor(provider=mock_provider, notifier=mock_notifier, interval=1)
    
    # Act
    monitor._check_tunnel()
    
    # Assert
    mock_notifier.notify.assert_called_once()
    args, _ = mock_notifier.notify.call_args
    assert "0.tcp.eu.ngrok.io:12345" in args[0]
    assert monitor.last_url == "tcp://0.tcp.eu.ngrok.io:12345"

def test_monitor_ignores_same_url(mock_provider, mock_notifier):
    # Arrange
    mock_provider.get_tunnel_url.return_value = "tcp://0.tcp.eu.ngrok.io:12345"
    monitor = TunnelMonitor(provider=mock_provider, notifier=mock_notifier, interval=1)
    monitor.last_url = "tcp://0.tcp.eu.ngrok.io:12345"
    
    # Act
    monitor._check_tunnel()
    
    # Assert
    mock_notifier.notify.assert_not_called()