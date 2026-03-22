---
title: 🦙 Ollama — Setup Guide
nav_order: 4
---

# 🦙 Ollama — Setup Guide

Ollama is an open-source runtime for running large language models (LLMs) locally, without any cloud dependency. It runs as a background service and exposes a REST API on port `11434`.

> **Minimum requirements:** 8 GB RAM (16 GB+ recommended) · Internet connection for initial model download · Compatible GPU for accelerated inference (optional but recommended)

---

## 📦 1. Installation

### 🪟 Windows

1. Download the installer from [https://ollama.com/download](https://ollama.com/download)
2. Run the `.exe` file and follow the on-screen instructions
3. The installer automatically adds `ollama` to the system `PATH`
4. After installation, Ollama appears in the system tray and starts as a background service

**Verify installation:**
```powershell
ollama --version
```

---

### 🍎 macOS

> Requires **macOS 14 Sonoma** or later.

1. Download the `.zip` from [https://ollama.com/download](https://ollama.com/download)
2. Unzip the archive and drag `Ollama.app` into `/Applications`
3. Launch the application — an icon will appear in the menu bar
4. On first launch, install the CLI tools when prompted

**Alternatively, via Homebrew:**
```bash
brew install ollama
```

**Verify installation:**
```bash
ollama --version
```

---

### 🐧 Linux

**One-line installation (recommended):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

The script installs the Ollama binary and automatically registers a `systemd` service that starts on system boot.

**Check service status:**
```bash
sudo systemctl status ollama
```

**Start / stop / restart manually:**
```bash
sudo systemctl start ollama
sudo systemctl stop ollama
sudo systemctl restart ollama
```

**Verify installation:**
```bash
ollama --version
```

---

## 🤖 2. Downloading and Running Models

### Pulling a model

```bash
# Download a model without running it
ollama pull qwen2.5:14b

# Download a specific version / quantization
ollama pull llama3.2:3b-instruct-q4_K_M
```

> Models are stored locally and available offline after the initial download.

### Running a model (interactive chat)

```bash
ollama run qwen2.5:14b
```

> If the model has not been pulled yet, `run` will automatically pull it first.

### Useful commands

```bash
ollama list                   # List all downloaded models
ollama show qwen2.5:14b       # Show model details (architecture, parameters)
ollama ps                     # Show models currently loaded in memory
ollama stop qwen2.5:14b       # Unload a model from memory
ollama rm qwen2.5:14b         # Delete a model from disk
```

---

## ⚡ 3. GPU Support

Ollama automatically detects an available GPU and uses it when conditions are met. GPU acceleration significantly increases inference speed.

### NVIDIA (CUDA)

**Requirements:** NVIDIA drivers + CUDA Toolkit

```bash
# Verify GPU availability
nvidia-smi

# Check whether Ollama is using the GPU
ollama ps
# The PROCESSOR column should show "GPU" or "GPU+CPU"
```

**Recommended:** Install the [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) for your driver version before installing Ollama.

For multi-GPU setups, Ollama automatically distributes model layers across GPUs when a model doesn't fit on a single card. To control which GPUs are used:

```bash
export CUDA_VISIBLE_DEVICES=0        # Use only the first GPU
export CUDA_VISIBLE_DEVICES=0,1      # Use both GPUs
```

---

### 🍎 Apple Silicon (Metal)

On Macs with M-series chips (M1/M2/M3/M4), Ollama automatically uses **Metal** GPU acceleration with no additional configuration required. The unified memory architecture makes Metal particularly efficient — there is no VRAM/RAM split.

---

## 🌐 4. REST API

The Ollama server listens on `http://localhost:11434` by default. All model interactions can be performed via HTTP requests.

### Text generation

```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:14b",
    "prompt": "Extract symptoms from: Patient reports fever and headache.",
    "stream": false
  }'
```

### Chat (multi-turn)

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:14b",
    "messages": [
      { "role": "system", "content": "You are a medical NLP assistant." },
      { "role": "user", "content": "Extract symptoms from the following text..." }
    ],
    "stream": false
  }'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen2.5:14b",
        "messages": [
            {"role": "system", "content": "You are a medical NLP assistant."},
            {"role": "user", "content": "Extract symptoms from: ..."}
        ],
        "stream": False
    }
)

data = response.json()
print(data["message"]["content"])
```

Or via the OpenAI-compatible SDK (Ollama exposes an OpenAI-compatible endpoint):
 
```bash
pip install openai
```
 
```python
from openai import OpenAI
 
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # required by the SDK, but ignored by Ollama
)
 
response = client.chat.completions.create(
    model="qwen2.5:14b",
    messages=[
        {"role": "system", "content": "You are a medical NLP assistant."},
        {"role": "user", "content": "Extract symptoms from: ..."}
    ]
)
 
print(response.choices[0].message.content)
```

---

## ⚙️ 5. Environment Variables
 
When using Ollama as an OpenAI-compatible server, only a subset of environment variables are relevant. The variables below affect the **server itself** — network exposure, model storage, memory behavior, and GPU acceleration — all of which directly impact how your OpenAI SDK client connects and performs.
 
> Variables related to internal concurrency (`OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_QUEUE`, `OLLAMA_MAX_LOADED_MODELS`) and low-level cache tuning (`OLLAMA_KV_CACHE_TYPE`, `OLLAMA_ORIGINS`) are server-side concerns and are not needed in this context.
 
### Reference table
 
| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `127.0.0.1:11434` | IP address and port the server listens on — set to `0.0.0.0:11434` to expose to other devices |
| `OLLAMA_MODELS` | `~/.ollama/models` | Path to the directory where models are stored |
| `OLLAMA_KEEP_ALIVE` | `5m` | How long a model stays loaded in memory after the last request — increase to reduce cold-start latency |
| `OLLAMA_FLASH_ATTENTION` | `0` | Enable Flash Attention to reduce VRAM usage (set to `1`) |
| `CUDA_VISIBLE_DEVICES` | all | Which NVIDIA GPUs are visible to Ollama |
| `OLLAMA_DEBUG` | `0` | Enable verbose server logging — useful when diagnosing connection issues from the client (set to `1`) |
 
---

### Configuration per OS

#### 🐧 Linux — `systemd` service

```bash
sudo systemctl edit ollama
```

In the editor that opens, add:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MODELS=/data/ollama/models"
Environment="OLLAMA_KEEP_ALIVE=10m"
Environment="OLLAMA_FLASH_ATTENTION=1"
```

Apply the changes:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

#### 🍎 macOS — `launchctl`

```bash
launchctl setenv OLLAMA_HOST "0.0.0.0"
launchctl setenv OLLAMA_KEEP_ALIVE "10m"
```

Then restart the Ollama application from the Applications folder.

---

#### 🪟 Windows — Environment Variables

1. Quit Ollama from the system tray (right-click → Quit)
2. Open **Settings** → search for "environment variables"
3. Click **Edit environment variables for your account**
4. Add or edit the desired variables (e.g. `OLLAMA_HOST` = `0.0.0.0:11434`)
5. Click OK and relaunch Ollama from the Start menu

---

## 🔌 6. Project Integration

> ⚠️ **Security warning:** Ollama has no built-in authentication. Exposing it on `0.0.0.0` makes the API accessible to anyone on the same network — or the internet if your firewall is open. Do not expose Ollama publicly without a reverse proxy (e.g. Nginx) that enforces authentication and TLS. For local development, prefer keeping `OLLAMA_HOST=127.0.0.1:11434` and using SSH tunneling to access it remotely.

### Accessing Ollama from another device or server

For Ollama to be reachable outside the local machine, the server must listen on all interfaces:

```bash
# Linux (systemd)
Environment="OLLAMA_HOST=0.0.0.0:11434"

# macOS
launchctl setenv OLLAMA_HOST "0.0.0.0"

# Windows — set OLLAMA_HOST=0.0.0.0:11434 as an environment variable
```

The API will then be accessible at `http://<SERVER_IP>:11434`.

---

### `.env` file (Python projects)

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:14b
OLLAMA_TIMEOUT=120
```

```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL    = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")

def extract_symptoms(text: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a medical NLP assistant."},
                {"role": "user", "content": text}
            ],
            "stream": False
        },
        timeout=int(os.getenv("OLLAMA_TIMEOUT", 120))
    )
    response.raise_for_status()
    return response.json()
```

---

### Healthcheck

Before sending requests, it is recommended to verify that the service is running:

```python
import requests

def is_ollama_running(base_url: str = "http://localhost:11434") -> bool:
    try:
        r = requests.get(base_url, timeout=3)
        return r.status_code == 200
    except requests.ConnectionError:
        return False
```

---

## 🛠️ Common Issues

| Problem | Cause | Solution |
|---|---|---|
| `command not found: ollama` | Not in PATH | Restart the terminal or add Ollama to PATH manually |
| `connection refused` on port 11434 | Service is not running | Run `ollama serve` or `systemctl start ollama` |
| Model generates very slowly | Running on CPU instead of GPU | Check `ollama ps` — the PROCESSOR column should show GPU |
| `503 server overloaded` | Too many parallel requests | Increase `OLLAMA_MAX_QUEUE` |
| Model unloads immediately | `OLLAMA_KEEP_ALIVE` too low | Set to `30m` or `-1` to keep it loaded indefinitely |
| Not enough VRAM | Model too large for the GPU | Use a quantized version (e.g. `q4_K_M`) |
