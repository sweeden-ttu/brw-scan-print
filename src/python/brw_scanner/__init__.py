#!/usr/bin/env python3
"""
Brother MFC-L2750DW Scanner Module

Provides SANE scanner functionality for the Brother MFC-L2750DW
network scanner at 192.168.0.23
"""

import sane
import logging
from typing import Optional, List, Dict, Any, Tuple
from io import BytesIO
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScannerManager:
    """Manages scanner connections and scanning operations."""

    DEFAULT_SCANNER_IP = "192.168.0.23"

    # Scanner sources
    SOURCE_FLATBED = "Flatbed"
    SOURCE_ADF = "ADF"
    SOURCE_ADF_DUPLEX = "ADF Duplex"

    # Resolution options
    DPI_150 = 150
    DPI_300 = 300
    DPI_600 = 600

    def __init__(self, scanner_ip: str = DEFAULT_SCANNER_IP):
        """
        Initialize scanner manager.

        Args:
            scanner_ip: IP address of the scanner
        """
        self.scanner_ip = scanner_ip
        self._scanner = None
        self._initialized = False
        logger.info(f"Initialized ScannerManager for scanner at {scanner_ip}")

    def _ensure_initialized(self):
        """Ensure SANE is initialized."""
        if not self._initialized:
            sane.init()
            self._initialized = True

    def discover_scanners(self) -> List[Dict[str, str]]:
        """
        Discover available scanners.

        Returns:
            List of scanner info dictionaries
        """
        self._ensure_initialized()
        devices = sane.get_devices()

        scanners = []
        for dev in devices:
            scanners.append(
                {
                    "name": dev.name,
                    "vendor": dev.vendor,
                    "model": dev.model,
                    "type": dev.type,
                }
            )

        logger.info(f"Discovered {len(scanners)} scanners")
        return scanners

    def find_brother_scanner(self) -> Optional[str]:
        """Find the Brother MFC-L2750DW scanner."""
        devices = self.discover_scanners()

        for dev in devices:
            name = dev.get("name", "")
            vendor = dev.get("vendor", "")
            model = dev.get("model", "")

            # Look for Brother device
            if "brother" in vendor.lower() or "brother" in model.lower():
                logger.info(f"Found Brother scanner: {name}")
                return name
            if "MFC" in model or "L2750" in model:
                logger.info(f"Found Brother scanner: {name}")
                return name

        return None

    def open_scanner(self, device_name: Optional[str] = None) -> Any:
        """
        Open a scanner device.

        Args:
            device_name: Scanner device name (auto-detect if None)

        Returns:
            Scanner device handle
        """
        self._ensure_initialized()

        if device_name is None:
            device_name = self.find_brother_scanner()

        if device_name is None:
            raise RuntimeError("No Brother scanner found")

        logger.info(f"Opening scanner: {device_name}")
        self._scanner = sane.open(device_name)
        return self._scanner

    def get_scanner_options(self) -> Dict[str, Any]:
        """Get available scanner options."""
        if self._scanner is None:
            raise RuntimeError("Scanner not opened")

        options = {}
        for name in self._scanner.opt:
            opt = self._scanner.opt[name]
            options[name] = {
                "title": opt.title,
                "type": str(opt.type),
                "unit": opt.unit,
                "constraint": opt.constraint,
                "is_active": opt.is_active,
                "value": opt.value,
            }

        return options

    def set_option(self, name: str, value: Any) -> None:
        """Set a scanner option."""
        if self._scanner is None:
            raise RuntimeError("Scanner not opened")

        logger.info(f"Setting {name} = {value}")
        self._scanner[name] = value

    def set_resolution(self, dpi: int = DPI_300) -> None:
        """Set scan resolution."""
        self.set_option("resolution", dpi)

    def set_source(self, source: str) -> None:
        """Set scan source (Flatbed, ADF, ADF Duplex)."""
        self.set_option("source", source)

    def set_scan_area(self, width_mm: float, height_mm: float) -> None:
        """Set scan area in millimeters."""
        # Convert to pixels at current DPI
        dpi = self._scanner.opt.get("resolution", {}).get("value", 300)
        width = int(width_mm * dpi / 25.4)
        height = int(height_mm * dpi / 25.4)

        # Set tl-x, tl-y, br-x, br-y
        self._scanner["tl-x"] = 0
        self._scanner["tl-y"] = 0
        self._scanner["br-x"] = width
        self._scanner["br-y"] = height

    def scan(self) -> Image.Image:
        """
        Perform scan and return PIL Image.

        Returns:
            PIL Image object
        """
        if self._scanner is None:
            self.open_scanner()

        logger.info("Starting scan...")
        self._scanner.start()
        img = self._scanner.scan()

        logger.info(f"Scan complete: {img.size}")
        return img

    def scan_to_bytes(self, format: str = "PNG") -> bytes:
        """
        Scan and return as bytes.

        Args:
            format: Image format (PNG, JPEG, TIFF)

        Returns:
            Image data as bytes
        """
        img = self.scan()
        buffer = BytesIO()
        img.save(buffer, format=format)
        return buffer.getvalue()

    def scan_multi_page(self, pages: int = 1) -> List[Image.Image]:
        """
        Scan multiple pages from ADF.

        Args:
            pages: Expected number of pages

        Returns:
            List of PIL Image objects
        """
        images = []

        for i in range(pages):
            logger.info(f"Scanning page {i + 1}/{pages}")
            img = self.scan()
            images.append(img)

        return images

    def close(self) -> None:
        """Close scanner."""
        if self._scanner is not None:
            logger.info("Closing scanner")
            self._scanner.close()
            self._scanner = None

    def __del__(self):
        """Cleanup on deletion."""
        if self._initialized:
            try:
                sane.exit()
            except:
                pass


class ScanOptions:
    """Scan option constants and helpers."""

    SOURCE_FLATBED = "Flatbed"
    SOURCE_ADF = "ADF"
    SOURCE_ADF_DUPLEX = "ADF Duplex"

    DPI_150 = 150
    DPI_300 = 300
    DPI_600 = 600

    FORMAT_PDF = "PDF"
    FORMAT_JPEG = "JPEG"
    FORMAT_PNG = "PNG"
    FORMAT_TIFF = "TIFF"

    # Paper sizes in mm
    LETTER_WIDTH = 215.9
    LETTER_HEIGHT = 279.4
    LEGAL_WIDTH = 215.9
    LEGAL_HEIGHT = 355.6
    A4_WIDTH = 210
    A4_HEIGHT = 297

    @staticmethod
    def create_options(
        source: str = SOURCE_FLATBED,
        dpi: int = DPI_300,
        format: str = FORMAT_PDF,
        paper_width: float = LETTER_WIDTH,
        paper_height: float = LETTER_HEIGHT,
    ) -> Dict[str, Any]:
        """Create standard scan options."""
        return {
            "source": source,
            "resolution": dpi,
            "format": format,
            "width_mm": paper_width,
            "height_mm": paper_height,
        }


if __name__ == "__main__":
    sm = ScannerManager()
    scanners = sm.discover_scanners()
    print("Available scanners:")
    for dev in scanners:
        print(f"  {dev['name']}: {dev['vendor']} {dev['model']}")
