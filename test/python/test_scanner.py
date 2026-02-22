#!/usr/bin/env python3
"""
Unit tests for Brother MFC-L2750DW Scanner Module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))


class TestScannerManager(unittest.TestCase):
    """Test cases for ScannerManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scanner_ip = "192.168.0.23"

    @patch("brw_scanner.sane.init")
    @patch("brw_scanner.sane.get_devices")
    def test_init(self, mock_get_devices, mock_init):
        """Test ScannerManager initialization."""
        from brw_scanner import ScannerManager

        sm = ScannerManager(scanner_ip=self.scanner_ip)

        self.assertEqual(sm.scanner_ip, self.scanner_ip)

    @patch("brw_scanner.sane.init")
    @patch("brw_scanner.sane.get_devices")
    def test_discover_scanners(self, mock_get_devices, mock_init):
        """Test scanner discovery."""
        from brw_scanner import ScannerManager

        # Mock SANE device
        mock_dev = MagicMock()
        mock_dev.name = "brother5:net1"
        mock_dev.vendor = "Brother"
        mock_dev.model = "MFC-L2750DW"
        mock_dev.type = "flatbed"

        mock_get_devices.return_value = [mock_dev]

        sm = ScannerManager()
        scanners = sm.discover_scanners()

        self.assertIsInstance(scanners, list)

    @patch("brw_scanner.sane.init")
    @patch("brw_scanner.sane.get_devices")
    def test_find_brother_scanner(self, mock_get_devices, mock_init):
        """Test finding Brother scanner."""
        from brw_scanner import ScannerManager

        mock_dev = MagicMock()
        mock_dev.name = "brother5:net1"
        mock_dev.vendor = "Brother"
        mock_dev.model = "MFC-L2750DW"

        mock_get_devices.return_value = [mock_dev]

        sm = ScannerManager()
        scanner_name = sm.find_brother_scanner()

        self.assertEqual(scanner_name, "brother5:net1")


class TestScanOptions(unittest.TestCase):
    """Test cases for ScanOptions class."""

    def test_source_constants(self):
        """Test source constants."""
        from brw_scanner import ScanOptions

        self.assertEqual(ScanOptions.SOURCE_FLATBED, "Flatbed")
        self.assertEqual(ScanOptions.SOURCE_ADF, "ADF")
        self.assertEqual(ScanOptions.SOURCE_ADF_DUPLEX, "ADF Duplex")

    def test_dpi_constants(self):
        """Test DPI constants."""
        from brw_scanner import ScanOptions

        self.assertEqual(ScanOptions.DPI_150, 150)
        self.assertEqual(ScanOptions.DPI_300, 300)
        self.assertEqual(ScanOptions.DPI_600, 600)

    def test_format_constants(self):
        """Test format constants."""
        from brw_scanner import ScanOptions

        self.assertEqual(ScanOptions.FORMAT_PDF, "PDF")
        self.assertEqual(ScanOptions.FORMAT_JPEG, "JPEG")
        self.assertEqual(ScanOptions.FORMAT_PNG, "PNG")
        self.assertEqual(ScanOptions.FORMAT_TIFF, "TIFF")

    def test_paper_size_constants(self):
        """Test paper size constants."""
        from brw_scanner import ScanOptions

        self.assertEqual(ScanOptions.LETTER_WIDTH, 215.9)
        self.assertEqual(ScanOptions.LETTER_HEIGHT, 279.4)
        self.assertEqual(ScanOptions.LEGAL_WIDTH, 215.9)
        self.assertEqual(ScanOptions.LEGAL_HEIGHT, 355.6)

    def test_create_options(self):
        """Test options creation."""
        from brw_scanner import ScanOptions

        options = ScanOptions.create_options(
            source=ScanOptions.SOURCE_ADF,
            dpi=ScanOptions.DPI_300,
            format=ScanOptions.FORMAT_PDF,
        )

        self.assertEqual(options["source"], "ADF")
        self.assertEqual(options["resolution"], 300)
        self.assertEqual(options["format"], "PDF")


class TestDeviceConfiguration(unittest.TestCase):
    """Test device configuration values."""

    def test_default_ip(self):
        """Test default IP address."""
        from brw_scanner import ScannerManager

        sm = ScannerManager()
        self.assertEqual(sm.scanner_ip, "192.168.0.23")


if __name__ == "__main__":
    unittest.main()
