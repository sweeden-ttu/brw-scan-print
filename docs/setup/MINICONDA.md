# SETUP.md - Miniconda Python Environment Setup

This guide covers setting up Python virtual environments using Miniconda for all projects.

## Why Miniconda?

Miniconda is preferred over venv because:
- Better dependency management with conda packages
- Works across different Linux distributions
- Easier GPU library management (cuda, cudnn)
- Compatible with HPCC environment

## Installation

### macOS / Linux

```bash
# Download Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install (answer 'yes' to initialization)
bash Miniconda3-latest-Linux-x86_64.sh

# Initialize for your shell
source ~/.bashrc  # or ~/.zshrc for zsh
```

### HPCC (RedRaider)

```bash
# On login node or in job script
module load gcc
module load cuda

# Install Miniconda to home directory
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
source $HOME/miniconda3/etc/profile.d/conda.sh
```

## Creating Environments

### Basic Python Environment

```bash
# Create environment
conda create -n myproject python=3.12 -y

# Activate
conda activate myproject

# Deactivate
conda deactivate
```

### With GPU Support (CUDA)

```bash
# Create environment with CUDA
conda create -n gpu-project python=3.12 cudatoolkit=11.8 -y

# Or use pip for CUDA
conda create -n gpu-project python=3.12 -y
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Project-Specific Environment

```bash
# brw-scan-print
conda create -n brw-scan python=3.12 pip -y
conda activate brw-scan
pip install pycups python-sane pillow pygobject

# OllamaHpcc
conda create -n ollama python=3.12 pip -y
conda activate ollama
pip install langchain langchain-community langsmith ollama python-dotenv requests

# GlobPretect
conda create -n vpn python=3.12 pip -y
conda activate vpn
pip install paramiko requests python-dotenv
```

## Environment Management

### List Environments

```bash
conda env list
```

### Export Environment

```bash
conda activate myproject
conda env export > environment.yml
```

### Import Environment

```bash
conda env create -f environment.yml
```

### Remove Environment

```bash
conda env remove -n myproject -y
```

## Using with VS Code / Cursor

1. Open VS Code / Cursor
2. Select Python interpreter: `Cmd+Shift+P` → "Python: Select Interpreter"
3. Choose conda environment: `~/miniconda3/envs/projectname/bin/python`

## Using with PyCharm

1. File → Settings → Project → Python Interpreter
2. Add → Conda Environment → Existing environment
3. Select: `~/miniconda3/envs/projectname/bin/python`

## HPCC Slurm Job with Conda

```bash
#!/bin/bash
#SBATCH -J myjob
#SBATCH -p matador
#SBATCH --gpus-per-node=1
#SBATCH -t 02:00:00

# Load system modules
module load gcc cuda

# Initialize conda
source $HOME/miniconda3/etc/profile.d/conda.sh

# Activate environment
conda activate gpu-project

# Run Python script
python myscript.py
```

## Common Issues

### Issue: Conda command not found

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/miniconda3/bin:$PATH"
source ~/.bashrc
```

### Issue: SSL certificate errors

```bash
conda config --set ssl_verify false
```

### Issue: GPU not detected

```bash
# Verify CUDA
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

## Quick Start Commands

```bash
# Install Miniconda
bash Miniconda3-latest-Linux-x86_64.sh

# Create project environment
conda create -n PROJECT python=3.12 -y

# Activate
conda activate PROJECT

# Install dependencies
pip install package1 package2

# Export for sharing
conda env export > environment.yml
```
