#!/bin/bash
# Brother MFC-L2750DW Driver Download and Installation Script
# Run as: bash install-drivers.sh

set -e

echo "=============================================="
echo "Brother MFC-L2750DW Driver Installer"
echo "=============================================="

# Check if running as root (needed for RPM installation)
if [ "$EUID" -ne 0 ] && ! sudo -v 2>/dev/null; then
    echo "Note: RPM installation requires sudo. Run with appropriate permissions."
fi

# Create driver directory
DRIVER_DIR="$HOME/brother-drivers"
mkdir -p "$DRIVER_DIR"
cd "$DRIVER_DIR"

echo ""
echo "Downloading Brother drivers..."

# Driver URLs
DRIVERS=(
    "https://download.brother.com/welcome/dlf105302/driver-install-tool-2.2.6-0.x86_64.rpm"
    "https://download.brother.com/welcome/dlf101949/brother-mfc2750dw-4.0.0-1.x86_64.rpm"
    "https://download.brother.com/welcome/dlf005948/brscan5-0.4.11-1.x86_64.rpm"
    "https://download.brother.com/welcome/dlf105303/brscan-skey-0.3.4-0.x86_64.rpm"
    "https://download.brother.com/welcome/dlf002330/brscan-scfg-1.0.2-0.x86_64.rpm"
)

for url in "${DRIVERS[@]}"; do
    filename=$(basename "$url")
    if [ ! -f "$filename" ]; then
        echo "  Downloading $filename..."
        curl -L -o "$filename" "$url" --progress-bar
    else
        echo "  Already downloaded: $filename"
    fi
done

echo ""
echo "=============================================="
echo "Installing Printer Driver"
echo "=============================================="
sudo dnf install -y ./brother-mfc2750dw-4.0.0-1.x86_64.rpm || \
    sudo rpm -ihv --nodeps ./brother-mfc2750dw-4.0.0-1.x86_64.rpm

echo ""
echo "=============================================="
echo "Installing Scanner Driver (brscan5)"
echo "=============================================="
sudo dnf install -y ./brscan5-0.4.11-1.x86_64.rpm || \
    sudo rpm -ihv --nodeps ./brscan5-0.4.11-1.x86_64.rpm

echo ""
echo "=============================================="
echo "Installing Scan-key-tool"
echo "=============================================="
sudo dnf install -y ./brscan-skey-0.3.4-0.x86_64.rpm || \
    sudo rpm -ihv --nodeps ./brscan-skey-0.3.4-0.x86_64.rpm

echo ""
echo "=============================================="
echo "Installing Scanner Setting File"
echo "=============================================="
sudo dnf install -y ./brscan-scfg-1.0.2-0.x86_64.rpm || \
    sudo rpm -ihv --nodeps ./brscan-scfg-1.0.2-0.x86_64.rpm

echo ""
echo "=============================================="
echo "Configuring Network Scanner"
echo "=============================================="
brsaneconfig5 -a name=MFC-L2750DW model=MFC-L2750DW ip=192.168.0.23

echo ""
echo "=============================================="
echo "Configuring CUPS Printer"
echo "=============================================="
sudo lpadmin -p MFC-L2750DW \
    -v ipp://192.168.0.23/ipp/print \
    -E \
    -m raw 2>/dev/null || echo "Printer configuration may need manual setup"

echo ""
echo "=============================================="
echo "Verifying Installation"
echo "=============================================="

echo ""
echo "Scanner configuration:"
brsaneconfig5 -q

echo ""
echo "Installed packages:"
rpm -qa | grep -E "(brother|brscan)"

echo ""
echo "=============================================="
echo "Installation Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Start scan-key-tool: brscan-skey"
echo "2. Test scanner: brscan-skey -l"
echo "3. Test printer: lpstat -p"
echo ""
echo "Device IP: 192.168.0.23"
echo "Device Model: MFC-L2750DW"
