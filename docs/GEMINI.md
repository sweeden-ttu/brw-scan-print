# GEMINI.md - Gemini AI Development Guide

This document provides guidance for Gemini AI when working on this project.

## Project Context

This is a multi-project toolchain:
- **GlobPretect**: VPN connection manager for TTU HPCC
- **OllamaHpcc**: Ollama server/client for RedRaider GPU clusters
- **brw-scan-print**: Brother MFC-L2750DW GNOME scanner & printer app

## Gemini Code Assist - Agent Mode (2025-2026)

### Overview

Gemini Code Assist now supports **Agent Mode** for enhanced pair programming in VS Code and IntelliJ IDEs. Agent Mode allows Gemini to:
- Analyze entire codebases and implement multi-file features
- Propose plans and await approval before changes
- Use MCP servers for extended capabilities
- Handle complex, multi-step tasks autonomously

### Key Features (October 2025 Update)

| Feature | Description |
|---------|-------------|
| **Agent Mode** | Multi-step autonomous coding with Gemini 2.5 Pro |
| **MCP Support** | Model Context Protocol integration (1800+ servers) |
| **1M Context** | Understand entire codebases with Gemini 2.5 Flash/Pro |
| **Free Tier** | 180K free completions/month (90x GitHub Copilot) |

### Agent Mode Workflow

```
User Prompt → Gemini API + Available Tools → Plan Generation → User Approval → Execution
```

### Model Selection

| Model | Context | Best For |
|-------|---------|----------|
| Gemini 2.5 Pro | 1M tokens | Complex reasoning, full codebase |
| Gemini 2.5 Flash | 1M tokens | Speed-optimized tasks |

### MCP Integration (October 2025)

Gemini now supports Model Context Protocol for connecting to external tools:

```json
// .gemini/config.json
{
  "workspaces": ["packages/web", "packages/mobile"],
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

## Fixed Ollama Ports (VPN Required)

**IMPORTANT**: Always use fixed ports 55077 or 66044. Never use default port 11434.

| Port | Model | Agent Role |
|------|-------|------------|
| 55077 | granite4 | Agentic - high-level decision making, tool selection |
| 66044 | qwen2.5-coder | Coding - code generation, debugging |
| 66033 | codellama | Plain English - communication, documentation |

## Gemini-Specific Guidelines

### Model Selection by Task

```python
# For code generation/debugging
port = 66044  # qwen-coder

# For complex reasoning
port = 55088  # deepseek-r1

# For general tasks
port = 55077  # granite4

# For documentation
port = 66033  # codellama
```

### Context Management

When working with Gemini:
1. Set context window appropriately for task (up to 1M tokens)
2. Use streaming for long generations
3. Implement proper error handling

### API Integration

```python
import requests

PORTS = {
    "agentic": 55077,
    "large": 55088,
    "coding": 66044,
    "plain": 66033
}

def query_gemini(prompt, task_type="coding"):
    port = PORTS[task_type]
    response = requests.post(
        f"http://localhost:{port}/api/generate",
        json={"model": "qwen2.5-coder", "prompt": prompt}
    )
    return response.json()
```

## Development Workflow

### 1. Analysis Phase
- Use port 55088 for deep reasoning
- Analyze requirements thoroughly

### 2. Implementation Phase
- Use port 66044 for code generation
- Generate clean, documented code

### 3. Documentation Phase
- Use port 66033 for plain English explanations
- Create clear documentation

### 4. Testing Phase
- Use port 55077 for test generation
- Validate implementations

## GitHub Integration

**Repository**: github.com/sweeden-ttu/{repo_name}

```bash
# Clone with SSH
git clone git@github.com:sweeden-ttu/brw-scan-print.git
git clone git@github.com:sweeden-ttu/GlobPretect.git
git clone git@github.com:sweeden-ttu/OllamaHpcc.git
```

## Collaboration with Claude

When working alongside Claude:
1. Gemini handles complex reasoning tasks (port 55088)
2. Claude handles implementation (port 66044)
3. Share context via GitHub issues

## Important Notes

- Always use fixed ports: 55077 (granite4), 66044 (qwen-coder)
- Never use default port 11434
- VPN must be active for all Ollama operations
- All ports require GlobPretect VPN running
- MCP migration (Tool Calling API → MCP) required by March 2026
