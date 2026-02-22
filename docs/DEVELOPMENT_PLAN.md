# Brother MFC-L2750DW Multi-Language Development Plan

## Project Overview

This document outlines the comprehensive development plan for creating Brother MFC-L2750DW printer/scanner libraries in multiple programming languages, along with AI agent integrations and development tools.

**Device**: Brother MFC-L2750DW  
**IP Address**: 192.168.0.23  
**Firmware**: ZE 1.13  
**Node Name**: BRW3-C9ABF72124

**Pre-installed Drivers** (available in ~/projects/brw-scan-print/setup/):
- brother-mfc2750dw-4.0.0-1.x86_64.rpm (Printer driver)
- brscan5-0.4.11-1.x86_64.rpm (Scanner driver)
- brscan-skey-0.3.4-0.x86_64.rpm (Scan-key-tool)
- brscan-scfg-1.0.2-0.x86_64.rpm (Scanner config)

---

## Table of Contents

1. [Python Library](#1-python-library)
2. [.NET Library](#2-net-library)
3. [Go Library](#3-go-library)
4. [Rust Library](#4-rust-library)
5. [Ollama Agentic Tools](#5-ollama-agentic-tools)
6. [LangChain/LangGraph Agents](#6-langchainlanggraph-agents)
7. [VS Code Integration](#7-vs-code-integration)
8. [Firewall Configuration](#8-firewall-configuration)
9. [SELinux Configuration](#9-selinux-configuration)
10. [Router Configuration](#10-router-configuration)

---

## 1. Python Library

### Current Status
- Basic printer module: `src/python/brw_printer/__init__.py`
- Basic scanner module: `src/python/brw_scanner/__init__.py`

### Enhancement Plan

#### Phase 1: Core Functionality
- [ ] **Printer Operations**
  - [ ] Print document (PDF, images, text)
  - [ ] Query printer status
  - [ ] Cancel print jobs
  - [ ] Set print options (copies, duplex, paper size, tray)
  
- [ ] **Scanner Operations**
  - [ ] Flatbed scanning
  - [ ] ADF single-sided scanning
  - [ ] ADF duplex scanning
  - [ ] Scan to multiple formats (PDF, JPEG, PNG, TIFF)
  - [ ] Set scan resolution (150, 300, 600 DPI)

#### Phase 2: Advanced Features
- [ ] **ADF Management**
  - [ ] Detect ADF availability
  - [ ] ADF paper capacity detection
  - [ ] Duplex mode support
  - [ ] Multi-page batch scanning
  
- [ ] **Paper Tray Management**
  - [ ] Detect available trays
  - [ ] Select paper source (Tray 1, Manual, MPF)
  - [ ] Paper size detection
  
- [ ] **Job Management**
  - [ ] Print queue management
  - [ ] Job history tracking
  - [ ] Print job priorities

#### Phase 3: Integration
- [ ] **GTK4 GUI**
  - [ ] Main application window
  - [ ] Print dialog integration
  - [ ] Scan preview widget
  - [ ] Settings management
  
- [ ] **CLI Tools**
  - [ ] `brw-print` - Print command
  - [ ] `brw-scan` - Scan command
  - [ ] `brw-status` - Device status

### Dependencies
```
pygobject
pycairo
Pillow
python-cups
python-sane (pysane)
```

### Module Structure
```
src/python/
├── brw_printer/
│   ├── __init__.py
│   ├── cups_client.py      # CUPS IPP client
│   ├── printer_manager.py  # Printer operations
│   └── options.py          # Print options
├── brw_scanner/
│   ├── __init__.py
│   ├── sane_client.py      # SANE client
│   ├── scanner_manager.py  # Scanner operations
│   └── options.py          # Scan options
├── brw_common/
│   ├── device.py          # Base device class
│   ├── config.py          # Configuration management
│   └── exceptions.py      # Custom exceptions
└── brw_app/
    ├── cli.py             # Command-line interface
    └── gui.py             # GTK application
```

---

## 2. .NET Library

### Target Framework
- .NET 8.0 (LTS)
- .NET 6.0 (for wider compatibility)

### Library Design

#### Core Interfaces
```csharp
namespace BrotherMFC
{
    public interface IPrinter
    {
        Task<PrintJob> PrintAsync(string filePath, PrintOptions options);
        Task<IEnumerable<PrintJob>> GetPrintQueueAsync();
        Task CancelJobAsync(int jobId);
        Task<PrinterStatus> GetStatusAsync();
    }
    
    public interface IScanner
    {
        Task<ScanResult> ScanAsync(ScanOptions options);
        Task<IEnumerable<string>> GetAvailableSourcesAsync();
        Task<bool> SetSourceAsync(string source);
    }
    
    public class PrintOptions
    {
        public int Copies { get; set; }
        public string PaperSize { get; set; }  // Letter, Legal, A4
        public string PaperSource { get; set; } // Tray1, Manual, MPF
        public bool Duplex { get; set; }
        public string Quality { get; set; }     // Draft, Normal, High
    }
    
    public class ScanOptions
    {
        public string Source { get; set; }    // Flatbed, ADF, ADF Duplex
        public int Resolution { get; set; }    // 150, 300, 600
        public string Format { get; set; }     // PDF, JPEG, PNG, TIFF
    }
}
```

### Implementation Plan

#### Phase 1: IPP Client
- [ ] HTTP/IPP client for printer communication
- [ ] IPP attribute parsing
- [ ] Print job submission
- [ ] Printer capabilities querying

#### Phase 2: SANE Integration
- [ ] P/Invoke bindings to libsane
- [ ] Scanner discovery
- [ ] Image acquisition
- [ ] Format conversion (System.Drawing.Common)

#### Phase 3: High-Level API
- [ ] PrinterManager class
- [ ] ScannerManager class
- [ ] Device discovery
- [ ] Async/await support

### Project Structure
```
src/csharp/BrotherMFC/
├── BrotherMFC/
│   ├── Printer/
│   │   ├── IPrinter.cs
│   │   ├── PrinterManager.cs
│   │   ├── PrintOptions.cs
│   │   └── PrintJob.cs
│   ├── Scanner/
│   │   ├── IScanner.cs
│   │   ├── ScannerManager.cs
│   │   ├── ScanOptions.cs
│   │   └── ScanResult.cs
│   ├── Common/
│   │   ├── DeviceInfo.cs
│   │   ├── DeviceStatus.cs
│   │   └── Exceptions.cs
│   └── Native/
│       ├── SaneInterop.cs
│       └── CupsInterop.cs
├── BrotherMFC.Tests/
│   ├── PrinterTests.cs
│   └── ScannerTests.cs
└── BrotherMFC.sln
```

### Dependencies
- System.Net.Http
- System.Drawing.Common (for image processing)
- Microsoft.NETFramework.ReferenceAssemblies (for older .NET)

---

## 3. Go Library

### Library Design

#### Core Types
```go
package brother

type Printer struct {
    IP       string
    Name     string
    Model    string
}

type PrintOptions struct {
    Copies     int    // Number of copies
    PaperSize  string // letter, legal, a4
    PaperSource string // tray1, manual, mpf
    Duplex     bool   // Double-sided printing
    Quality    string // draft, normal, high
}

type Scanner struct {
    IP    string
    Name  string
    Model string
}

type ScanOptions struct {
    Source    string // flatbed, adf, adf-duplex
    Resolution int  // 150, 300, 600
    Format    string // pdf, jpeg, png, tiff
}

type ScanResult struct {
    Format string
    Data   []byte
    Width  int
    Height int
}
```

### Implementation Plan

#### Phase 1: CUPS Client
- [ ] IPP protocol implementation
- [ ] CUPS HTTP client
- [ ] Print job submission
- [ ] Printer attributes

#### Phase 2: SANE Client
- [ ] CGO bindings to libsane
- [ ] Scanner enumeration
- [ ] Image scanning
- [ ] Format handling (use imaging libraries)

#### Phase 3: Convenience Functions
- [ ] High-level Printer.Scan() method
- [ ] Device auto-discovery
- [ ] Connection pooling
- [ ] Error handling

### Project Structure
```
src/go/brother/
├── printer.go      // Printer operations
├── scanner.go     // Scanner operations
├── cups.go        // CUPS client
├── sane.go        // SANE bindings
├── device.go      // Device discovery
├── options.go     // Option types
└── brother.go     // Main package
```

### Dependencies
- github.com/google/uuid (for job IDs)
- golang.org/x/net (for HTTP)

---

## 4. Rust Library

### Library Design

#### Core Traits
```rust
use std::io::Read;

pub trait Printer {
    fn print(&self, file: &mut Read, options: &PrintOptions) -> Result<JobId, PrinterError>;
    fn status(&self) -> Result<PrinterStatus, PrinterError>;
    fn cancel(&self, job_id: JobId) -> Result<(), PrinterError>;
}

pub trait Scanner {
    fn scan(&self, options: &ScanOptions) -> Result<ImageData, ScannerError>;
    fn sources(&self) -> Result<Vec<Source>, ScannerError>;
}

pub struct PrintOptions {
    pub copies: u32,
    pub paper_size: PaperSize,
    pub paper_source: PaperSource,
    pub duplex: bool,
    pub quality: Quality,
}

pub struct ScanOptions {
    pub source: ScanSource,
    pub resolution: u32,
    pub format: ImageFormat,
}
```

### Implementation Plan

#### Phase 1: FFI Bindings
- [ ] CUPS FFI bindings (cups-sys)
- [ ] SANE FFI bindings (sane-sys)
- [ ] Error handling with thiserror

#### Phase 2: Safe Wrappers
- [ ] Safe Printer wrapper
- [ ] Safe Scanner wrapper
- [ ] Builder patterns for options
- [ ] Async support with tokio

#### Phase 3: High-Level API
- [ ] PrinterManager
- [ ] ScannerManager
- [ ] Connection pooling

### Project Structure
```
src/rust/brother-mfc/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── printer/
│   │   ├── mod.rs
│   │   ├── cups.rs
│   │   └── options.rs
│   ├── scanner/
│   │   ├── mod.rs
│   │   ├── sane.rs
│   │   └── options.rs
│   ├── ffi/
│   │   ├── mod.rs
│   │   ├── cups_sys.rs
│   │   └── sane_sys.rs
│   └── error.rs
└── examples/
    ├── print.rs
    └── scan.rs
```

---

## 5. Ollama Agentic Tools

### Concept
Create Ollama-compatible tools that allow AI agents to interact with the Brother MFC-L2750DW for print and scan operations.

### Available Tools

#### Print Tool
```json
{
  "name": "brother_print",
  "description": "Print documents to Brother MFC-L2750DW printer",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string", "description": "Path to file to print"},
      "copies": {"type": "integer", "default": 1},
      "duplex": {"type": "boolean", "default": false},
      "paper_size": {"type": "string", "enum": ["letter", "legal", "a4"]},
      "paper_source": {"type": "string", "enum": ["tray1", "manual", "mpf"]}
    },
    "required": ["file_path"]
  }
}
```

#### Scan Tool
```json
{
  "name": "brother_scan",
  "description": "Scan documents from Brother MFC-L2750DW scanner",
  "parameters": {
    "type": "object",
    "properties": {
      "source": {"type": "string", "enum": ["flatbed", "adf", "adf-duplex"]},
      "resolution": {"type": "integer", "enum": [150, 300, 600]},
      "format": {"type": "string", "enum": ["pdf", "jpeg", "png", "tiff"]},
      "output_path": {"type": "string"}
    },
    "required": ["output_path"]
  }
}
```

#### Status Tool
```json
{
  "name": "brother_status",
  "description": "Get Brother MFC-L2750DW device status"
}
```

### Implementation

#### Tool Definition (JSON for Ollama)
```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "brother_print",
        "description": "Print documents to Brother MFC-L2750DW",
        "parameters": {...}
      }
    },
    {
      "type": "function", 
      "function": {
        "name": "brother_scan",
        "description": "Scan documents from Brother MFC-L2750DW",
        "parameters": {...}
      }
    },
    {
      "type": "function",
      "function": {
        "name": "brother_status",
        "description": "Get device status"
      }
    }
  ]
}
```

#### Implementation Steps
1. [ ] Create Python wrapper with Ollama tool format
2. [ ] Register tools with Ollama
3. [ ] Test with llama3/other models
4. [ ] Add error handling and retry logic
5. [ ] Document usage

---

## 6. LangChain/LangGraph Agents

### Agent Architecture

#### Print Agent
```
User Request → Intent Classification → Extract Parameters → Execute Print → Return Result
```

#### Scan Agent  
```
User Request → Intent Classification → Extract Parameters → Execute Scan → Save/Return
```

### LangChain Implementation

#### Tools
```python
from langchain.tools import Tool

brother_print_tool = Tool(
    name="brother_print",
    func=print_to_brother,
    description="Print documents to Brother MFC-L2750DW printer"
)

brother_scan_tool = Tool(
    name="brother_scan", 
    func=scan_from_brother,
    description="Scan documents from Brother MFC-L2750DW scanner"
)

brother_status_tool = Tool(
    name="brother_status",
    func=get_brother_status,
    description="Get printer/scanner status"
)
```

### LangGraph Implementation

#### Graph Structure
```python
from langgraph.graph import StateGraph, END

# Define state
class AgentState(TypedDict):
    user_request: str
    intent: str
    parameters: dict
    result: str
    error: str

# Define nodes
def classify_intent(state):
    # Use LLM to classify print vs scan
    ...

def extract_parameters(state):
    # Extract parameters from request
    ...

def execute_operation(state):
    # Call Brother library
    ...

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("classify", classify_intent)
workflow.add_node("extract", extract_parameters)
workflow.add_node("execute", execute_operation)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "extract")
workflow.add_edge("extract", "execute")
workflow.add_edge("execute", END)
```

### Implementation Steps
1. [ ] Create LangChain tools wrapper
2. [ ] Build LangGraph state machine
3. [ ] Add multi-step workflows (e.g., scan then email)
4. [ ] Implement error recovery
5. [ ] Add conversation memory

---

## 7. VS Code Integration

### Extensions

#### 1. Printer Explorer
- View available printers
- Quick print from context menu
- Print queue management

#### 2. Scanner Explorer
- View available scanners
- Quick scan to file
- Preview scanned images

#### 3. Task Provider
- Define print/scan tasks in tasks.json
- Run from command palette

### Implementation

#### package.json Configuration
```json
{
  "contributes": {
    "commands": [
      {
        "command": "brother.print",
        "title": "Brother: Print Document"
      },
      {
        "command": "brother.scan", 
        "title": "Brother: Scan Document"
      },
      {
        "command": "brother.status",
        "title": "Brother: Device Status"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "command": "brother.print",
          "when": "resourceExtname == .pdf"
        }
      ]
    }
  }
}
```

### VS Code Dev Containers
- Pre-configured dev container with all dependencies
- Include Brother library bindings

### Implementation Steps
1. [ ] Create VS Code extension project
2. [ ] Implement printer commands
3. [ ] Implement scanner commands
4. [ ] Add status bar integration
5. [ ] Create debug configurations

---

## 8. Firewall Configuration

### Rocky Linux 10 (firewalld)

#### Required Ports

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| IPP | 631 | TCP | Printer communication |
| Socket | 9100 | TCP | Raw printer port |
| HTTP | 80 | TCP | Web interface |
| SNMP | 161 | UDP | Device monitoring |
| **Scan-key-tool** | **54925** | **UDP** | Scanner discovery |
| **Scan-key-tool** | **54921** | **TCP** | Scanner data transfer |

#### Firewall Rules
```bash
# Allow IPP (CUPS)
sudo firewall-cmd --permanent --add-service=ipp

# Allow raw printing (socket)
sudo firewall-cmd --permanent --add-port=9100/tcp

# Allow web interface
sudo firewall-cmd --permanent --add-service=http

# Allow Scan-key-tool (UDP) - Required for scanner button scanning
sudo firewall-cmd --permanent --add-port=54925/udp

# Allow Scan-key-tool (TCP) - Required for scanner data transfer
sudo firewall-cmd --permanent --add-port=54921/tcp

# Reload firewall
sudo firewall-cmd --reload

# Verify rules
sudo firewall-cmd --list-all
```

#### For Local Only (Restricted to Printer IP Only)
```bash
# If printer is on same network segment
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.0.0/24" accept'

# Or specific IP (recommended)
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.0.23" accept'
```

### Implementation Steps
1. [x] Document required ports
2. [x] Create firewall script (in docs/setup/INSTALL.md)
3. [ ] Test connectivity
4. [ ] Document troubleshooting

---

## 9. SELinux Configuration

### Current Status
SELinux is enabled on Rocky Linux 10 by default.

### Required SELinux Policies

#### CUPS Printing
```bash
# Check current CUPS context
ls -laZ /etc/cups/
ps -Z | grep cups

# Allow CUPS to connect to network
sudo setsebool -P cups_execmem 1
sudo setsebool -P nis_enabled 1

# Allow printing to network printer
sudo setsebool -P printing_sync_pol 1
```

#### SANE Scanning
```bash
# Allow SANE to access network scanners
sudo setsebool -P saned_connect_any 1

# Allow scanner device access
sudo setsebool -P scanner_bind_all_ports 1
```

### Custom Policy Module (if needed)
```
# brotherd.te
module brotherd 1.0;

require {
    type cupsd_t;
    type saned_t;
    type node_t;
    class tcp_socket { connect recv_msg send_msg };
    class udp_socket { connect recv_msg send_msg };
}

# Allow CUPS to connect to network printer
allow cupsd_t node_t:tcp_socket connect;

# Allow SANE to connect to network scanner
allow saned_t node_t:udp_socket connect;
allow saned_t node_t:tcp_socket connect;
```

### Implementation Steps
1. [ ] Document SELinux booleans needed
2. [ ] Create SELinux policy module
3. [ ] Test printing with SELinux enforcing
4. [ ] Document troubleshooting

---

## 10. Router Configuration

### Network Setup Requirements

#### Static IP Reservation
- **IP Address**: 192.168.0.23
- **Recommendation**: Reserve in DHCP server
- **Alternative**: Set static IP on printer

#### Firewall Rules (if printer is on separate VLAN)
```
# Allow printer VLAN to host VLAN
iptables -A FORWARD -i br0 -o br1 -s 192.168.0.0/24 -d 192.168.1.0/24 -j ACCEPT
```

#### Port Forwarding (if accessing remotely)
```
# Not recommended for security reasons
# Instead use VPN or SSH tunnel
```

### Implementation Steps
1. [ ] Document network requirements
2. [ ] Create network setup script
3. [ ] Test from different network segments
4. [ ] Document VPN/tunnel options

---

## Summary

| Language | Phase 1 | Phase 2 | Phase 3 |
|----------|---------|---------|---------|
| Python | Core print/scan | ADF, trays, GUI | CLI, advanced features |
| .NET | IPP client | SANE bindings | High-level API |
| Go | CUPS client | SANE bindings | Convenience functions |
| Rust | FFI bindings | Safe wrappers | Async API |

### Cross-Cutting Concerns
- Firewall configuration documentation
- SELinux policy development
- Router/network setup guide
- Ollama tool definitions
- LangChain/LangGraph agents
- VS Code extension

---

## References

- [CUPS Documentation](https://www.cups.org/doc/)
- [SANE Project](http://sane-project.org/)
- [Brother Linux Drivers](https://support.brother.com/g/s/id/linux/en/)
- [Rocky Linux SELinux](https://docs.rockylinux.org/)
