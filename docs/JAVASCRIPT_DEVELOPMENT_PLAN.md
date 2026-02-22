# JavaScript/TypeScript Library Development Plan

## Project Overview

Create a JavaScript/TypeScript library for Brother MFC-L2750DW that works in Node.js and browsers, with MCP server integration and Ollama tool support.

**Device**: Brother MFC-L2750DW at 192.168.0.23  
**Target**: Node.js, Browser, MCP Servers, Ollama

---

## Table of Contents

1. [Architecture](#1-architecture)
2. [Node.js Library](#2-nodejs-library)
3. [Browser Library](#3-browser-library)
4. [MCP Server](#4-mcp-server)
5. [Ollama Tools](#5-ollama-tools)
6. [Publishing](#6-publishing)

---

## 1. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    JavaScript/TypeScript Ecosystem            │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Node.js    │  │  Browser    │  │   MCP Server       │  │
│  │  Library    │  │  Library    │  │   (JSON-RPC)       │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │              │
│         └────────────────┴─────────────────────┘              │
│                          │                                    │
│                  ┌─────────▼─────────┐                        │
│                  │  Core API Layer  │                        │
│                  │  - Printer        │                        │
│                  │  - Scanner       │                        │
│                  │  - Device        │                        │
│                  └─────────┬─────────┘                        │
│                            │                                  │
│         ┌──────────────────┼──────────────────┐             │
│         │                  │                  │             │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐      │
│  │ CUPS/IPP    │  │ SANE        │  │ brscan-skey│      │
│  │ HTTP Client │  │ HTTP Client │  │ Network     │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Node.js Library

### Project Structure
```
src/javascript/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # Main entry
│   ├── printer/
│   │   ├── PrinterClient.ts  # CUPS/IPP client
│   │   ├── PrinterManager.ts # High-level API
│   │   └── types.ts         # Printer types
│   ├── scanner/
│   │   ├── ScannerClient.ts  # SANE client
│   │   ├── ScannerManager.ts # High-level API
│   │   └── types.ts         # Scanner types
│   ├── device/
│   │   ├── DeviceClient.ts   # Device discovery
│   │   └── types.ts         # Device types
│   └── common/
│       ├── HttpClient.ts     # HTTP wrapper
│       ├── config.ts        # Configuration
│       └── errors.ts        # Custom errors
├── dist/                     # Compiled JS
└── test/
    ├── printer.test.ts
    └── scanner.test.ts
```

### Core Types

```typescript
// src/printer/types.ts
export interface PrintOptions {
  copies?: number;
  paperSize?: 'letter' | 'legal' | 'a4';
  paperSource?: 'tray1' | 'manual' | 'mpf';
  duplex?: boolean;
  quality?: 'draft' | 'normal' | 'high';
}

export interface PrintJob {
  id: number;
  title: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  createdAt: Date;
}

export interface PrinterInfo {
  name: string;
  uri: string;
  model: string;
  status: 'idle' | 'printing' | 'error';
}

// src/scanner/types.ts
export interface ScanOptions {
  source?: 'flatbed' | 'adf' | 'adf-duplex';
  resolution?: 150 | 300 | 600;
  format?: 'pdf' | 'jpeg' | 'png' | 'tiff';
}

export interface ScanResult {
  data: Buffer;
   width: number format: string;
;
  height: number;
}

export interface ScannerInfo {
  name: string;
  vendor: string;
  model: string;
  sources: string[];
}
```

### Implementation

#### Phase 1: Core Library
- [ ] Set up Node.js project with TypeScript
- [ ] Implement HTTP client wrapper
- [ ] Implement CUPS/IPP printer client
- [ ] Implement SANE scanner client
- [ ] Add error handling

#### Phase 2: High-Level API
- [ ] PrinterManager class
- [ ] ScannerManager class
- [ ] Device discovery
- [ ] Configuration management

#### Phase 3: Advanced Features
- [ ] Event emitters for job status
- [ ] Retry logic
- [ ] Connection pooling

### package.json

```json
{
  "name": "@sweeden-ttu/brother-mfc",
  "version": "0.1.0",
  "description": "Brother MFC-L2750DW JavaScript/TypeScript library",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src --ext .ts"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0",
    "jest": "^29.0.0",
    "eslint": "^8.0.0"
  }
}
```

---

## 3. Browser Library

### Architecture
- [ ] WebAssembly bindings (optional)
- [ ] REST API wrapper for browser
- [ ] Web Worker for long operations

### Browser Compatibility
```typescript
// Can use in browser via:
// 1. Bundled with webpack/rollup
// 2. Direct from CDN
// 3. As MCP server client
```

---

## 4. MCP Server

### What is MCP?
Model Context Protocol (MCP) - A standard for AI agents to interact with tools.

### MCP Server Implementation

```typescript
// src/mcp-server/index.ts
import { McpServer, StdioServer } from '@modelcontextprotocol/sdk';

const server = new McpServer({
  name: 'brother-mfc',
  version: '1.0.0'
});

// Tool: print_document
server.tool('print_document', {
  title: 'Print Document',
  description: 'Print a document to Brother MFC-L2750DW',
  inputSchema: {
    type: 'object',
    properties: {
      filePath: { type: 'string', description: 'Path to file' },
      copies: { type: 'number', default: 1 },
      duplex: { type: 'boolean', default: false },
      paperSize: { type: 'string', enum: ['letter', 'legal', 'a4'] }
    },
    required: ['filePath']
  }
}, async (params) => {
  const { PrinterManager } = await import('../printer');
  const printer = new PrinterManager({ ip: '192.168.0.23' });
  const jobId = await printer.print(params.filePath, {
    copies: params.copies,
    duplex: params.duplex,
    paperSize: params.paperSize
  });
  return { content: [{ type: 'text', text: `Print job ${jobId} submitted` }] };
});

// Tool: scan_document
server.tool('scan_document', {
  title: 'Scan Document',
  description: 'Scan a document from Brother MFC-L2750DW',
  inputSchema: {
    type: 'object',
    properties: {
      source: { type: 'string', enum: ['flatbed', 'adf', 'adf-duplex'] },
      resolution: { type: 'number', enum: [150, 300, 600] },
      format: { type: 'string', enum: ['pdf', 'jpeg', 'png'] },
      outputPath: { type: 'string' }
    },
    required: ['outputPath']
  }
}, async (params) => {
  const { ScannerManager } = await import('../scanner');
  const scanner = new ScannerManager({ ip: '192.168.0.23' });
  const result = await scanner.scan(params);
  // Save to file...
  return { content: [{ type: 'text', text: `Scanned to ${params.outputPath}` }] };
});

// Tool: get_device_status
server.tool('get_device_status', {
  title: 'Device Status',
  description: 'Get Brother MFC-L2750DW status'
}, async () => {
  // Get printer and scanner status
  return { content: [{ type: 'text', text: 'Printer: Ready\nScanner: Ready' }] };
});

// Start server
new StdioServer().start(server);
```

### MCP Server Structure
```
src/mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts           # Main server
│   ├── tools/
│   │   ├── print.ts
│   │   ├── scan.ts
│   │   └── status.ts
│   └── brother/
│       └── client.ts     # Brother API client
└── dist/
```

---

## 5. Ollama Tools

### Ollama Tool Format

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "brother_print",
        "description": "Print documents to Brother MFC-L2750DW",
        "parameters": {
          "type": "object",
          "properties": {
            "file_path": { "type": "string" },
            "copies": { "type": "integer", "default": 1 },
            "duplex": { "type": "boolean", "default": false },
            "paper_size": { "type": "string", "enum": ["letter", "legal", "a4"] }
          },
          "required": ["file_path"]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "brother_scan",
        "description": "Scan documents from Brother MFC-L2750DW",
        "parameters": {
          "type": "object",
          "properties": {
            "source": { "type": "string", "enum": ["flatbed", "adf", "adf-duplex"] },
            "resolution": { "type": "integer", "enum": [150, 300, 600] },
            "format": { "type": "string", "enum": ["pdf", "jpeg", "png"] },
            "output_path": { "type": "string" }
          },
          "required": ["output_path"]
        }
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

### Ollama Integration

```typescript
// src/ollama/tools.ts
import { ToolDefinition } from './types';

export const brotherTools: ToolDefinition[] = [
  {
    name: 'brother_print',
    description: 'Print documents to Brother MFC-L2750DW printer',
    parameters: {
      type: 'object',
      properties: {
        file_path: { type: 'string', description: 'Path to file to print' },
        copies: { type: 'integer', description: 'Number of copies', default: 1 },
        duplex: { type: 'boolean', description: 'Double-sided printing', default: false },
        paper_size: { type: 'string', enum: ['letter', 'legal', 'a4'], default: 'letter' }
      },
      required: ['file_path']
    }
  },
  {
    name: 'brother_scan',
    description: 'Scan documents from Brother MFC-L2750DW scanner',
    parameters: {
      type: 'object',
      properties: {
        source: { type: 'string', enum: ['flatbed', 'adf', 'adf-duplex'], default: 'flatbed' },
        resolution: { type: 'integer', enum: [150, 300, 600], default: 300 },
        format: { type: 'string', enum: ['pdf', 'jpeg', 'png'], default: 'pdf' },
        output_path: { type: 'string', description: 'Where to save scan' }
      },
      required: ['output_path']
    }
  },
  {
    name: 'brother_status',
    description: 'Get current printer/scanner status',
    parameters: { type: 'object', properties: {} }
  }
];
```

### Pluggable Ollama Architecture

```typescript
// src/ollama/index.ts
import { brotherTools } from './tools';
import { BrotherClient } from '../common/client';

export class OllamaPlugin {
  private client: BrotherClient;
  
  constructor(ip: string = '192.168.0.23') {
    this.client = new BrotherClient(ip);
  }
  
  getTools() {
    return brotherTools;
  }
  
  async executeTool(toolName: string, params: Record<string, any>) {
    switch (toolName) {
      case 'brother_print':
        return this.client.print(params.file_path, params);
      case 'brother_scan':
        return this.client.scan(params);
      case 'brother_status':
        return this.client.getStatus();
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }
}

// Export for use with Ollama
export const brotherMfc = new OllamaPlugin();
```

---

## Ollama Port Mappings (Fixed Ports - VPN Required)

**IMPORTANT**: Always use fixed ports 55077 or 66044. Never use default port 11434.

| Variable | Port | Model | Purpose |
|----------|------|-------|---------|
| GRANITE_URL | 55077 | granite4 | Agentic tasks |
| QWEN_URL | 66044 | qwen2.5-coder | Code generation |

### Environment Setup

```bash
# In your code / .env file
GRANITE_URL = "http://localhost:55077"
QWEN_URL = "http://localhost:66044"
```

### Podman Container Launch

```bash
# granite4 on 55077
podman run -d --name ollama-granite4 -p 55077:55077 \
  -v ollama:/root/.ollama \
  -e OLLAMA_HOST=0.0.0.0:55077 \
  quay.io/ollama/ollama serve

# qwen-coder on 66044
podman run -d --name ollama-qwen -p 66044:66044 \
  -v ollama:/root/.ollama \
  -e OLLAMA_HOST=0.0.0.0:66044 \
  quay.io/ollama/ollama serve
```

### LangChain Integration

```python
import os
from langchain_community.llms import Ollama

PORTS = {
    "granite": "http://localhost:55077",
    "think": "http://localhost:55088",
    "qwen": "http://localhost:66044",
    "code": "http://localhost:66033"
}

llm = Ollama(model="granite4", base_url=PORTS["granite"])
```

---

## 6. Publishing

### Package Names

| Package | Registry | Name |
|---------|----------|------|
| Node.js | npm | `@sweeden-ttu/brother-mfc` |
| MCP Server | npm | `@sweeden-ttu/brother-mfc-mcp` |
| Ollama Tools | npm | `@sweeden-ttu/brother-mfc-ollama` |

### Publishing Commands

```bash
# Build all packages
npm run build

# Publish to npm
npm publish --access public

# Or for scoped packages
npm publish --access public --scope @sweeden-ttu
```

### GitHub Packages

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | podman login ghcr.io -u $GITHUB_ACTOR --password-stdin

# Build and push
podman build -t ghcr.io/sweeden-ttu/brother-mfc:latest .
podman push ghcr.io/sweeden-ttu/brother-mfc:latest
```

### Publishing Workflow

```yaml
# .github/workflows/publish.yml
name: Publish

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      
      - run: npm ci
      - run: npm run build
      - run: npm test
      - run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## Summary

| Component | Language | Registry | Status |
|-----------|----------|----------|--------|
| Node.js Library | TypeScript | npm (@sweeden-ttu) | To do |
| Browser Library | TypeScript | npm (@sweeden-ttu) | To do |
| MCP Server | TypeScript | npm (@sweeden-ttu) | To do |
| Ollama Tools | TypeScript | npm (@sweeden-ttu) | To do |
| Docker Image | Dockerfile | ghcr.io/sweeden-ttu | To do |

---

## Next Steps

1. [ ] Create repository structure
2. [ ] Initialize Node.js project
3. [ ] Implement core library
4. [ ] Create MCP server
5. [ ] Create Ollama tools
6. [ ] Publish to npm
