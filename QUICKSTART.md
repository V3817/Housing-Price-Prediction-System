# 🚀 Quick Start Guide

Get your Housing Price Prediction System up and running in minutes!

## ⚡ Super Quick Start

### Option 1: One-Command Deployment (Recommended)
```bash
python deploy.py
```
This will start both the prediction server and Streamlit app automatically!

### Option 2: Manual Start
```bash
# Terminal 1: Start prediction server
python simple_server.py

# Terminal 2: Start Streamlit app
streamlit run app.py
```

## 🌐 Access Your System

- **🌐 Web App**: http://localhost:8501
- **📊 API Server**: http://127.0.0.1:8000
- **📖 API Docs**: http://127.0.0.1:8000/

## 🎯 Make Your First Prediction

1. Open http://localhost:8501 in your browser
2. Adjust the house features using the sidebar sliders
3. Click "Predict Price" 
4. Get instant house price estimates! 🏠💰

## 🔧 Troubleshooting

### "Model not found" error?
- Ensure you have the trained model in `mlruns/` directory
- Run the training pipeline first if needed

### Port already in use?
- Change ports in the scripts or kill existing processes
- Default ports: 8000 (API), 8501 (Streamlit)

### Dependencies missing?
```bash
pip install -r requirements.txt
```

## 📱 Test the API

```bash
# Health check
curl http://127.0.0.1:8000/health

# Make a prediction
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Overall Qual": 7, "Gr Liv Area": 2000}'
```

## 🎉 You're Ready!

Your Housing Price Prediction System is now running! Check the main README.md for detailed documentation and advanced features.

---

**Need help?** Check the main README.md or create an issue in the repository! 🆘
