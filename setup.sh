#!/bin/bash
# setup.sh — One-time environment setup for robot-ai-mission-planner
#
# Usage:
#   ./setup.sh
#
# After this finishes, just run:
#   docker compose up robot-sim
#
set -e

REPO_URL="git@github.com:adhi062002/robot-ai-mission-planner.git"
REPO_DIR="robot-ai-mission-planner"
BRANCH="add-docker-support"
OLLAMA_MODEL="llama3.2"

echo "=================================================="
echo " robot-ai-mission-planner — environment setup"
echo "=================================================="

# ---------------------------------------------------------------
# 1. Install Docker (skip if already installed)
# ---------------------------------------------------------------
if command -v docker &> /dev/null; then
    echo "[1/6] Docker already installed, skipping."
else
    echo "[1/6] Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    sudo usermod -aG docker "$USER"
    echo "Docker installed. NOTE: you may need to log out/in (or run 'newgrp docker') for group permissions to apply."
fi

# ---------------------------------------------------------------
# 2. Install NVIDIA Container Toolkit (only if an NVIDIA GPU is present)
# ---------------------------------------------------------------
if command -v nvidia-smi &> /dev/null; then
    if dpkg -l | grep -q nvidia-container-toolkit; then
        echo "[2/6] NVIDIA Container Toolkit already installed, skipping."
    else
        echo "[2/6] NVIDIA GPU detected. Installing NVIDIA Container Toolkit..."
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
          | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
        curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
          | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
          | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

        sudo apt-get update
        sudo apt-get install -y nvidia-container-toolkit
        sudo nvidia-ctk runtime configure --runtime=docker
        sudo systemctl restart docker
    fi
else
    echo "[2/6] No NVIDIA GPU detected (nvidia-smi not found). Skipping GPU toolkit — Ollama will run on CPU."
fi

# ---------------------------------------------------------------
# 3. Clone the repo (skip if already present)
# ---------------------------------------------------------------
if [ -d "$REPO_DIR" ]; then
    echo "[3/6] Repo directory already exists, skipping clone."
else
    echo "[3/6] Cloning repository..."
    git clone "$REPO_URL"
fi

cd "$REPO_DIR"

# ---------------------------------------------------------------
# 4. Checkout the correct branch
# ---------------------------------------------------------------
echo "[4/6] Checking out branch: $BRANCH"
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

# ---------------------------------------------------------------
# 5. Build images
# ---------------------------------------------------------------
echo "[5/6] Building Docker images (this can take a while the first time)..."
docker compose build

# ---------------------------------------------------------------
# 6. Start Ollama and pull the model
# ---------------------------------------------------------------
echo "[6/6] Starting Ollama and pulling model: $OLLAMA_MODEL"
docker compose up -d ollama

echo "Waiting for Ollama to become ready..."
until docker exec "$(docker compose ps -q ollama)" curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    sleep 1
done

docker exec -it "$(docker compose ps -q ollama)" ollama pull "$OLLAMA_MODEL"

echo "=================================================="
echo " Setup complete!"
echo ""
echo " To run the simulation, use:"
echo "   cd $REPO_DIR"
echo "   docker compose up robot-sim"
echo "=================================================="
