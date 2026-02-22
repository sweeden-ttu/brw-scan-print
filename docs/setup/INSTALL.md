# Brother MFC-L2750DW Driver Installation Guide

This guide provides step-by-step instructions for installing Brother MFC-L2750DW drivers on Rocky Linux 10.

## Prerequisites

1. **Root/Sudo Access**: Required for installing RPM packages
2. **Network Connection**: Printer at 192.168.0.23 must be reachable
3. **Terminal Access**: Command line installation required

---

## Quick Installation (Recommended)

### Step 1: Download Drivers

```bash
mkdir -p ~/brother-drivers
cd ~/brother-drivers

# Download all required drivers
curl -L -O "https://download.brother.com/welcome/dlf105302/driver-install-tool-2.2.6-0.x86_64.rpm"
curl -L -O "https://download.brother.com/welcome/dlf101949/brother-mfc2750dw-4.0.0-1.x86_64.rpm"
curl -L -O "https://download.brother.com/welcome/dlf005948/brscan5-0.4.11-1.x86_64.rpm"
curl -L -O "https://download.brother.com/welcome/dlf105303/brscan-skey-0.3.4-0.x86_64.rpm"
curl -L -O "https://download.brother.com/welcome/dlf002330/brscan-scfg-1.0.2-0.x86_64.rpm"
```

### Step 2: Install Drivers (as root/sudo)

```bash
cd ~/brother-drivers

# Install Printer Driver
sudo dnf install -y ./brother-mfc2750dw-4.0.0-1.x86_64.rpm

# Install Scanner Driver
sudo dnf install -y ./brscan5-0.4.11-1.x86_64.rpm

# Install Scan-key-tool (optional - for scanner button support)
sudo dnf install -y ./brscan-skey-0.3.4-0.x86_64.rpm

# Install Scanner Setting File (optional)
sudo dnf install -y ./brscan-scfg-1.0.2-0.x86_64.rpm
```

### Step 3: Configure Network Scanner

```bash
# Add network scanner (no sudo required)
brsaneconfig5 -a name=MFC-L2750DW model=MFC-L2750DW ip=192.168.0.23

# Verify scanner is recognized
brsaneconfig5 -q
```

Expected output:
```
MFC-L2750DW        : 192.168.0.23    [IP]
```

### Step 4: Configure CUPS Printer

```bash
# Find printer IP
ping -c 1 192.168.0.23

# Add printer to CUPS
sudo lpadmin -p MFC-L2750DW \
  -v ipp://192.168.0.23/ipp/print \
  -E \
  -m raw

# Set as default printer
sudo lpoptions -d MFC-L2750DW

# Verify printer
lpstat -p
```

---

## Manual Installation (RPM Commands)

### Step 1: Login as Superuser

```bash
su -
# Or use sudo for all commands
sudo su -
```

### Step 2: Install the Driver

Navigate to the directory where you downloaded the drivers:

```bash
cd ~/brother-drivers
```

#### Install Printer Driver (RPM)

```bash
# Install printer driver
rpm -ihv --nodeps ./brother-mfc2750dw-4.0.0-1.x86_64.rpm
```

#### Install Scanner Driver (RPM)

```bash
# Install scanner driver
rpm -ihv --nodeps ./brscan5-0.4.11-1.x86_64.rpm
```

#### Install Scan-key-tool (RPM) - Optional

```bash
# Install scan-key-tool (enables scanner button on device)
rpm -ihv --nodeps ./brscan-skey-0.3.4-0.x86_64.rpm
```

### Step 3: Verify Installation

Check if the driver is installed:

```bash
# Check printer driver
rpm -qa | grep -e brother-mfc2750dw

# Check scanner driver
rpm -qa | grep -e brscan5

# Check scan-key-tool
rpm -qa | grep -e brscan-skey
```

Expected output:
```
brother-mfc2750dw-4.0.0-1.x86_64
brscan5-0.4.11-1.x86_64
brscan-skey-0.3.4-0.x86_64
```

---

## Network Scanner Configuration

### Using brsaneconfig5 (For brscan5 models)

#### Add Network Scanner Entry

```bash
brsaneconfig5 -a name=MFC-L2750DW model=MFC-L2750DW ip=192.168.0.23
```

#### Confirm Network Scanner Entry

```bash
brsaneconfig5 -q | grep MFC-L2750DW
```

Expected output:
```
MFC-L2750DW        : 192.168.0.23    [IP]
```

#### Remove Scanner Entry (if needed)

```bash
brsaneconfig5 -r MFC-L2750DW
```

---

## Scan-key-tool Setup (Scanner Button Support)

The Scan-key-tool allows you to initiate scans directly from the scanner's control panel button.

### Prerequisites

1. **Scanner driver must be installed first** (brscan5)
2. **GIMP** should be installed for "scan-to-image" functionality
3. **Firewall configuration** may be needed for network access

```bash
# Install GIMP (optional, for scan-to-image)
sudo dnf install -y gimp
```

### Install Scan-key-tool (as root/sudo)

```bash
# Navigate to driver directory
cd ~/brother-drivers

# Install scan-key-tool
sudo rpm -ihv --nodeps ./brscan-skey-0.3.4-0.x86_64.rpm
```

### Verify Installation

Check if the scan-key-tool is installed:

```bash
# Check installation
rpm -qa | grep -e brscan-skey
```

Expected output:
```
brscan-skey-0.3.4-0.x86_64
```

### Run Scan-key-tool

The scan-key-tool runs as a background daemon:

```bash
# Start scan-key-tool
brscan-skey
```

### Verify Scanner Detection

Check if the scanner is detected by scan-key-tool:

```bash
# List detected scanner devices
brscan-skey -l
```

Expected output:
```
 MFC-L2750DW          : 192.168.0.23         : Active
```

### Using the Scanner Button

1. **Place document** in ADF (Automatic Document Feeder) or on flatbed
2. **Press SCAN button** on the scanner control panel
3. **Select destination** on the scanner's LCD:
   - PC (Scan to computer)
   - Image (Scan to image editor)
   - OCR (Scan to OCR application)
   - Email (Scan and attach to email)
4. **Select user** (if prompted)
5. **Press START** to begin scan

### Scan-key-tool Options

```bash
# List options
brscan-skey -h

# Stop scan-key-tool
brscan-skey -t

# Start scan-key-tool
brscan-skey

# List devices
brscan-skey -l
```

### Troubleshooting Scan-key-tool

```bash
# Check if running
ps aux | grep brscan-skey

# Check logs
journalctl -xe | grep brscan-skey

# Restart service
pkill brscan-skey
brscan-skey
```

---

## CUPS Printer Configuration

### Add Network Printer

```bash
# Add printer via IPP
sudo lpadmin -p MFC-L2750DW \
  -v ipp://192.168.0.23/ipp/print \
  -E \
  -m raw

# Or using socket protocol
sudo lpadmin -p MFC-L2750DW \
  -v socket://192.168.0.23:9100 \
  -E \
  -m raw

# Or using LPD protocol
sudo lpadmin -p MFC-L2750DW \
  -v lpd://192.168.0.23/binbrlpr \
  -E \
  -m raw
```

### Set Default Printer

```bash
sudo lpoptions -d MFC-L2750DW
```

### Configure Printer Options

```bash
# Set default paper size
sudo lpadmin -p MFC-L2750DW -o media=letter

# Enable duplexing
sudo lpadmin -p MFC-L2750DW -o sides=two-sided-long-edge
```

### Test Printing

```bash
# Print test page
lp -d MFC-L2750DW /usr/share/cups/data/testprint

# Print a PDF
lpr -P MFC-L2750DW document.pdf

# Print with options
lpr -P MFC-L2750DW -o copies=2 -o sides=two-sided-long-edge document.pdf
```

---

## Testing the Installation

### Test Scanner

```bash
# List available scanners
scanimage -L

# Test scan (flatbed)
scanimage --device-name=brother5:net1 --output-file=test.ppm --format=ppm

# Or use simple-scan (if installed)
simple-scan
```

Expected output for `scanimage -L`:
```
device `brother5:net1' is a Brother MFC-L2750DW scanner
```

### Test Printer

```bash
# Check printer status
lpstat -p MFC-L2750DW

# View print queue
lpq -P MFC-L2750DW
```

---

## Troubleshooting

### Scanner Not Found

```bash
# Check network connectivity
ping 192.168.0.23

# Check brscan configuration
brsaneconfig5 -q

# Check SANE configuration
scanimage -L

# Restart saned service
sudo systemctl restart saned
```

### Printer Not Found

```bash
# Check CUPS status
sudo systemctl status cups

# Check network connectivity
ping 192.168.0.23

# View CUPS error log
sudo tail -f /var/log/cups/error_log

# Restart CUPS
sudo systemctl restart cups
```

### Permission Issues

```bash
# Add user to lp and scanner groups
sudo usermod -a -G lp,snanner $USER

# Log out and back in for changes to take effect
```

### Driver Reinstallation

```bash
# Remove old driver
sudo rpm -e brother-mfc2750dw
sudo rpm -e brscan5

# Reinstall
cd ~/brother-drivers
sudo dnf install -y ./brother-mfc2750dw-4.0.0-1.x86_64.rpm
sudo dnf install -y ./brscan5-0.4.11-1.x86_64.rpm
```

---

## Firewall Configuration for Scan-key-tool

To use the Brother Scan-key-tool (brscan-skey) for scanning from the scanner's control panel buttons, the following ports must be opened:

### Required Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| **54925** | UDP | Scan-key-tool discovery and communication |
| **54921** | TCP | Scan-key-tool data transfer |

### Rocky Linux 10 (firewalld)

```bash
# Add UDP port for Scan-key-tool discovery
sudo firewall-cmd --permanent --add-port=54925/udp

# Add TCP port for Scan-key-tool data transfer  
sudo firewall-cmd --permanent --add-port=54921/tcp

# Reload firewall
sudo firewall-cmd --reload

# Verify rules
sudo firewall-cmd --list-all
```

### Alternative: Allow Printer IP Only

For security, you can restrict to only the printer's IP address:

```bash
# Allow UDP from printer IP
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.0.23" port port="54925" protocol="udp" accept'

# Allow TCP from printer IP
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.0.23" port port="54921" protocol="tcp" accept'

# Reload firewall
sudo firewall-cmd --reload
```

### CUPS/IPP Printing Ports (Already Required)

| Port | Protocol | Purpose |
|------|----------|---------|
| **631** | TCP | IPP (Internet Printing Protocol) |
| **9100** | TCP | Raw socket printing |
| **80** | TCP | HTTP (web interface) |

```bash
# Allow IPP printing
sudo firewall-cmd --permanent --add-service=ipp

# Allow raw socket printing
sudo firewall-cmd --permanent --add-port=9100/tcp

# Reload
sudo firewall-cmd --reload
```

### Verify Firewall Settings

```bash
# List all rules
sudo firewall-cmd --list-all

# Check specific ports
sudo firewall-cmd --query-port=54925/udp
sudo firewall-cmd --query-port=54921/tcp
```

### If Using iptables (Legacy)

```bash
# Allow Scan-key-tool ports
sudo iptables -A INPUT -p udp --dport 54925 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 54921 -j ACCEPT

# Save rules
sudo service iptables save
```

---

## Device Information

| Setting | Value |
|---------|-------|
| **Model** | MFC-L2750DW |
| **IP Address** | 192.168.0.23 |
| **Firmware** | ZE 1.13 |
| **Node Name** | BRW3-C9ABF72124 |
| **Protocol** | IPP (Port 631) / Socket (Port 9100) |

---

## Driver Download URLs Reference

| Driver | Version | URL |
|--------|---------|-----|
| Driver Install Tool | 2.2.6-0 | https://download.brother.com/welcome/dlf105302/driver-install-tool-2.2.6-0.x86_64.rpm |
| Printer Driver | 4.0.0-1 | https://download.brother.com/welcome/dlf101949/brother-mfc2750dw-4.0.0-1.x86_64.rpm |
| Scanner Driver | 0.4.11-1 | https://download.brother.com/welcome/dlf005948/brscan5-0.4.11-1.x86_64.rpm |
| Scan-key-tool | 0.3.4-0 | https://download.brother.com/welcome/dlf105303/brscan-skey-0.3.4-0.x86_64.rpm |
| Scanner Setting | 1.0.2-0 | https://download.brother.com/welcome/dlf002330/brscan-scfg-1.0.2-0.x86_64.rpm |

---

## Related Commands Reference

```bash
# brsaneconfig5 options
brsaneconfig5 -a name=NAME model=MODEL ip=IP    # Add scanner
brsaneconfig5 -r NAME                            # Remove scanner
brsaneconfig5 -q                                 # List scanners
brsaneconfig5 -h                                 # Help

# lp/lpadmin options
lpadmin -p PRINTER -v URI -E                    # Add printer
lpadmin -x PRINTER                               # Remove printer
lpoptions -d PRINTER                             # Set default
lpstat -p                                        # List printers

# scanimage options
scanimage -L                                     # List devices
scanimage -d DEVICE --output=FILE               # Scan to file
```
