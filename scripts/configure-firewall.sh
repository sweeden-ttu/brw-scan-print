#!/bin/bash
# Brother MFC-L2750DW Firewall Configuration Script
# Configures firewall rules for printing and scanning

set -e

PRINTER_IP="192.168.0.23"

echo "=============================================="
echo "Brother MFC-L2750DW Firewall Configuration"
echo "=============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root (use sudo)"
    exit 1
fi

echo ""
echo "Configuring firewall for Brother MFC-L2750DW..."

# Add CUPS/IPP service
echo "[1/6] Adding IPP (CUPS) service..."
firewall-cmd --permanent --add-service=ipp 2>/dev/null || true

# Add raw socket printing
echo "[2/6] Adding raw socket printing (port 9100)..."
firewall-cmd --permanent --add-port=9100/tcp 2>/dev/null || true

# Add HTTP for web interface
echo "[3/6] Adding HTTP service (port 80)..."
firewall-cmd --permanent --add-service=http 2>/dev/null || true

# Add Scan-key-tool UDP (scanner discovery)
echo "[4/6] Adding Scan-key-tool UDP (port 54925)..."
firewall-cmd --permanent --add-port=54925/udp 2>/dev/null || true

# Add Scan-key-tool TCP (scanner data transfer)
echo "[5/6] Adding Scan-key-tool TCP (port 54921)..."
firewall-cmd --permanent --add-port=54921/tcp 2>/dev/null || true

# Alternative: Restrict to printer IP only (more secure)
echo "[6/6] Adding IP-based restriction for $PRINTER_IP..."
firewall-cmd --permanent --add-rich-rule="rule family='ipv4' source address='$PRINTER_IP' accept" 2>/dev/null || true

# Reload firewall
echo ""
echo "Reloading firewall..."
firewall-cmd --reload

echo ""
echo "=============================================="
echo "Firewall Configuration Complete!"
echo "=============================================="
echo ""
echo "Configured ports:"
echo "  - 631/tcp  (IPP/CUPS printing)"
echo "  - 9100/tcp (Raw socket printing)"
echo "  - 80/tcp   (HTTP web interface)"
echo "  - 54925/udp (Scan-key-tool discovery)"
echo "  - 54921/tcp (Scan-key-tool data transfer)"
echo ""

echo "Current firewall rules:"
firewall-cmd --list-all

echo ""
echo "Verify specific ports:"
echo "  UDP 54925: $(firewall-cmd --query-port=54925/udp 2>/dev/null || echo 'not configured')"
echo "  TCP 54921: $(firewall-cmd --query-port=54921/tcp 2>/dev/null || echo 'not configured')"
echo "  IPP:       $(firewall-cmd --query-service=ipp 2>/dev/null || echo 'not configured')"
