# Container Images for Building Brother MFC-L2750DW Libraries

This document describes two container images: one for musl-based builds and one for non-musl (glibc) builds.

---

## Image Comparison

| Feature | musl Image | Non-Musl (glibc) Image |
|---------|-------------|------------------------|
| **Base** | Alpine Linux | Rocky Linux 9 |
| **libc** | musl | glibc |
| **Size** | ~5-10 MB | ~80-180 MB |
| **RPM Support** | No | Yes |
| **Brother Driver Support** | No | **Yes** |
| **Use Case** | Lightweight builds | Full development |

---

## Image 1: musl Build Image (Alpine)

### When to Use
- Building lightweight binaries
- When you don't need RPM compatibility
- For web services, APIs
- **NOT compatible with Brother MFC drivers**

### Image
```bash
docker pull alpine:latest
podman pull alpine:latest
```

### Size
~5-10 MB base

### Use Cases
```dockerfile
# Dockerfile.alpine
FROM alpine:latest

# Install build tools
RUN apk add --no-cache \
    gcc \
    g++ \
    make \
    python3 \
    nodejs \
    npm \
    git

WORKDIR /build
CMD ["/bin/sh"]
```

---

## Image 2: Non-Musl Build Image (Rocky Linux)

### When to Use
- Building RPM packages
- Using Brother scanner/Printer drivers (brscan5)
- When you need glibc compatibility
- Full EL (Enterprise Linux) compatibility

### Image
```bash
# Official Rocky Linux
podman pull rockylinux/rockylinux:9

# Minimal version
podman pull rockylinux/rockylinux:9-minimal
```

### Size
- Minimal: ~80 MB
- Full: ~180 MB

### Use Cases
```dockerfile
# Dockerfile.rocky
FROM rockylinux/rockylinux:9

# Install development tools
RUN dnf -y install \
    gcc \
    gcc-c++ \
    make \
    python3 \
    python3-pip \
    git \
    go \
    meson \
    ninja-build \
    && dnf clean all

# Install Brother dependencies
RUN dnf -y install \
    cups-devel \
    libsane-devel \
    && dnf clean all

WORKDIR /build
CMD ["/bin/bash"]
```

---

## Complete Build Images

### Alpine (musl) - For Non-Brother Builds

```dockerfile
# Dockerfile.alpine
FROM alpine:3.19

# Build tools
RUN apk add --no-cache \
    build-base \
    cmake \
    ninja \
    python3 \
    nodejs \
    npm \
    go \
    git \
    curl \
    wget

# Node.js specific
RUN npm install -g typescript

WORKDIR /app
```

### Rocky Linux 9 (glibc) - For Brother/Full Development

```dockerfile
# Dockerfile.rocky
FROM rockylinux/rockylinux:9

# Enable CRB (CodeReady Builder) for additional packages
RUN dnf -y install dnf-plugins-core && \
    dnf config-manager --set-enabled crb

# Development tools
RUN dnf -y install \
    gcc \
    gcc-c++ \
    make \
    cmake \
    meson \
    ninja-build \
    python3 \
    python3-pip \
    python3-devel \
    go \
    git \
    curl \
    wget \
    podman \
    && dnf clean all

# Install Node.js
RUN curl -fsSL https://rpm.nodesource.com/setup_20.x | bash - && \
    dnf install -y nodejs && \
    dnf clean all

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Install .NET
RUN dnf -y install https://packages.microsoft.com/config/rhel/9/packages-microsoft-prod.rpm && \
    dnf install -y dotnet-sdk-8.0 && \
    dnf clean all

WORKDIR /app
```

---

## Quick Reference

### musl Image (Alpine)
```bash
# Pull
podman pull alpine:3.19

# Build
podman build -f Dockerfile.alpine -t my-app:alpine .

# Run
podman run -it --rm my-app:alpine /bin/sh
```

### Non-Musl Image (Rocky Linux)
```bash
# Pull
podman pull rockylinux/rockylinux:9

# Build
podman build -f Dockerfile.rocky -t my-app:rocky .

# Run
podman run -it --rm my-app:rocky /bin/bash
```

---

## For Brother MFC-L2750DW Development

**Use Rocky Linux 9 (non-musl)** because:
- Brother drivers (brscan5) are RPM-based
- CUPS/SANE require glibc
- Full compatibility with EL ecosystem

```bash
podman pull rockylinux/rockylinux:9
```
