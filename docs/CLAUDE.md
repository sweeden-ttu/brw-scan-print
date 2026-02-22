# CLAUDE.md - Claude AI Development Guide

This document provides guidance for Claude AI when working on the Brother MFC-L2750DW GNOME Scanner & Printer application.

## Project Overview

Build a GNOME desktop application for Brother MFC-L2750DW that provides:
- Printing via CUPS/IPP
- Scanning via SANE + brscan5
- GTK4-based UI with GObject
- Support for ADF, duplex, paper trays

**Device**: 192.168.0.23, firmware ZE 1.13, node BRW3-C9ABF72124

## Pre-Installed Drivers

The Brother drivers are already downloaded and installed on this system:
- Printer driver: `brother-mfc2750dw-4.0.0-1.x86_64.rpm`
- Scanner driver: `brscan5-0.4.11-1.x86_64.rpm`
- Scan-key-tool: `brscan-skey-0.3.4-0.x86_64.rpm`

Driver files are located in: `~/projects/brw-scan-print/setup/`

To examine driver contents:
```bash
# List driver files
ls -la ~/projects/brw-scan-print/setup/

# Extract and examine RPM contents
rpm2cpio ~/projects/brw-scan-print/setup/brscan5-0.4.11-1.x86_64.rpm | cpio -idmv
```

## Development Philosophy

### Recommended Approach: Incremental Test-Driven Development

1. **Start Simple**: Get basic printing working first
2. **Add Scanning**: Then integrate SANE scanning
3. **Build UI**: Finally create GTK interface
4. **Test Each Layer**: Write tests before implementation

## Claude-Specific Guidelines

### Language Selection

**Recommended: Python with PyGObject**

Reasons:
- Faster iteration than C/Vala
- Direct bindings to GTK, CUPS, SANE
- Easier debugging
- Can still create proper GNOME app via PyGObject

```python
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject

import cups
import sane
```

### Key Libraries

| Library | Purpose | Python Bindings |
|---------|---------|-----------------|
| GTK4 | UI Framework | `gi.repository.Gtk` |
| CUPS | Printing | `cups` module |
| SANE | Scanning | `sane` module |
| libgusb | USB Device | `gi.repository.GUsb` |

### Build System

Use Meson for C/Vala components:

```meson
project('brw-scan-print', 'c', 'vala',
    version: '0.1.0',
    meson_version: '>=0.50'

gnome = import('gnome')
gtk = dependency('gtk4')

# Python components use pip
py_dep = dependency('python3')
pygobject_dep = dependency('pygobject-3.0')
```

### Testing Strategy

```python
# test/test_printer.py
import unittest
from brw_printer import PrinterManager

class TestPrinterDiscovery(unittest.TestCase):
    def test_discover_network_printer(self):
        pm = PrinterManager()
        printers = pm.discover()
        self.assertIsInstance(printers, list)
        
    def test_connect_to_known_device(self):
        pm = PrinterManager()
        printer = pm.connect('192.168.0.23')
        self.assertIsNotNone(printer)
```

## Implementation Tasks

### Phase 1: Printer Integration (Priority: HIGH)

1. **Discover printers**
   ```python
   # Use CUPS IPP API
   conn = cups.Connection()
   printers = conn.getPrinters()
   ```

2. **Send print job**
   ```python
   # Submit print job
   job_id = conn.printFile('MFC-L2750DW', '/path/to/file.pdf', 'Title', {})
   ```

3. **Printer options**
   ```python
   # Get/set printer options
   conn.setJobHoldUntil(job_id, 'indefinite')
   conn.cancelJob(job_id)
   ```

### Phase 2: Scanner Integration (Priority: HIGH)

1. **Initialize SANE**
   ```python
   sane.init()
   devices = sane.get_devices()
   ```

2. **Open scanner**
   ```python
   dev = sane.open(devices[0].name)
   dev.start()
   img = dev.scan()
   ```

3. **ADF & Duplex**
   ```python
   # Set source options
   dev['source'] = 'ADF Duplex'
   dev['duplex'] = True
   ```

### Phase 3: GTK UI (Priority: MEDIUM)

1. **Main Window**
   ```python
   class Application(Gtk.Application):
       def do_activate(self):
           window = Gtk.ApplicationWindow()
           window.set_title("Brother Scanner & Printer")
           window.present()
   ```

2. **Print Dialog Integration**
   ```python
   print_op = Gtk.PrintOperation()
   print_op.set_embed_page_setup(True)
   result = print_op.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)
   ```

3. **Scanner Preview**
   ```python
   # Preview scanned image
   img = Gtk.Image()
   img.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_data(...))
   ```

## Code Style

### Python

Follow PEP 8 with GNOME conventions:

```python
from gi.repository import Gtk, GObject, GdkPixbuf
import cups
import sane

class ScannerManager(GObject.Object):
    """Manages scanner connections and operations."""
    
    def __init__(self):
        super().__init__()
        self._scanners = []
        
    def discover(self):
        """Discover available scanners."""
        sane.init()
        self._scanners = sane.get_devices()
        return self._scanners
    
    def scan(self, device_name, options=None):
        """Perform scan with given options."""
        options = options or {}
        dev = sane.open(device_name)
        for opt, val in options.items():
            dev[opt] = val
        return dev.scan()
```

### C/Vala

Follow GNOME C coding style:

```vala
class PrinterManager : Object {
    private Cups.Connection conn;
    
    public void discover() {
        stdout.printf("Discovering printers...\n");
    }
}
```

## Common Issues & Solutions

### Issue: SANE not finding network scanner

**Solution**: Configure brscan5 properly:

```bash
brsaneconfig5 -a name=MFC-L2750DW \
  ip=192.168.0.23 \
  modelname=MFC-L2750DW
```

### Issue: GTK print dialog not showing printer

**Solution**: Ensure CUPS printer is registered:

```bash
lpstat -p
lpadmin -p MFC-L2750DW -v ipp://192.168.0.23/ipp/print -E
```

### Issue: Permission denied on scanner

**Solution**: Add user to scanner group:

```bash
sudo usermod -a -G scanner $USER
# Log out and back in
```

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Python modules | snake_case | `brw_scanner.py` |
| Python classes | PascalCase | `class ScannerManager` |
| C headers | snake_case.h | `brw_printer.h` |
| C sources | snake_case.c | `brw_printer.c` |
| Vala sources | snake_case.vala | `brw_scanner.vala` |
| Test files | test_*.py | `test_scanner.py` |
| Config files | *.conf | `brw-scan-print.conf` |

## Debugging

### Python Debug

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use Python's debugger
import pdb; pdb.set_trace()
```

### SANE Debug

```bash
SANE_DEBUG_ALL=1 scanimage -L
```

### CUPS Debug

```bash
cupsctl --debug-logging
tail -f /var/log/cups/error_log
```

## Next Steps for Claude

1. **Set up environment**: Use `module` toolchain
2. **Write unit tests first**: Test printer/scanner discovery
3. **Implement printer module**: Basic CUPS integration
4. **Implement scanner module**: SANE + brscan5
5. **Build GTK UI**: Simple main window
6. **Integrate print dialog**: Use Gtk.PrintOperation

## Important Notes

- Device IP is fixed at 192.168.0.23
- Use network protocol (IPP) not USB for reliability
- Test with simple-scan first to verify SANE works
- The module toolchain provides build environment:
  ```bash
  module install python 3.12.0
  module install c 14.0.0
  module install c++ 14.0.0
  ```
