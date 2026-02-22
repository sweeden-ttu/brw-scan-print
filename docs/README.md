# Brother MFC-L2750DW GNOME Scanner & Printer Application

A comprehensive GNOME desktop application for the Brother MFC-L2750DW all-in-one printer/scanner with automatic document feeder (ADF), duplex scanning, and multiple paper tray support.

## Device Specifications

| Feature | Specification |
|---------|---------------|
| **Model** | Brother MFC-L2750DW |
| **Type** | Monochrome Laser All-in-One |
| **Print Speed** | 34-36 ppm |
| **Print Resolution** | 2400 x 600 DPI |
| **Scan Resolution** | 2400 x 600 DPI (optical) |
| **ADF Capacity** | 50 sheets with duplex |
| **Paper Tray** | 250 sheets (Letter, Legal, Executive, A4, A5, B6) |
| **Network IP** | 192.168.0.23 |
| **Firmware** | ZE 1.13 |
| **Node Name** | BRW3-C9ABF72124 |

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **UI Framework** | GTK4/GObject | GNOME-native interface |
| **Printing** | CUPS, IPP | System printing |
| **Scanning** | SANE, libgusb | Scanner access |
| **Build System** | Meson/Ninja | C/Vala builds |
| **Python** | PyGObject | Language bindings |
| **Driver** | brscan5 + IPP | Device communication |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GNOME Desktop                             │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │   GTK4 UI       │  │   Print Dialog (GtkPrint*)     │  │
│  │   (App Window)  │  │   Scan Preview                 │  │
│  └────────┬────────┘  └──────────────┬──────────────────┘  │
│           │                          │                       │
│           └────────────┬─────────────┘                       │
│                        │                                     │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              Application Core                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │  │
│  │  │ PrintManager │  │ ScanManager  │  │ TrayMgr  │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘  │  │
│  └─────────┼──────────────────┼────────────────┼────────┘  │
│            │                  │                │             │
│  ┌─────────▼─────────────────▼────────────────▼─────────┐  │
│  │              Driver Layer                             │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │  │
│  │  │ CUPS/IPP     │  │ SANE+brscan5 │  │ Network  │  │  │
│  │  │ (Printing)   │  │ (Scanning)   │  │ Config   │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                        │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐
    │ Network │    │  brscan5  │   │    CUPS   │
    │ Printer │    │  Scanner  │   │  Server   │
    │192.168.0│    │  Driver   │   │  Local   │
    └─────────┘    └───────────┘   └───────────┘
```

## Supported Features

### Printing
- [ ] Black & white printing (default)
- [ ] Color printing (via driver)
- [ ] Duplex printing
- [ ] Paper source selection (Tray 1, Manual, ADF)
- [ ] Paper size: Letter, Legal
- [ ] Print quality settings
- [ ] Integration with GNOME print dialog

### Scanning
- [ ] Flatbed scanning
- [ ] ADF single-sided scanning
- [ ] ADF duplex scanning (double-sided)
- [ ] Scan to PDF, JPEG, PNG, TIFF
- [ ] Resolution: 150, 300, 600 DPI
- [ ] Automatic document feeder usage detection

## Project Structure

```
brw-scan-print/
├── docs/                    # Documentation
│   ├── README.md           # This file
│   ├── CLAUDE.md           # Claude AI guide
│   ├── AGENTS.md           # Agent systems guide
│   └── GEMINI.md           # Gemini AI guide
├── src/
│   ├── c/                  # C implementation
│   │   ├── include/        # Headers
│   │   ├── src/           # Source files
│   │   ├── meson.build    # Build configuration
│   │   └── CMakeLists.txt # Alternative build
│   ├── python/             # Python implementation
│   │   ├── brw_scanner/   # Scanner module
│   │   ├── brw_printer/   # Printer module
│   │   └── setup.py       # Package setup
│   └── vala/               # Vala implementation
│       ├── src/            # Vala source
│       └── meson.build     # Vala build
├── test/
│   ├── c/                  # C tests
│   ├── python/             # Python tests
│   └── integration/        # Integration tests
├── build/                  # Build output
├── etc/                    # Configuration files
│   └── brw-scan-print.conf # App configuration
├── scripts/                # Helper scripts
│   ├── install-deps.sh    # Install dependencies
│   ├── build-all.sh       # Build all implementations
│   └── test-device.sh     # Device testing
└── README.md               # Main documentation
```

## Prerequisites

### System Dependencies

```bash
# Install using module toolchain
module install c 14.0.0
module install c++ 14.0.0  
module install python 3.12.0
module install go 1.22.0

# Or install system dependencies manually
sudo dnf install \
    gcc gcc-c++ \
    libsane-devel cups-devel libusb-devel \
    glib2-devel gtk4-devel \
    meson ninja-build \
    python3-devel python3-gobject \
    vala gtk4-devel
```

### Brother Driver Installation

The application requires the Brother MFC-L2750DW drivers for network printing and scanning.

#### Download URLs (Rocky Linux 10 / RHEL / CentOS)

| Driver | Version | Download URL |
|--------|---------|--------------|
| Driver Install Tool | 2.2.6-0 | https://download.brother.com/welcome/dlf105302/driver-install-tool-2.2.6-0.x86_64.rpm |
| Linux Printer Driver (RPM) | 4.0.0-1 | https://download.brother.com/welcome/dlf101949/brother-mfc2750dw-4.0.0-1.x86_64.rpm |
| Scanner Driver 64-bit (RPM) | 0.4.11-1 | https://download.brother.com/welcome/dlf005948/brscan5-0.4.11-1.x86_64.rpm |
| Scan-key-tool 64-bit (RPM) | 0.3.4-0 | https://download.brother.com/welcome/dlf105303/brscan-skey-0.3.4-0.x86_64.rpm |
| Scanner Setting File (RPM) | 1.0.2-0 | https://download.brother.com/welcome/dlf002330/brscan-scfg-1.0.2-0.x86_64.rpm |

#### Installation Commands

```bash
# Create driver directory
mkdir -p ~/brother-drivers
cd ~/brother-drivers

# Download all required drivers
curl -O https://download.brother.com/welcome/dlf105302/driver-install-tool-2.2.6-0.x86_64.rpm
curl -O https://download.brother.com/welcome/dlf101949/brother-mfc2750dw-4.0.0-1.x86_64.rpm
curl -O https://download.brother.com/welcome/dlf005948/brscan5-0.4.11-1.x86_64.rpm
curl -O https://download.brother.com/welcome/dlf105303/brscan-skey-0.3.4-0.x86_64.rpm
curl -O https://download.brother.com/welcome/dlf002330/brscan-scfg-1.0.2-0.x86_64.rpm

# Install Printer Driver (requires sudo)
sudo dnf install -y brother-mfc2750dw-4.0.0-1.x86_64.rpm

# Install Scanner Driver (requires sudo)
sudo dnf install -y brscan5-0.4.11-1.x86_64.rpm

# Install Scan-key-tool (optional, for scanner button support)
sudo dnf install -y brscan-skey-0.3.4-0.x86_64.rpm

# Install Scanner Setting File (optional)
sudo dnf install -y brscan-scfg-1.0.2-0.x86_64.rpm

# Configure network scanner (no sudo required)
brsaneconfig5 -a name=MFC-L2750DW \
  ip=192.168.0.23 \
  modelname=MFC-L2750DW

# Verify scanner is recognized
brsaneconfig5 -l
```
  ip=192.168.0.23 \
  modelname=MFC-L2750DW
```

## Building

### Python Implementation (Recommended)

```bash
cd ~/projects/brw-scan-print

# Set up Python environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pygobject cups4 pycairo pillow

# Build and install
cd src/python
pip install -e .
```

### C Implementation

```bash
cd ~/projects/brw-scan-print/src/c
meson setup build
meson compile -C build
meson install --prefix=$HOME/.local
```

### Vala Implementation

```bash
cd ~/projects/brw-scan-print/src/vala
meson setup build
meson compile -C build
```

## Testing

### Unit Tests

```bash
# Python tests
cd ~/projects/brw-scan-print/test/python
python3 -m pytest

# C tests
cd ~/projects/brw-scan-print/test/c
meson test -C build
```

### Device Integration Tests

```bash
# Test printer discovery
python3 -c "
from brw_printer import PrinterManager
pm = PrinterManager()
print(pm.discover())

# Test scanner discovery  
from brw_scanner import ScannerManager
sm = ScannerManager()
print(sm.discover())
"

# Run device test script
./scripts/test-device.sh 192.168.0.23
```

## Usage

### Command Line

```bash
# Start GUI application
brw-scan-print

# Print a document
brw-print --printer MFC-L2750DW --copies 2 document.pdf

# Scan from ADF
brw-scan --device MFC-L2750DW --source adf --output scan.pdf

# Scan duplex
brw-scan --device MFC-L2750DW --source adf-duplex --output scan.pdf
```

### Integration with GNOME

The application integrates with:

- **GNOME Files**: Right-click "Print with brw-scan-print"
- **GNOME Print Dialog**: Select as system printer
- **Desktop Shortcuts**: Launch scan/print from desktop

## Configuration

Edit `etc/brw-scan-print.conf`:

```ini
[device]
ip_address = 192.168.0.23
model = MFC-L2750DW
firmware = ZE 1.13
node_name = BRW3-C9ABF72124

[scanning]
default_dpi = 300
default_format = PDF
default_source = flatbed

[printing]
default_copies = 1
default_quality = normal
default_paper = letter

[paths]
scan_output = ~/Documents/Scans
log_file = ~/.local/share/brw-scan-print/log.txt
```

## Troubleshooting

### Scanner Not Found

```bash
# Check network connectivity
ping 192.168.0.23

# Check brscan configuration
brsaneconfig5 -l

# View SANE devices
scanimage -L
```

### Printer Not Found

```bash
# Check CUPS
cupsctl | grep printer

# View CUPS printers
lpstat -p

# Add printer manually
lpadmin -p MFC-L2750DW -v ipp://192.168.0.23/ipp/print -E
```

### Permission Issues

```bash
# Add user to scanner group
sudo usermod -a -G scanner $USER

# Set up udev rules (requires sudo)
echo 'ATTRS{idVendor}=="04f9", ENV{libsane_matched}="yes"' | \
  sudo tee /etc/udev/rules.d/60-brother.rules
```

## Development

See the following guides for different development approaches:

- **[CLAUDE.md](docs/CLAUDE.md)** - For Claude AI development
- **[AGENTS.md](docs/AGENTS.md)** - For multi-agent systems
- **[GEMINI.md](docs/GEMINI.md)** - For code generation

## License

GPL-3.0 or later

## Author

Brother MFC-L2750DW GNOME Application Project

## References

- [SANE Project](http://sane-project.org/)
- [CUPS Documentation](https://www.cups.org/doc/)
- [GTK4 Print API](https://docs.gtk.org/gtk4/class.PrintOperation.html)
- [Brother Linux Drivers](https://support.brother.com/g/s/id/linux/en/index.html)
