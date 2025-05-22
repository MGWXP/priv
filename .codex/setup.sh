#!/usr/bin/env bash
set -euo pipefail

# Update APT index before network is cut
apt-get update -y

# Install minimal system packages that ship wheels
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3-pytest \
    python3-flake8 \
    python3-pip \
    python3-setuptools \
    python3-wheel

# Ensure latest pip
python3 -m pip install --upgrade pip

# Remove matplotlib from requirements if present
grep -v '^matplotlib' requirements.txt > requirements.tmp || true
mv requirements.tmp requirements.txt

# Install dependencies from requirements file
python3 -m pip install -r requirements.txt || true

exit 0
