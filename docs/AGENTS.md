# AGENTS.md - Multi-Agent Development Guide

This document provides guidance for autonomous agent systems working on the Brother MFC-L2750DW GNOME Scanner & Printer application.

## Project Overview

- **Device**: Brother MFC-L2750DW at 192.168.0.23 (firmware ZE 1.13)
- **Platform**: Rocky Linux 10 (x86_64, rpm)
- **Goal**: Build GNOME desktop app for print/scan with ADF support

## Pre-Installed Drivers

The Brother drivers are already downloaded and installed on this system:
- Printer driver: `brother-mfc2750dw-4.0.0-1.x86_64.rpm`
- Scanner driver: `brscan5-0.4.11-1.x86_64.rpm`
- Scan-key-tool: `brscan-skey-0.3.4-0.x86_64.rpm`

Driver files are located in: `~/projects/brw-scan-print/setup/`

To examine driver contents:
```bash
ls -la ~/projects/brw-scan-print/setup/
rpm2cpio ~/projects/brw-scan-print/setup/brscan5-0.4.11-1.x86_64.rpm | cpio -idmv
```

## Rocky Linux 10 Best Practices

### Recommended Stack

| Component | Rocky Linux Package | Version |
|-----------|-------------------|---------|
| Compiler | gcc, gcc-c++ | System default |
| Python | python3.12 | Module or python312 |
| GTK | gtk4-devel | Latest |
| CUPS | cups-devel, libcups | 2.x |
| SANE | sane-backends-devel | 1.4.x |
| Build | meson, ninja-build | Latest |

### Installation Commands

```bash
# Using DNF (preferred on Rocky)
dnf install -y gcc gcc-c++ python3-devel
dnf install -y gtk4-devel libsane-devel cups-devel
dnf install -y meson ninja-build

# Or use module toolchain (no sudo required)
module install c 14.0.0
module install c++ 14.0.0  
module install python 3.12.0
module install go 1.22.0
```

## Agent Architecture

### Team Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Coordinator                          │
│  (Orchestrates all sub-agents)                              │
└─────────────────────────────────────────────────────────────┘
          │              │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │  Printer  │  │  Scanner  │  │    UI     │  │  Testing  │
    │   Agent   │  │   Agent   │  │   Agent   │  │   Agent   │
    └───────────┘  └───────────┘  └───────────┘  └───────────┘
```

### Agent Responsibilities

#### Agent 1: Printer Integration
- **Goal**: CUPS/IPP printer integration
- **Tasks**:
  1. Discover network printer at 192.168.0.23
  2. Submit print jobs via IPP
  3. Handle paper tray selection
  4. Implement duplex printing
  5. Test with various document types

#### Agent 2: Scanner Integration
- **Goal**: SANE + brscan5 scanner integration
- **Tasks**:
  1. Install brscan5 driver
  2. Configure network scanner
  3. Implement flatbed scanning
  4. Implement ADF scanning
  5. Implement duplex scanning

#### Agent 3: UI Development
- **Goal**: GTK4 GNOME application
- **Tasks**:
  1. Create main application window
  2. Integrate print dialog (Gtk.PrintOperation)
  3. Create scan preview widget
  4. Add tray selection UI
  5. Apply GNOME styling

#### Agent 4: Testing & QA
- **Goal**: Comprehensive testing
- **Tasks**:
  1. Write unit tests for each module
  2. Integration tests with real device
  3. Performance benchmarking
  4. Edge case handling
  5. Documentation testing

## Parallel Development Strategy

### Independent Workstreams

Each agent can work independently with these interfaces:

```python
# Shared interfaces for all agents
class DeviceInterface:
    """Common device interface."""
    def connect(self) -> bool: ...
    def disconnect(self) -> None: ...
    def get_status(self) -> dict: ...

class PrinterInterface(DeviceInterface):
    """Printer-specific interface."""
    def print_file(self, path: str, options: dict) -> int: ...
    def get_queues(self) -> list: ...
    def cancel_job(self, job_id: int) -> None: ...

class ScannerInterface(DeviceInterface):
    """Scanner-specific interface."""
    def scan(self, options: dict) -> bytes: ...
    def get_sources(self) -> list: ...
    def set_source(self, source: str) -> None: ...
```

### Synchronization Points

1. **Daily Standup**: Share progress, blockers
2. **API Changes**: Update shared interfaces
3. **Integration Testing**: Combined testing phase
4. **Release**: Unified build and deployment

## Implementation Approaches

### Approach 1: Component-Based (Recommended)

**Strategy**: Build independent components, integrate at end

| Phase | Duration | Agent | Deliverable |
|-------|----------|-------|-------------|
| 1 | 2 days | Printer | printer.py module |
| 2 | 2 days | Scanner | scanner.py module |
| 3 | 3 days | UI | main.ui window |
| 4 | 2 days | Testing | test suite |
| 5 | 1 day | Integration | Working app |

**Pros**: Parallel work, clear boundaries
**Cons**: Integration risk

### Approach 2: Layer-Based

**Strategy**: Build layers bottom-up

| Layer | Components |
|-------|------------|
| 1 | Device communication |
| 2 | CUPS/SANE wrappers |
| 3 | Business logic |
| 4 | UI components |

### Approach 3: Test-First

**Strategy**: Write tests first, implement to pass

```python
# test_scanner.py
def test_adf_scan():
    """Test ADF scanning."""
    scanner = ScannerManager()
    scanner.connect('192.168.0.23')
    scanner.set_source('ADF')
    result = scanner.scan()
    assert result is not None
    assert len(result.pages) == expected_pages
```

## Communication Protocol

### Message Format

```json
{
  "agent": "printer",
  "action": "discover",
  "params": {},
  "result": {
    "printers": ["MFC-L2750DW"]
  }
}
```

### Shared State

Use Redis or file-based state:

```python
# state/shared.json
{
  "device_ip": "192.168.0.23",
  "device_model": "MFC-L2750DW",
  "firmware": "ZE 1.13",
  "printer_status": "ready",
  "scanner_status": "ready"
}
```

## Continuous Integration

### Build Pipeline

```yaml
# .github/workflows/build.yml
name: Build and Test

on: [push, pull_request]

jobs:
  build:
    runs-on: rocky-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          dnf install -y gtk4-devel libsane-devel cups-devel
          pip install -r requirements.txt
      - name: Run tests
        run: pytest test/python/
      - name: Build
        run: python -m build
```

### Test Pipeline

```bash
# Run all tests
make test

# Run specific module tests
pytest test/python/test_scanner.py -v
meson test -C build

# Integration tests
./scripts/test-device.sh 192.168.0.23
```

## Resource Management

### Shared Resources

| Resource | Access | Notes |
|----------|--------|-------|
| Device IP | Read-only | Fixed at 192.168.0.23 |
| CUPS | R/W | Local server |
| SANE | R/W | Local daemon |
| Build artifacts | R/W | build/ directory |

### Conflict Prevention

- Use file locking for shared state
- Separate test devices for each agent
- Coordinate device access times

## Deployment

### Local Installation

```bash
# Build all components
./scripts/build-all.sh

# Install for current user
pip install -e src/python
meson install --prefix=$HOME/.local
```

### System Installation (requires sudo)

```bash
# Requires sudo
sudo dnf install ./brw-scan-print.rpm
sudo systemctl enable brw-scan-print
```

## Error Handling

### Device Errors

```python
class DeviceError(Exception):
    """Base device error."""
    pass

class PrinterOfflineError(DeviceError):
    """Printer is offline."""
    pass

class ScannerBusyError(DeviceError):
    """Scanner is busy."""
    pass
```

### Recovery Strategies

| Error | Recovery |
|-------|----------|
| Device offline | Retry with backoff |
| Job failed | Re-queue with notification |
| ADF jam | Clear and retry |
| Network timeout | Reconnect and resume |

## Agent Coordination Example

```python
# coordinator.py
class AgentCoordinator:
    def __init__(self):
        self.agents = {
            'printer': PrinterAgent(),
            'scanner': ScannerAgent(),
            'ui': UIAgent(),
            'testing': TestingAgent()
        }
    
    def run_sprint(self, tasks):
        """Run sprint with parallel execution."""
        results = {}
        for task in tasks:
            agent = self.agents[task['agent']]
            results[task['id']] = agent.execute(task)
        return results
    
    def integrate(self):
        """Integrate all components."""
        # Run integration tests
        # Build final artifact
        # Generate reports
```

## Next Steps for Agents

1. **Read device specs** from README.md
2. **Set up environment** using module toolchain
3. **Pick approach** (component-based recommended)
4. **Start with tests** (test-first approach)
5. **Communicate** via shared state

## Important Notes

- All agents must use Rocky Linux 10 compatible packages
- Device IP is fixed: 192.168.0.23
- Use module toolchain for builds: `module install python 3.12.0`
- Report blockers immediately to coordinator
- Test on real hardware when possible
