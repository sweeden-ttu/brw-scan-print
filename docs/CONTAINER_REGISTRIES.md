# Container Registry & Image Guide

This document provides information about popular container registries and recommended images for Rocky Linux 10 development.

---

## Popular Container Registries

### 1. Docker Hub (docker.io)
- **URL**: https://hub.docker.com
- **Official**: Yes
- **Authentication**: Optional (for private repos)
- **Usage**: `docker pull nginx:latest`

### 2. Quay (quay.io)
- **URL**: https://quay.io
- **Owned by**: Red Hat
- **Best for**: Enterprise/CentOS/Rocky images
- **Usage**: `podman pull quay.io/centos/centos:stream9`

### 3. GitHub Container Registry (ghcr.io)
- **URL**: https://ghcr.io
- **Owned by**: GitHub
- **Best for**: Open source projects
- **Usage**: `podman pull ghcr.io/namespace/image:latest`

### 4. Google Container Registry (gcr.io)
- **URL**: https://gcr.io
- **Owned by**: Google Cloud
- **Best for**: GCP workloads
- **Usage**: `podman pull gcr.io/project-id/image:latest`

### 5. NVIDIA GPU Cloud (nvcr.io)
- **URL**: https://nvcr.io
- **Owned by**: NVIDIA
- **Best for**: CUDA/AI workloads
- **Usage**: `podman pull nvcr.io/nvidia/cuda:12.4.0-base-ubuntu22.04`

---

## Recommended Minimal Images for Rocky Linux 10 Development

### Top 3 Recommendations

| Rank | Image | Size | Use Case |
|------|-------|------|----------|
| **1** | `rockylinux/rockylinux:9-minimal` | ~80 MB | Base system, minimal footprint |
| **2** | `rockylinux/rockylinux:9` | ~180 MB | Full system with dnf/ Package manager |
| **3** | `alpine:latest` | ~7 MB | Lightweight, musl-based (NOT EL compatible) |

### Why Rocky Linux 9 over 10?

- Rocky Linux 10 (EL10) is very new
- Most available images are EL9-based
- Better ecosystem support for EL9
- Rocky 9 is ABI-compatible with most EL10 applications

---

## Image Categories

### Minimal Base Images

```bash
# Tiny - just enough to run
podman pull rockylinux/rockylinux:9-minimal

# Regular - includes dnf/package manager
podman pull rockylinux/rockylinux:9

# Full - includes everything
podman pull rockylinux/rockylinux:9.3
```

### Development Images

```bash
# CentOS Stream 9 (Rocky-compatible)
podman pull quay.io/centos/centos:stream9

# AlmaLinux
podman pull almalinux:9

# Fedora (bleeding edge)
podman pull fedora:39
```

### HPC/Development Images

```bash
# Scientific computing base
podman pull rockylinux/rockylinux:9

# Add your own layers with:
# RUN dnf install -y gcc gcc-c++ make python3
```

---

## Alpine vs Rocky Linux

| Feature | Alpine | Rocky Linux |
|---------|---------|-------------|
| **Size** | ~5-10 MB | ~80-180 MB |
| **Package Manager** | apk | dnf/yum |
| ** libc** | musl | glibc |
| **EL Compatibility** | No | Yes |
| **RPM Support** | No | Yes |
| **Brother Driver Support** | No | **Yes** |

**Important**: Brother drivers (brscan5) are RPM-based and require glibc. Use Rocky Linux, not Alpine.

---

## Image Tags Explained

```bash
# Latest stable
podman pull rockylinux/rockylinux:9

# Specific version
podman pull rockylinux/rockylinux:9.3.20231119

# Minimal variant
podman pull rockylinux/rockylinux:9-minimal

# Stream version
podman pull rockylinux/rockylinux:stream9
```

---

## Finding Images

### Search Commands

```bash
# Search Docker Hub
podman search rockylinux

# Search Quay
podman search quay.io/rockylinux

# List available tags
podman manifest inspect rockylinux/rockylinux:9 2>/dev/null | grep -o '"tag": "[^"]*"' | head -20
```

### Official Image Locations

| Distribution | Docker Hub | Quay.io |
|--------------|------------|----------|
| Rocky Linux | `rockylinux/rockylinux` | N/A |
| CentOS | `centos/centos` | `quay.io/centos/centos` |
| AlmaLinux | `almalinux/almalinux` | N/A |
| Fedora | `fedora` | N/A |
| Ubuntu | `ubuntu` | N/A |
| Debian | `debian` | N/A |

---

## Building Your Own Image

### Using Rocky Linux Base

```dockerfile
# Dockerfile
FROM rockylinux/rockylinux:9

# Install development tools
RUN dnf -y install \
    gcc \
    gcc-c++ \
    make \
    python3 \
    python3-pip \
    git \
    && dnf clean all

# Set working directory
WORKDIR /app

# Copy application
COPY . .

# Default command
CMD ["/bin/bash"]
```

### Build Command

```bash
# Build the image
podman build -t my-dev-env:latest .

# Or with Docker
docker build -t my-dev-env:latest .
```

---

## Best Practices

### 1. Use Minimal Base
```dockerfile
# Good - minimal base
FROM rockylinux/rockylinux:9-minimal

# Avoid - large base with everything
FROM rockylinux/rockylinux:9
```

### 2. Clean Up in Same Layer
```dockerfile
# Good - clean in same layer
RUN dnf install -y package && dnf clean all

# Bad - leaves cache
RUN dnf install -y package
RUN dnf clean all
```

### 3. Use Specific Tags
```dockerfile
# Good - reproducible
FROM rockylinux/rockylinux:9.3.20231119

# Avoid - may change
FROM rockylinux/rockylinux:9
FROM rockylinux/rockylinux:latest
```

### 4. Multi-stage Builds
```dockerfile
# Build stage
FROM rockylinux/rockylinux:9 AS builder
RUN dnf install -y gcc && dnf clean all

# Runtime stage
FROM rockylinux/rockylinux:9-minimal
COPY --from=builder /usr/bin/gcc /usr/bin/
```

---

## Quick Reference

### Most Useful Commands

```bash
# Pull image
podman pull rockylinux/rockylinux:9

# List images
podman images

# Run interactive
podman run -it rockylinux/rockylinux:9 /bin/bash

# Run with volume
podman run -v ~/project:/app -it rockylinux/rockylinux:9

# Save/Load for offline use
podman save -o image.tar rockylinux/rockylinux:9
podman load -i image.tar

# Tag for local registry
podman tag rockylinux/rockylinux:9 localhost/myimage:latest
```

---

## For Brother MFC-L2750DW Development

Use **Rocky Linux 9** (not Alpine) because:

1. Brother drivers are RPM-based
2. brscan5 requires glibc (not musl)
3. CUPS/SANE libraries are available
4. EL-compatible package ecosystem

```bash
# Recommended base for this project
podman pull rockylinux/rockylinux:9
```
