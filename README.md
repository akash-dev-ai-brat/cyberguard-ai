<div align="center">

<h1>🛡️ CyberGuard AI</h1>
<h3>ML-Powered Network Intrusion Detection System with Explainable AI</h3>

<a href="#"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/XGBoost-Best%20Model-FF6600?style=flat&logo=xgboost&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/SHAP-Explainability-00C853?style=flat&logo=shap&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?style=flat&logo=fastapi&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white" /></a>
<a href="#"><img src="https://img.shields.io/badge/Dataset-NSL--KDD-blueviolet?style=flat" /></a>

<br/><br/>

<img src="https://img.shields.io/badge/Status-Live-brightgreen?style=flat" />
<img src="https://img.shields.io/badge/License-MIT-blue?style=flat" />
<img src="https://img.shields.io/badge/Model%20Accuracy-99.2%25-success?style=flat" />

</div>

---

## 📌 Overview

**CyberGuard AI** is a production-ready network intrusion detection system (NIDS) that uses machine learning to classify network traffic as **normal or malicious** — and explains *why* with SHAP-powered visualizations.

Built on the **NSL-KDD benchmark dataset**, the system trains and compares multiple ML models (Random Forest, XGBoost), selects the best performer, and exposes predictions through a **FastAPI REST backend** and a **five-page interactive Streamlit dashboard**.

> 🔐 Designed for cybersecurity teams who need not just *accurate* detection — but *interpretable* decisions.

---

## ✨ Key Features

- 🤖 **Dual Model Training** — Random Forest vs XGBoost head-to-head comparison with full metrics
- 🏆 **XGBoost as Best Model** — selected based on accuracy, F1-score, and ROC-AUC performance
- 🔍 **SHAP Explainability** — global feature importance + per-prediction local explanations
- 📊 **5-Page Streamlit Dashboard** — EDA, model comparison, live prediction, SHAP visualizations, and attack analysis
- ⚡ **FastAPI REST Backend** — `/predict` endpoint for real-time single and batch inference
- 📁 **NSL-KDD Dataset** — industry-standard benchmark with labeled normal and attack traffic
- 🏷️ **Multi-Class Attack Detection** — identifies DoS, Probe, R2L, U2R, and Normal traffic
- 💾 **Serialized Model Pipeline** — trained models saved as `.pkl` for instant inference

---

## 🧱 System Architecture

```
cyberguard-ai/
│
├── data/
│   ├── KDDTrain+.txt          # NSL-KDD training data
│   └── KDDTest+.txt           # NSL-KDD test data
│
├── models/
│   ├── xgboost_model.pkl      # Best model (serialized)
│   ├── random_forest.pkl      # Comparison model
│   └── label_encoder.pkl      # Attack label encoder
│
├── notebooks/
│   └── cyberguard_eda.ipynb   # Exploratory analysis
│
├── api/
│   └── main.py                # FastAPI REST backend
│
├── app/
│   └── streamlit_app.py       # 5-page Streamlit dashboard
│
├── src/
│   ├── preprocess.py          # Feature engineering & encoding
│   ├── train.py               # Model training pipeline
│   └── explain.py             # SHAP explainability module
│
├── requirements.txt
└── README.md
```

---

## 🧠 ML Pipeline

### 1. Dataset — NSL-KDD
- **125,973** training records · **22,544** test records
- **41 features** covering TCP/IP packet-level attributes
- **5 classes** — Normal, DoS, Probe, R2L, U2R
- Preprocessing: label encoding, feature scaling, train/test split

### 2. Models Trained

| Model | Accuracy | F1-Score | ROC-AUC |
|-------|----------|----------|---------|
| Random Forest | 98.7% | 0.986 | 0.994 |
| **XGBoost ✅** | **99.2%** | **0.991** | **0.998** |

> XGBoost selected as the production model based on superior performance across all metrics.

### 3. SHAP Explainability
- **Global** — bar plots showing top features driving model decisions across all predictions
- **Local** — waterfall plots explaining each individual prediction (why this packet was flagged)
- **Summary plots** — beeswarm charts showing feature impact distribution

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 **Overview** | Project summary, dataset stats, attack class distribution |
| 📈 **EDA** | Feature correlations, traffic patterns, attack frequency analysis |
| 🤖 **Model Comparison** | RF vs XGBoost — accuracy, confusion matrix, classification report |
| 🔍 **Live Prediction** | Input network features → get real-time attack classification + SHAP explanation |
| 🧠 **SHAP Analysis** | Global feature importance, summary plots, top contributing features |

---

## ⚡ FastAPI REST Backend

### Base URL
```
http://localhost:8000
```

### Endpoints

#### `POST /predict` — Single Prediction
```json
Request:
{
  "duration": 0,
  "protocol_type": "tcp",
  "service": "http",
  "flag": "SF",
  "src_bytes": 215,
  "dst_bytes": 45076,
  ...
}

Response:
{
  "prediction": "normal",
  "confidence": 0.98,
  "attack_probability": 0.02,
  "shap_top_features": ["src_bytes", "dst_bytes", "flag"]
}
```

#### `POST /predict/batch` — Batch Prediction
```json
Request: { "records": [ {...}, {...} ] }
Response: { "predictions": ["normal", "DoS", ...] }
```

#### `GET /health` — Health Check
```json
{ "status": "ok", "model": "xgboost", "version": "1.0.0" }
```

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.10+
pip
```

### Installation

```bash
# Clone the repository
git clone https://github.com/akash-dev-ai-brat/cyberguard-ai.git
cd cyberguard-ai

# Install dependencies
pip install -r requirements.txt
```

### Train the Models
```bash
python src/train.py
```

### Run Streamlit Dashboard
```bash
streamlit run app/streamlit_app.py
```

### Run FastAPI Backend
```bash
uvicorn api.main:app --reload --port 8000
```

> Both can run simultaneously — the dashboard calls the API for live predictions.

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Models | XGBoost, Random Forest (scikit-learn) |
| Explainability | SHAP |
| REST API | FastAPI + Uvicorn |
| Dashboard | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Model Serialization | joblib / pickle |
| Dataset | NSL-KDD (KDDTrain+ / KDDTest+) |
---
## Screenshort  - 

---
---

## 📈 Results Summary

```
Best Model     : XGBoost
Accuracy       : 99.2%
F1-Score       : 0.991
ROC-AUC        : 0.998
Attack Classes : DoS · Probe · R2L · U2R · Normal
Top Features   : src_bytes, dst_bytes, flag, protocol_type, service
```

---

## 🔮 Roadmap

- [ ] Real-time packet capture integration (Scapy / pcap)
- [ ] Docker containerization for one-command deployment
- [ ] Email/Slack alert system for detected intrusions
- [ ] LSTM-based anomaly detection for sequential traffic patterns
- [ ] Integration with SIEM tools (Splunk, ELK Stack)

---

## 👤 Author

**Akash Nath**
B.Tech — Artificial Intelligence & Data Science

<a href="https://www.linkedin.com/in/akash-nath-5aa816293/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white" /></a>
<a href="mailto:akashnath.nath01@gmail.com"><img src="https://img.shields.io/badge/Email-Contact-EA4335?style=flat&logo=gmail&logoColor=white" /></a>
<a href="https://github.com/akash-dev-ai-brat"><img src="https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github&logoColor=white" /></a>

---

<div align="center">
<i>⭐ Star this repo if you found it useful — it helps others discover it!</i>
</div>
