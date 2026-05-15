# 🎣 AI-Powered Phishing Detection System

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ML: Security](https://img.shields.io/badge/ML-Security-green.svg)]()

A production-grade AI platform designed to identify malicious emails using Natural Language Processing (NLP), behavioral indicators, and machine learning classification.

Developed by **Syed**.

## 🧠 Intelligence Features

- **NLP Preprocessing**: HTML stripping, tokenization, stemming, and URL extraction.
- **Feature Extraction**: Urgent language detection, financial bait keywords, and sender mismatch analysis.
- **Behavioral Scoring**: Weighted confidence scoring for phishing classification.
- **XAI (Explainable AI)**: Visualizes feature importance to explain why an email was flagged.
- **Interactive Dashboard**: Modern Streamlit-based UI for Security Operations Centers (SOC).

## 🛡️ Detection Capabilities

The system classifies emails into:
- ✅ **SAFE**: No malicious indicators found.
- ⚠️ **SUSPICIOUS**: Potential risk, further investigation needed.
- 🟠 **HIGH RISK**: Strong phishing indicators detected.
- 🔴 **CRITICAL**: Confirmed malicious threat vectors.

## 🛠️ Tech Stack

- **ML/NLP**: `scikit-learn`, `nltk`, `pandas`, `numpy`
- **UI**: `streamlit`, `plotly`
- **Utilities**: `beautifulsoup4`, `regex`

## 📦 Installation

```bash
git clone https://github.com/nullfist/phishing-detection.git
cd phishing-detection
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🖥️ Usage

Launch the SOC Analysis Dashboard:
```bash
streamlit run dashboard.py
```

## 📊 Analytics
The platform provides:
- Live Threat Score (0-100)
- Detected Indicator Breakdown
- Feature Importance Heatmaps
- Recommended Security Actions

## 🤝 Contributing
Open to PRs for adding new ML models or advanced feature extraction modules.

## 📜 License
MIT License.
