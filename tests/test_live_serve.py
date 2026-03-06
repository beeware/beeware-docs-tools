from unittest.mock import MagicMock, patch
import http.client
import time

import pytest
from beeware_docs_tools.live_serve_en import launch_browser

class TestLaunchBrowser:
    @patch("beeware_docs_tools.live_serve_en.webbrowser.open")
    @patch("beeware_docs_tools.live_serve_en.http.client.HTTPConnection")
    def test_launch_browser_success(self, mock_http_connection, mock_webbrowser_open):
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_conn.getresponse.return_value = mock_response
        mock_http_connection.return_value = mock_conn

        launch_browser(8000, timeout=1)

        mock_webbrowser_open.assert_called_once_with("http://localhost:8000/")
        mock_conn.request.assert_called_once_with("HEAD", "/")
        mock_conn.getresponse.assert_called_once()
        mock_conn.close.assert_called_once()


    @patch("beeware_docs_tools.live_serve_en.webbrowser.open")
    @patch("beeware_docs_tools.live_serve_en.http.client.HTTPConnection")
    @patch("beeware_docs_tools.live_serve_en.time.sleep")
    def test_launch_browser_connection_refused_then_success(self, mock_sleep, mock_http_connection, mock_webbrowser_open):
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        
        # First call raises OSError, second call succeeds
        mock_conn.getresponse.side_effect = [OSError(), mock_response]
        mock_http_connection.return_value = mock_conn

        launch_browser(8000, timeout=1)

        mock_webbrowser_open.assert_called_once_with("http://localhost:8000/")
        assert mock_conn.request.call_count == 2
        assert mock_conn.getresponse.call_count == 2
        # It should have slept once after the first failure
        mock_sleep.assert_called_once_with(0.1)

    @patch("beeware_docs_tools.live_serve_en.webbrowser.open")
    @patch("beeware_docs_tools.live_serve_en.http.client.HTTPConnection")
    @patch("beeware_docs_tools.live_serve_en.time.sleep")
    @patch("beeware_docs_tools.live_serve_en.time.time")
    def test_launch_browser_timeout(self, mock_time, mock_sleep, mock_http_connection, mock_webbrowser_open):
        mock_conn = MagicMock()
        mock_conn.getresponse.side_effect = OSError()
        mock_http_connection.return_value = mock_conn

        # Simulate time passing to trigger timeout immediately on second iteration
        mock_time.side_effect = [0, 0, 1]

        launch_browser(8000, timeout=1)

        mock_webbrowser_open.assert_not_called()
        mock_sleep.assert_called_once_with(0.1)

    @patch("beeware_docs_tools.live_serve_en.webbrowser.open")
    @patch("beeware_docs_tools.live_serve_en.http.client.HTTPConnection")
    @patch("beeware_docs_tools.live_serve_en.time.sleep")
    def test_launch_browser_server_error(self, mock_sleep, mock_http_connection, mock_webbrowser_open):
        mock_conn = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 503  # Server error, shouldn't break loop
        mock_success_response = MagicMock()
        mock_success_response.status = 200

        mock_conn.getresponse.side_effect = [mock_response, mock_success_response]
        mock_http_connection.return_value = mock_conn

        launch_browser(8000, timeout=1)

        mock_webbrowser_open.assert_called_once_with("http://localhost:8000/")
        assert mock_conn.request.call_count == 2
        assert mock_sleep.call_count == 0 # we no longer sleep on 503, only on exception

