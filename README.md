# 🌌 ChronoCanvas

An **autonomous AI agent** that creates artwork, poetry, dynamic UI themes, and ambient soundscapes based on real-time weather and time of day — with zero manual prompts required.

---

## ✨ Features

- 🎨 **Automated Digital Art**: Generates celestial & planetary visuals tailored to live weather.
- 📜 **Weather Poetry**: Writes atmospheric poems and lore based on temperature and sky conditions.
- 🌈 **Dynamic Colors**: Shifts the frontend color palette automatically based on solar cycles.
- 🎵 **Ambient Soundscape**: Synthesizes background audio keyed to environmental mood.
- ☁️ **AWS Serverless & Local**: Runs in the cloud via AWS Lambda/EventBridge or locally using Python.

---

## 📂 Project Structure

```text
chronocanvas-agent/
├── backend/
│   ├── agent.py          # Core agent logic
│   └── lambda_function.py# AWS Lambda handler & API router
├── frontend/
│   ├── index.html        # Web dashboard UI
│   ├── app.js            # Frontend logic & Web Audio synthesizer
│   └── styles.css        # Styles & dynamic color themes
├── aws/
│   ├── template.yaml     # AWS SAM deployment template
│   └── deploy.ps1        # AWS deployment script
├── data/
│   └── history.json      # Creation history store
├── article/
│   └── builder_center_article.md # AWS Builder submission article
└── server.py             # Local dev server
```

---

## 🚀 Quickstart (Run Locally)

### 1. Start the local server
```bash
python server.py 8085
```

### 2. Open in browser
Go to **`http://localhost:8085`** to view the app.

---

## ☁️ AWS Deployment

Deploy the serverless stack using **AWS SAM**:

```bash
cd aws
sam build
sam deploy --guided
```

This sets up AWS Lambda, S3, DynamoDB, API Gateway, and an EventBridge cron (triggers every 6 hours)

---

## 🔌 API Endpoints

- `GET /canvas/latest` — Get the newest creation
- `GET /canvas/history` — Get all past creations
- `POST /canvas/generate` — Trigger a new creation on demand

---

## 📄 License
MIT License
