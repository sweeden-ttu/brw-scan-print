#!/usr/bin/env python3
"""
Brother MFC-L2750DW Printer Module

Provides CUPS/IPP printer functionality for the Brother MFC-L2750DW
network printer at 192.168.0.23
"""

import cups
import logging
from typing import Optional, Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrinterManager:
    """Manages printer connections and print jobs."""

    DEFAULT_PRINTER_IP = "192.168.0.23"
    DEFAULT_PRINTER_NAME = "MFC-L2750DW"

    def __init__(
        self,
        printer_ip: str = DEFAULT_PRINTER_IP,
        printer_name: str = DEFAULT_PRINTER_NAME,
    ):
        """
        Initialize printer manager.

        Args:
            printer_ip: IP address of the printer
            printer_name: CUPS printer name
        """
        self.printer_ip = printer_ip
        self.printer_name = printer_name
        self.conn = cups.Connection()
        logger.info(f"Initialized PrinterManager for {printer_name} at {printer_ip}")

    def discover_printers(self) -> Dict[str, Dict]:
        """
        Discover available printers.

        Returns:
            Dictionary of printer names to printer info
        """
        printers = self.conn.getPrinters()
        logger.info(f"Discovered {len(printers)} printers")
        return printers

    def is_printer_available(self) -> bool:
        """Check if the Brother printer is available."""
        printers = self.discover_printers()
        return self.printer_name in printers

    def print_file(
        self,
        file_path: str,
        title: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
    ) -> int:
        """
        Print a file to the Brother printer.

        Args:
            file_path: Path to the file to print
            title: Job title
            options: CUPS print options

        Returns:
            Job ID if successful

        Raises:
            cups.HTTPError: On HTTP errors
            cups.IPPError: On IPP errors
        """
        options = options or {}
        options.setdefault("copies", "1")
        options.setdefault("media", "letter")

        title = title or "Brother Print Job"

        logger.info(f"Printing {file_path} to {self.printer_name}")

        try:
            job_id = self.conn.printFile(self.printer_name, file_path, title, options)
            logger.info(f"Print job submitted: {job_id}")
            return job_id
        except cups.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except cups.IPPError as e:
            logger.error(f"IPP error: {e}")
            raise

    def get_job_status(self, job_id: int) -> Dict[str, Any]:
        """Get status of a print job."""
        return self.conn.getJobAttributes(job_id)

    def cancel_job(self, job_id: int) -> None:
        """Cancel a print job."""
        logger.info(f"Cancelling job {job_id}")
        self.conn.cancelJob(job_id)

    def get_printer_attributes(self) -> Dict[str, Any]:
        """Get printer attributes."""
        printers = self.discover_printers()
        return printers.get(self.printer_name, {})

    def get_supported_options(self) -> Dict[str, List[str]]:
        """Get supported printer options."""
        printer = self.get_printer_attributes()
        # Return supported media types, etc.
        return {
            "media": ["letter", "legal", "a4", "executive"],
            "sides": ["one-sided", "two-sided-long-edge", "two-sided-short-edge"],
            "quality": ["draft", "normal", "high"],
        }


class PrintOptions:
    """Print option constants and helpers."""

    MEDIA_LETTER = "letter"
    MEDIA_LEGAL = "legal"
    MEDIA_A4 = "a4"

    SIDES_ONE_SIDED = "one-sided"
    SIDES_DUPLEX_LONG = "two-sided-long-edge"
    SIDES_DUPLEX_SHORT = "two-sided-short-edge"

    QUALITY_DRAFT = "draft"
    QUALITY_NORMAL = "normal"
    QUALITY_HIGH = "high"

    SOURCE_AUTO = "auto"
    SOURCE_TRAY1 = "tray1"
    SOURCE_MANUAL = "manual"
    SOURCE_MPF = "mpf"

    @staticmethod
    def create_options(
        copies: int = 1,
        media: str = MEDIA_LETTER,
        sides: str = SIDES_ONE_SIDED,
        quality: str = QUALITY_NORMAL,
        source: str = SOURCE_TRAY1,
    ) -> Dict[str, str]:
        """Create standard print options."""
        return {
            "copies": str(copies),
            "media": media,
            "sides": sides,
            "quality": quality,
            "InputSlot": source,
        }


if __name__ == "__main__":
    pm = PrinterManager()
    printers = pm.discover_printers()
    print("Available printers:")
    for name, info in printers.items():
        print(f"  {name}: {info.get('printer-uri-supported', 'N/A')}")
