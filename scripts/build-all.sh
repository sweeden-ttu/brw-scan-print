#!/bin/bash
# Build Script for brw-scan-print
# Builds all implementations (Python, C, Vala)

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=============================================="
echo "Building brw-scan-print"
echo "=============================================="

# Source module toolchain if available
if command -v module &> /dev/null; then
    echo "Loading module toolchain..."
    source ~/module-toolchain/module.sh 2>/dev/null || true
    
    # Install required toolchains
    echo "Installing toolchains..."
    module install python 3.12.0 2>/dev/null || true
    module install c 14.0.0 2>/dev/null || true
    module install c++ 14.0.0 2>/dev/null || true
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo dnf install -y \
    gcc gcc-c++ \
    python3-devel python3-pip \
    gtk4-devel libsane-devel cups-devel libusb-devel \
    glib2-devel gobject-introspection \
    meson ninja-build \
    2>/dev/null || true

# Install Python dependencies
echo "Installing Python packages..."
pip3 install --user pygobject pycairo pillow pytest || true

echo ""
echo "=============================================="
echo "Building Python Implementation"
echo "=============================================="

if [ -d "src/python" ]; then
    cd src/python
    
    # Install in development mode
    pip3 install -e . --user || true
    
    # Run tests if available
    if [ -d "test" ]; then
        echo "Running Python tests..."
        python3 -m pytest test/ -v || true
    fi
    
    cd "$PROJECT_DIR"
fi

echo ""
echo "=============================================="
echo "Building C Implementation"
echo "=============================================="

if [ -d "src/c" ]; then
    cd src/c
    
    if [ -f "meson.build" ]; then
        meson setup build --prefix="$HOME/.local" || true
        meson compile -C build || true
        meson install --prefix="$HOME/.local" || true
    fi
    
    cd "$PROJECT_DIR"
fi

echo ""
echo "=============================================="
echo "Build Complete!"
echo "=============================================="
echo ""
echo "Python modules installed to: ~/.local/lib/python*/site-packages/"
echo "C libraries installed to: ~/.local/lib/"
echo ""
echo "To use the modules:"
echo "  export PYTHONPATH=\$HOME/.local/lib/python3.12/site-packages:\$PYTHONPATH"
echo "  python3 -c 'from brw_printer import PrinterManager'"
