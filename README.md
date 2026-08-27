# 🏡 Housing Price Prediction System

A comprehensive machine learning system for predicting house prices using the Ames Housing dataset. This project includes a complete ML pipeline, web interface, and API endpoints.

## 🚀 Features

- **Interactive Streamlit Web App** - User-friendly interface for house price predictions
- **Machine Learning Pipeline** - End-to-end ML workflow using ZenML
- **REST API** - Flask-based prediction service
- **Model Management** - MLflow integration for model versioning
- **Comprehensive Feature Engineering** - Advanced preprocessing and transformation
- **Real-time Predictions** - Instant house price estimates

## 📊 Dataset

The system uses the **Ames Housing Dataset** which contains:
- **2,930** residential properties
- **81** features including:
  - Physical characteristics (area, rooms, quality)
  - Location features (neighborhood, zoning)
  - Temporal features (year built, sold)
  - Amenities (garage, basement, porch)

## 🏗️ Architecture

```
├── app.py                 # Streamlit web application
├── simple_server.py       # Flask prediction API
├── pipelines/            # ML pipeline definitions
├── steps/               # Pipeline step implementations
├── src/                 # Core functionality modules
├── analysis/            # EDA and analysis notebooks
├── data/               # Dataset storage
└── mlruns/             # MLflow model artifacts
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/housing-price-predictor.git
   cd housing-price-predictor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the prediction server**
   ```bash
   python simple_server.py
   ```

4. **Launch the Streamlit app**
   ```bash
   streamlit run app.py
   ```

## ☁️ Streamlit Cloud Deployment

### Option 1: Use Minimal Requirements (Recommended)
1. **Fork/Clone** this repository to your GitHub account
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Connect** your GitHub account
4. **Select** your repository
5. **Main file path**: `app.py`
6. **Requirements file**: `requirements-streamlit-cloud.txt`
7. **Click Deploy** 🚀

### Option 2: Use Full Requirements
- Use `requirements.txt` if you want all features
- May take longer to deploy due to more dependencies

### ⚠️ Important Notes for Streamlit Cloud:
- **Model files**: Ensure `mlruns/` directory is included in your GitHub repo
- **Python version**: Streamlit Cloud uses Python 3.11 by default
- **Memory limits**: Be aware of Streamlit Cloud's memory constraints
- **Deployment time**: First deployment may take 5-10 minutes

## 🎯 Usage

### Web Interface
1. Open your browser to `http://localhost:8501` (local) or your Streamlit Cloud URL
2. Adjust house features using the sidebar sliders
3. Click "Predict Price" to get instant estimates
4. View detailed predictions and mathematical relationships

### API Endpoints

#### Health Check
```bash
curl http://127.0.0.1:8000/health
```

#### Prediction (MLflow format)
```bash
curl -X POST http://127.0.0.1:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_records": [{"Overall Qual": 7, "Gr Liv Area": 2000}]}'
```

#### Simple Prediction
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Overall Qual": 7, "Gr Liv Area": 2000}'
```

## 🔧 Model Details

### Preprocessing
- **Target Variable**: Log-transformed using `np.log1p(SalePrice)`
- **Numerical Features**: Mean imputation for missing values
- **Categorical Features**: One-hot encoding with unknown handling
- **Feature Engineering**: Log transformation for skewed numerical features

### Algorithm
- **Model**: Linear Regression with scikit-learn
- **Pipeline**: Preprocessing + model in a single pipeline
- **Validation**: Train-test split (80-20)

### Performance
- **Expected Price Range**: $100,000 - $250,000
- **Accuracy**: Optimized for typical residential properties
- **Features**: 81 comprehensive house characteristics

## 📁 Project Structure

```
housing-price-predictor/
├── app.py                 # Main Streamlit application
├── simple_server.py       # Flask prediction server
├── requirements.txt       # Full Python dependencies
├── requirements-streamlit-cloud.txt  # Minimal dependencies for Streamlit Cloud
├── README.md             # This file
├── pipelines/            # ML pipeline definitions
│   ├── training_pipeline.py
│   └── deployment_pipeline.py
├── steps/               # Pipeline steps
│   ├── data_ingestion_step.py
│   ├── feature_engineering_step.py
│   ├── model_building_step.py
│   └── ...
├── src/                 # Core modules
│   ├── feature_engineering.py
│   ├── data_splitter.py
│   └── ...
├── analysis/            # Data analysis
│   └── EDA.ipynb       # Exploratory data analysis
├── data/               # Dataset storage
│   └── archive.zip     # Ames Housing dataset
└── mlruns/             # MLflow artifacts
    └── 0/              # Model versions
```

## 🔍 Key Features Explained

### 1. Feature Engineering
- **Log Transformation**: Applied to skewed numerical features
- **Missing Value Handling**: Intelligent imputation strategies
- **Categorical Encoding**: One-hot encoding for categorical variables

### 2. Model Pipeline
- **Preprocessing**: Consistent transformation across training and inference
- **Model Training**: Linear regression with regularization
- **Pipeline Persistence**: Complete pipeline saved for deployment

### 3. Web Interface
- **Interactive Controls**: Sliders and inputs for all features
- **Real-time Updates**: Instant predictions as you adjust values
- **Educational Content**: Mathematical explanations and context

## 🚀 Deployment

### Local Development
```bash
# Terminal 1: Start prediction server
python simple_server.py

# Terminal 2: Start Streamlit app
streamlit run app.py
```

### Streamlit Cloud Deployment
1. **Use `requirements-streamlit-cloud.txt`** for minimal dependencies
2. **Ensure `mlruns/` directory** is in your GitHub repo
3. **Deploy via** [share.streamlit.io](https://share.streamlit.io)
4. **Main file**: `app.py`

### Production Deployment
1. **Model Server**: Deploy `simple_server.py` to your preferred hosting
2. **Web App**: Deploy `app.py` to Streamlit Cloud or similar
3. **Environment**: Ensure all dependencies from `requirements.txt` are installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ames Housing Dataset**: Iowa State University
- **MLflow**: Model lifecycle management
- **ZenML**: ML pipeline orchestration
- **Streamlit**: Web application framework

## 📞 Support

For questions or issues:
- Create an issue in this repository
- Check the documentation in the code
- Review the EDA notebook for data insights

---

**Happy House Hunting! 🏠✨**
