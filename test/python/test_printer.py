#!/usr/bin/env python3
"""
Unit tests for Brother MFC-L2750DW Printer Module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "python"))


class TestPrinterManager(unittest.TestCase):
    """Test cases for PrinterManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.printer_ip = "192.168.0.23"
        self.printer_name = "MFC-L2750DW"

    @patch("brw_printer.cups.Connection")
    def test_init(self, mock_cups):
        """Test PrinterManager initialization."""
        from brw_printer import PrinterManager

        pm = PrinterManager(printer_ip=self.printer_ip, printer_name=self.printer_name)

        self.assertEqual(pm.printer_ip, self.printer_ip)
        self.assertEqual(pm.printer_name, self.printer_name)
        self.assertIsNotNone(pm.conn)

    @patch("brw_printer.cups.Connection")
    def test_discover_printers(self, mock_cups):
        """Test printer discovery."""
        from brw_printer import PrinterManager

        # Mock CUPS response
        mock_cups.return_value.getPrinters.return_value = {
            "MFC-L2750DW": {"printer-uri-supported": "ipp://192.168.0.23/ipp/print"},
            "OtherPrinter": {"printer-uri-supported": "ipp://other/ipp/print"},
        }

        pm = PrinterManager()
        printers = pm.discover_printers()

        self.assertIsInstance(printers, dict)
        self.assertIn("MFC-L2750DW", printers)

    @patch("brw_printer.cups.Connection")
    def test_is_printer_available(self, mock_cups):
        """Test printer availability check."""
        from brw_printer import PrinterManager

        mock_cups.return_value.getPrinters.return_value = {
            "MFC-L2750DW": {"printer-uri-supported": "ipp://192.168.0.23/ipp/print"}
        }

        pm = PrinterManager()
        self.assertTrue(pm.is_printer_available())

    @patch("brw_printer.cups.Connection")
    def test_print_file(self, mock_cups):
        """Test printing a file."""
        from brw_printer import PrinterManager

        mock_cups.return_value.printFile.return_value = 123

        pm = PrinterManager()
        job_id = pm.print_file("/tmp/test.pdf")

        self.assertEqual(job_id, 123)
        mock_cups.return_value.printFile.assert_called_once()

    def test_print_options(self):
        """Test print options creation."""
        from brw_printer import PrintOptions

        options = PrintOptions.create_options(
            copies=2, media="letter", sides="two-sided-long-edge"
        )

        self.assertEqual(options["copies"], "2")
        self.assertEqual(options["media"], "letter")
        self.assertEqual(options["sides"], "two-sided-long-edge")


class TestPrintOptions(unittest.TestCase):
    """Test cases for PrintOptions class."""

    def test_create_options_defaults(self):
        """Test default options."""
        from brw_printer import PrintOptions

        options = PrintOptions.create_options()

        self.assertEqual(options["copies"], "1")
        self.assertEqual(options["media"], "letter")

    def test_media_constants(self):
        """Test media constants."""
        from brw_printer import PrintOptions

        self.assertEqual(PrintOptions.MEDIA_LETTER, "letter")
        self.assertEqual(PrintOptions.MEDIA_LEGAL, "legal")
        self.assertEqual(PrintOptions.MEDIA_A4, "a4")

    def test_sides_constants(self):
        """Test sides constants."""
        from brw_printer import PrintOptions

        self.assertEqual(PrintOptions.SIDES_ONE_SIDED, "one-sided")
        self.assertEqual(PrintOptions.SIDES_DUPLEX_LONG, "two-sided-long-edge")
        self.assertEqual(PrintOptions.SIDES_DUPLEX_SHORT, "two-sided-short-edge")


class TestDeviceConfiguration(unittest.TestCase):
    """Test device configuration values."""

    def test_default_ip(self):
        """Test default IP address."""
        from brw_printer import PrinterManager

        pm = PrinterManager()
        self.assertEqual(pm.printer_ip, "192.168.0.23")

    def test_default_name(self):
        """Test default printer name."""
        from brw_printer import PrinterManager

        pm = PrinterManager()
        self.assertEqual(pm.printer_name, "MFC-L2750DW")


if __name__ == "__main__":
    unittest.main()
