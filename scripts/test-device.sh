#!/bin/bash
# Brother MFC-L2750DW Device Test Script
# Tests connectivity and functionality of the Brother MFC-L2750DW device

set -e

PRINTER_IP="192.168.0.23"
PRINTER_NAME="MFC-L2750DW"

echo "=============================================="
echo "Brother MFC-L2750DW Device Test"
echo "=============================================="

# Test 1: Network Connectivity
echo ""
echo "[Test 1] Network Connectivity"
echo "-----------------------------"
if ping -c 1 -W 2 "$PRINTER_IP" > /dev/null 2>&1; then
    echo "✓ Printer is reachable at $PRINTER_IP"
else
    echo "✗ Cannot reach printer at $PRINTER_IP"
    echo "  Check network connection and IP address"
    exit 1
fi

# Test 2: Check brsaneconfig
echo ""
echo "[Test 2] Scanner Configuration"
echo "-------------------------------"
if command -v brsaneconfig5 &> /dev/null; then
    echo "brsaneconfig5 found"
    echo "Configured scanners:"
    brsaneconfig5 -q || echo "  No scanners configured"
else
    echo "✗ brsaneconfig5 not found (scanner driver may not be installed)"
fi

# Test 3: Check SANE
echo ""
echo "[Test 3] SANE Scanner Detection"
echo "--------------------------------"
if command -v scanimage &> /dev/null; then
    echo "scanimage found"
    echo "Available scanners:"
    scanimage -L || echo "  No scanners detected"
else
    echo "✗ scanimage not found (SANE may not be installed)"
fi

# Test 4: Check CUPS
echo ""
echo "[Test 4] CUPS Printer Status"
echo "----------------------------"
if command -v lpstat &> /dev/null; then
    echo "CUPS printers:"
    lpstat -p || echo "  No printers configured"
    
    echo ""
    echo "Printer queues:"
    lpq -a || echo "  No print queues"
else
    echo "✗ CUPS not found"
fi

# Test 5: Check scan-key-tool
echo ""
echo "[Test 5] Scan-key-tool Status"
echo "-------------------------------"
if command -v brscan-skey &> /dev/null; then
    echo "brscan-skey found"
    echo "Running brscan-skey -l:"
    brscan-skey -l || echo "  No devices detected"
    
    echo ""
    echo "brscan-skey process:"
    if pgrep -x brscan-skey > /dev/null; then
        echo "  ✓ brscan-skey is running"
    else
        echo "  ○ brscan-skey is not running"
        echo "  Run 'brscan-skey' to start"
    fi
else
    echo "✗ brscan-skey not found"
fi

# Test 6: IPP Printer Query
echo ""
echo "[Test 6] IPP Printer Query"
echo "--------------------------"
if command -v ippfind &> /dev/null; then
    echo "Looking for IPP printers on network..."
    ippfind || echo "  No IPP printers found"
else
    echo "ippfind not available"
fi

# Test 7: Device Information
echo ""
echo "[Test 7] Device Information"
echo "---------------------------"
echo "Printer IP: $PRINTER_IP"
echo "Printer Name: $PRINTER_NAME"
echo "Expected Firmware: ZE 1.13"
echo "Expected Node: BRW3-C9ABF72124"

# Test 8: Web Interface (if accessible)
echo ""
echo "[Test 8] Web Interface Check"
echo "-----------------------------"
if curl -s -m 5 "http://$PRINTER_IP/" > /dev/null 2>&1; then
    echo "✓ Web interface accessible at http://$PRINTER_IP"
else
    echo "○ Web interface not accessible (may require authentication)"
fi

echo ""
echo "=============================================="
echo "Test Complete"
echo "=============================================="
echo ""
echo "Summary:"
echo "- Network: Reachable"
echo "- Scanner: Check brsaneconfig5 -q"
echo "- Printer: Check lpstat -p"
echo ""
echo "To start scanning: brscan-skey"
echo "To print: lpr -P $PRINTER_NAME file.pdf"
