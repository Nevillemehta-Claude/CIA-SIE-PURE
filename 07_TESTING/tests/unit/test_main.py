"""
Tests for CIA-SIE Main Entry Point
==================================

Unit tests for main application entry point.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import logging


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_configures_basic_logging(self):
        """Test setup_logging configures basic logging."""
        from cia_sie.main import setup_logging

        mock_settings = Mock()
        mock_settings.log_level = "INFO"
        mock_settings.log_file = None

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('logging.basicConfig') as mock_basic_config:
            setup_logging()

        mock_basic_config.assert_called_once()
        call_kwargs = mock_basic_config.call_args[1]
        assert call_kwargs['level'] == logging.INFO

    def test_setup_logging_with_file_handler(self):
        """Test setup_logging adds file handler when configured."""
        from cia_sie.main import setup_logging

        mock_settings = Mock()
        mock_settings.log_level = "DEBUG"
        mock_settings.log_file = "/tmp/test.log"

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('logging.basicConfig'), \
             patch('logging.FileHandler') as mock_file_handler, \
             patch('logging.getLogger') as mock_get_logger:

            mock_handler_instance = Mock()
            mock_file_handler.return_value = mock_handler_instance

            mock_root_logger = Mock()
            mock_get_logger.return_value = mock_root_logger

            setup_logging()

        mock_file_handler.assert_called_once_with("/tmp/test.log")
        mock_root_logger.addHandler.assert_called_once_with(mock_handler_instance)

    def test_setup_logging_without_file_handler(self):
        """Test setup_logging skips file handler when not configured."""
        from cia_sie.main import setup_logging

        mock_settings = Mock()
        mock_settings.log_level = "INFO"
        mock_settings.log_file = None  # No file configured

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('logging.basicConfig'), \
             patch('logging.FileHandler') as mock_file_handler:
            setup_logging()

        mock_file_handler.assert_not_called()

    def test_setup_logging_uppercase_conversion(self):
        """Test setup_logging converts log level to uppercase."""
        from cia_sie.main import setup_logging

        mock_settings = Mock()
        mock_settings.log_level = "warning"  # lowercase
        mock_settings.log_file = None

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('logging.basicConfig') as mock_basic_config:
            setup_logging()

        call_kwargs = mock_basic_config.call_args[1]
        assert call_kwargs['level'] == logging.WARNING


class TestMain:
    """Tests for main function."""

    def test_main_starts_uvicorn(self):
        """Test main starts uvicorn server."""
        from cia_sie.main import main

        mock_settings = Mock()
        mock_settings.app_name = "CIA-SIE"
        mock_settings.app_version = "1.0.0"
        mock_settings.debug = False
        mock_settings.api_host = "0.0.0.0"
        mock_settings.api_port = 8000
        mock_settings.log_level = "INFO"
        mock_settings.log_file = None

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('cia_sie.main.setup_logging'), \
             patch('uvicorn.run') as mock_uvicorn:
            main()

        mock_uvicorn.assert_called_once()
        call_args = mock_uvicorn.call_args
        assert call_args[0][0] == "cia_sie.api.app:app"
        assert call_args[1]['host'] == "0.0.0.0"
        assert call_args[1]['port'] == 8000
        assert call_args[1]['reload'] is False

    def test_main_enables_reload_in_debug_mode(self):
        """Test main enables reload when debug is True."""
        from cia_sie.main import main

        mock_settings = Mock()
        mock_settings.app_name = "CIA-SIE"
        mock_settings.app_version = "1.0.0"
        mock_settings.debug = True
        mock_settings.api_host = "127.0.0.1"
        mock_settings.api_port = 3000
        mock_settings.log_level = "debug"
        mock_settings.log_file = None

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('cia_sie.main.setup_logging'), \
             patch('uvicorn.run') as mock_uvicorn:
            main()

        call_kwargs = mock_uvicorn.call_args[1]
        assert call_kwargs['reload'] is True
        assert call_kwargs['log_level'] == "debug"

    def test_main_logs_startup_info(self):
        """Test main logs startup information."""
        from cia_sie.main import main

        mock_settings = Mock()
        mock_settings.app_name = "CIA-SIE"
        mock_settings.app_version = "2.0.0"
        mock_settings.debug = True
        mock_settings.api_host = "0.0.0.0"
        mock_settings.api_port = 8000
        mock_settings.log_level = "INFO"
        mock_settings.log_file = None

        with patch('cia_sie.main.get_settings', return_value=mock_settings), \
             patch('cia_sie.main.setup_logging'), \
             patch('uvicorn.run'), \
             patch('logging.getLogger') as mock_get_logger:

            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            main()

        # Verify info calls were made
        assert mock_logger.info.call_count >= 2
        # Check that app name/version was logged
        info_calls = [str(call) for call in mock_logger.info.call_args_list]
        assert any("CIA-SIE" in str(call) for call in info_calls)


class TestMainConstitutionalCompliance:
    """Constitutional compliance tests for main module."""

    @pytest.mark.constitutional
    def test_no_recommendation_generation_in_main(self):
        """CRITICAL: Main module must not generate recommendations."""
        import cia_sie.main as main_module

        prohibited_methods = [
            'recommend', 'suggest', 'advise', 'compute_score',
            'aggregate_signals', 'calculate_confidence',
        ]

        for method in prohibited_methods:
            assert not hasattr(main_module, method), \
                f"CONSTITUTIONAL VIOLATION: main module has {method}"
