# 🌌 ChronoCanvas — Autonomous Weather & Atmosphere Adaptive Agent

> **An always-on, zero-prompt autonomous creative agent deployed on AWS that continuously senses real-time atmospheric & astronomical telemetry to synthesize digital artwork, micro-poetry, dynamic UI color palettes, and procedural ambient soundscapes.**

---

[![AWS Serverless](https://img.shields.io/badge/AWS-Serverless_SAM-orange.svg?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?logo=python)](https://python.org)
[![EventBridge](https://img.shields.io/badge/EventBridge-Scheduled_Cron-purple.svg)](https://aws.amazon.com/eventbridge/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 👁️ Vision & What It Does

In modern digital life, standard AI generative tools require active human initiation: opening an application, crafting a prompt, and waiting for generation. 

**ChronoCanvas flips this paradigm.** It operates silently and autonomously in the background. Without any human intervention, ChronoCanvas continuously monitors ambient real-time environmental telemetry—including weather conditions, temperature, solar angles, and astronomical phases—and synthesizes:

- 🎨 **Atmospheric Digital Artwork**: Photorealistic celestial and planetary artwork reflecting current atmospheric conditions.
- 📜 **Environmental Micro-Poetry & Lore**: Evocative stanzas and observational lore derived from weather metrics.
- 🎨 **Dynamic HSL Color Vectoring**: A multi-color palette that dynamically shifts the theme of the web UI.
- 🎵 **Procedural Web Audio Ambient Soundscapes**: Harmonics generated mathematically via the Web Audio API, keyed to the environmental color hue.

---

## 🏗️ Architecture & Data Flow

```
                               ┌───────────────────────────┐
                               │   Open-Meteo Weather API  │
                               └─────────────┬─────────────┘
                                             │ Real-time Telemetry
                                             ▼
┌──────────────────┐           ┌───────────────────────────┐           ┌───────────────────────────┐
│ EventBridge Cron │ ────────► │  ChronoCanvas Agent Core  │ ────────► │ Pollinations AI Art Engine│
│ (Every 6 Hours)  │           │     (backend/agent.py)    │           └───────────────────────────┘
└──────────────────┘           └─────────────┬─────────────┘
                                             │
                         ┌───────────────────┴───────────────────┐
                         ▼                                       ▼
             ┌──────────────────────┐                ┌──────────────────────┐
             │ DynamoDB & S3 Bucket │                │  Local JSON Fallback │
             │  (AWS Persistence)   │                │ (data/history.json)  │
             └──────────────────────┘                └──────────────────────┘
                         ▲                                       ▲
                         │                                       │
                         └───────────────────┬───────────────────┘
                                             │ HTTP API Gateway
                                             ▼
                               ┌───────────────────────────┐
                               │   Web Dashboard & Synth   │
                               │(frontend/index.html & app)│
                               └───────────────────────────┘
```

---

## ⚡ Tech Stack

- **Cloud Platform**: AWS Serverless Architecture (AWS SAM)
- **Execution Environment**: AWS Lambda (Python 3.11)
- **Scheduler**: Amazon EventBridge (Cron trigger every 6 hours: `rate(6 hours)`)
- **Storage**: Amazon S3 (JSON Metadata Storage) & Amazon DynamoDB (`ChronoCanvas-Gallery`)
- **API Layer**: Amazon API Gateway
- **Frontend UI**: HTML5, Vanilla CSS3 (Dynamic HSL Variables), JavaScript (ES6+), Web Audio API
- **Local Runtime**: Python Built-in `http.server` HTTP Gateway Bridge

---

## 📁 Repository Structure

```
chronocanvas-agent/
├── article/
│   └── builder_center_article.md  # AWS Builder Center submission article
├── aws/
│   ├── deploy.ps1                 # AWS SAM deployment script
│   └── template.yaml              # AWS SAM Infrastructure as Code template
├── backend/
│   ├── agent.py                   # Autonomous Creative Agent core logic
│   ├── lambda_function.py         # AWS Lambda entry point & API Router
│   └── requirements.txt           # Backend dependencies (boto3)
├── data/
│   └── history.json               # Creation gallery storage / fallback
├── frontend/
│   ├── app.js                     # Frontend logic & Web Audio synthesizer engine
│   ├── index.html                 # Main dashboard UI
│   └── styles.css                 # Glassmorphic UI styles with dynamic HSL variables
├── README.md                      # Project Documentation
└── server.py                      # Standalone local HTTP dev server
```

---

## 🚀 Quickstart — Running Locally

You can run ChronoCanvas locally without needing AWS credentials or cloud deployment.

### Prerequisites
- **Python 3.8+** installed

### 1. Clone the Repository
```bash
git clone https://github.com/U7ama/ChronoCanvas.git
cd ChronoCanvas
```

### 2. Start the Local Server
```bash
python server.py 8085
```

### 3. Open in Browser
Navigate to **[http://localhost:8085](http://localhost:8085)** in your web browser.

---

## ☁️ Deploying to AWS Serverless

To deploy ChronoCanvas to your AWS account via AWS SAM:

### Prerequisites
- [AWS CLI](https://aws.amazon.com/cli/) configured with valid credentials
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed

### Deployment Steps
```powershell
cd aws
.\deploy.ps1
```
Or execute SAM directly:
```bash
cd aws
sam build
sam deploy --guided
```

Once deployed, SAM will output your **API Gateway Endpoint URL**, which triggers the Lambda agent automatically or responds to frontend requests.

---

## 🔌 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/canvas/latest` | `GET` | Returns the most recently synthesized autonomous creation object. |
| `/canvas/history` | `GET` | Returns the timeline array of all past creations stored in DynamoDB/Local JSON. |
| `/canvas/generate` | `POST` | Manually triggers an autonomous agent creation cycle on demand. |

### Sample JSON Response (`GET /canvas/latest`)
```json
{
  "canvas_id": "canvas-1787308627",
  "created_at": "2026-08-21 15:37:07",
  "location": "New York, USA",
  "title": "Solitude in Solar Zenith",
  "poem": "Across the quiet canopy of solar zenith...",
  "lore": "Synthesized during Solar Zenith under Mainly Clear Amber Atmosphere...",
  "weather": {
    "temperature_c": 17.7,
    "temperature_f": 63.9,
    "weather_code": 1,
    "condition": "Mainly Clear Amber Atmosphere"
  },
  "mood": {
    "phase": "Solar Zenith",
    "mood": "Vibrant, Energetic, Radiant",
    "primary_hue": 207,
    "palette": ["hsl(207, 85%, 60%)", "hsl(252, 75%, 50%)", "hsl(27, 90%, 65%)", "hsl(87, 40%, 15%)"]
  },
  "image_url": "https://image.pollinations.ai/prompt/..."
}
```

---

## 📄 License

This project is open-source and available under the **MIT License**.
