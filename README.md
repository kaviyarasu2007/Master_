# Master_
Automated a Security AI with Antrophic Skills 
Markdown
# ⚡ Threat Orchestration & Execution Hub

![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![React](https://img.shields.io/badge/React-Vite-cyan)

## 📖 Overview
The **Threat Orchestration & Execution Hub** is a custom-built, asynchronous cybersecurity operations framework. It bridges an advanced LLM reasoning engine (via OpenRouter/Claude Core) with a live local execution environment. 

This architecture allows an operator to issue natural language tactical commands (e.g., "Analyze this malware", "List network interfaces"), which the AI then translates into safe, verifiable shell commands that are executed locally. The output is streamed back to a custom React-based dark-mode terminal via WebSockets in real-time.

## 🏗️ Architecture & Project Structure
The system utilizes a dual-engine architecture:
1. **Strategic Engine (Backend):** A FastAPI/Python server that manages API transactions, enforces security guardrails, and handles asynchronous subprocess execution.
2. **Operator Console (Frontend):** A React/Vite web application styled with Tailwind CSS to emulate a high-end SOC terminal.

```text
Master/
├── engine/                   # Python Backend Module
│   ├── __init__.py           # Package initializer
│   ├── app.py                # FastAPI server, WebSocket routes, & AI logic
│   ├── safety.py             # Security controller and command guardrails
│   └── websocket.py          # WebSocket connection manager
├── skills/                   # Autonomous Playbooks (Markdown files)
│   ├── analyzing-android-malware-with-apktool/
│   ├── hunting-threats/
│   └── reverse-engineering/
├── src/                      # React Frontend Source Code
│   ├── components/
│   │   └── OpenTerminal.jsx  # Live terminal streaming component
│   ├── App.jsx               # Main React application
│   └── main.jsx              # React DOM entry point
├── test/                     # Python Virtual Environment (v3.12)
├── index.html                # Vite application entry point
├── package.json              # Node.js dependencies and scripts
├── postcss.config.js         # Tailwind CSS compiler configuration
├── requirements.txt          # Python backend dependencies
├── tailwind.config.js        # UI styling configuration
└── vite.config.js            # Frontend build tool configuration
⚙️ Prerequisites
Ensure you have the following installed on your host machine before deployment:

Python 3.12 (Strict requirement to avoid pydantic-core Rust compilation errors found in 3.13+)

Node.js & npm

OpenRouter API Key (For the LLM reasoning engine)

🚀 Installation & Setup
1. Backend Environment Setup (Python)
The backend requires an isolated Python 3.12 virtual environment to manage API routing and WebSocket handling.

Bash
# Navigate to the project root
cd ~/Master

# Create the virtual environment using stable Python 3.12
python3.12 -m venv test

# Activate the virtual environment
source test/bin/activate

# Upgrade pip (crucial for pre-built wheels) and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
2. Frontend Environment Setup (Node.js)
The frontend utilizes Vite for rapid hot-module reloading and Tailwind CSS for the dark-mode aesthetic.

Bash
# Install all Node modules and build tools
npm install

# Initialize Tailwind CSS to generate the required PostCSS configuration
npx tailwindcss init -p
3. API Key Configuration
Before starting the servers, you must link your LLM access key.

Open engine/app.py.

Locate the OPENROUTER_KEY variable at the top of the file.

Replace "sk-or-v1-..." with your active, secure OpenRouter API key.

💻 Running the Framework
This system requires two active terminal sessions to run simultaneously.

Terminal 1: Ignite the Backend Engine

Bash
cd ~/Master
source test/bin/activate
uvicorn engine.app:app --reload --port 8000
Expected Output: Application startup complete.

Terminal 2: Ignite the Operator Console

Bash
cd ~/Master
npm run dev
Expected Output: ➜  Local:   http://localhost:3000/

🎯 Usage & Execution
Open your web browser and navigate to http://localhost:3000.

Wait for the terminal to display: SYSTEM: WebSocket bridge established with app.py.

Enter a tactical scenario into the command prompt.

Example: "System, assume we have isolated an infected Android APK. Based on your Android malware analysis skills, run a safe, local terminal command to list the files in the current directory..."

The Strategic Reasoning Stream (Left Panel) will display the AI's formulated tactical plan based on the active skills/ playbooks.

The Live Terminal Pipeline (Right Panel) will intercept the AI's command, verify it, execute it via the host OS, and stream the standard output back to your screen.

🔧 Troubleshooting Guide
Error: Failed building wheel for pydantic-core during backend setup.

Fix: Your system is using an unsupported bleeding-edge Python version (like 3.14) and trying to compile Rust from scratch. Downgrade your virtual environment strictly to python3.12.

Error: sh: 1: vite: not found during frontend startup.

Fix: The node_modules folder is missing or corrupted. Run rm -rf node_modules package-lock.json followed by a fresh npm install.

Error: SYSTEM REJECTION: Backend interface unreachable.

Fix: The Python backend has crashed, likely due to a missing import (e.g., import asyncio in app.py) or an invalid API key causing a JSON gateway fault. Check Terminal 1 logs for the exact Python traceback.

UI is unstyled / stacked vertically.

Fix: Tailwind is failing to compile. Ensure you ran npx tailwindcss init -p to create postcss.config.js, then restart the Vite server.

🛡️ Security & Warning
USE WITH CAUTION. This framework executes live terminal commands on your host machine. While it is equipped with a SecurityController (engine/safety.py) to restrict destructive commands (like rm, mkfs, chmod -R), it is highly recommended to run this framework inside a dedicated Virtual Machine (VM) or containerized environment when handling live malware or conducting active threat hunting.

🙏 Acknowledgements
Anthropic-Cybersecurity-Skills: The expansive library of autonomous playbooks, system prompts, and tactical cybersecurity skills powering the reasoning capabilities of this framework was generously provided and curated by mukul975 (Anthropic-Cybersecurity-Skills).
