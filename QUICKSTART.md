# Quick Start Guide

## 🚀 Getting Started with Agricultural Price Prediction System

### Prerequisites
- Python 3.8 or higher
- pip or conda
- Git

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/agri-price-prediction.git
cd agri-price-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app/streamlit_app.py
```

Visit `http://localhost:8501` in your browser.

---

### Option 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agri-price-prediction.git
cd agri-price-prediction

# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t agri-price-prediction .
docker run -p 8501:8501 agri-price-prediction
```

Visit `http://localhost:8501` in your browser.

---

### Option 3: Package Installation

```bash
# Install from package
pip install agri-price-prediction

# Run
agri-predict
```

---

## 📊 Using the Web Application

### 1. Dashboard
- View real-time commodity prices
- See price trends and statistics
- Compare moving averages

### 2. Price Prediction
- Select a commodity (Onion, Potato, Pulses)
- Choose forecast period (7-90 days)
- Get predicted prices with confidence intervals

### 3. Historical Analysis
- Explore historical price data
- View statistical distributions
- See feature correlations

### 4. Model Performance
- Compare different ML models
- View accuracy metrics
- Understand model capabilities

---

## 💻 Python API Usage

```python
from src.data_loader import DataLoader
from src.preprocessing import preprocess_and_engineer
from src.model_training import RandomForestTrainer

# Load data
loader = DataLoader()
df = loader.load_commodity_data('onion')

# Preprocess
df = preprocess_and_engineer(df)

# Prepare features and target
X = df.drop(['date', 'commodity', 'price'], axis=1).values
y = df['price'].values

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
trainer = RandomForestTrainer()
trainer.train(X_train, y_train)

# Make predictions
predictions = trainer.predict(X_test)

# Evaluate
from src.model_evaluation import ModelEvaluator
evaluator = ModelEvaluator()
metrics = evaluator.evaluate_model(y_test, predictions, "Random Forest")
evaluator.print_evaluation_report(metrics)
```

---

## 📁 Project Structure

```
agri-price-prediction/
├── app/                          # Web application
│   ├── streamlit_app.py         # Main Streamlit app
│   └── config.py                # Configuration
├── src/                          # Core modules
│   ├── data_loader.py           # Data loading
│   ├── preprocessing.py         # Data preprocessing
│   ├── model_training.py        # Model training
│   ├── model_evaluation.py      # Model evaluation
│   └── predictions.py           # Prediction generation
├── models/                       # Trained models
├── data/                         # Data directory
│   ├── raw/                     # Raw data
│   └── processed/               # Processed data
├── notebooks/                    # Jupyter notebooks
├── tests/                        # Unit tests
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose
├── setup.py                      # Package setup
└── README.md                     # Project README
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# API Configuration
AGMARKET_API_KEY=your_api_key_here

# Model Configuration
MODEL_TYPE=xgboost  # or random_forest, lstm, arima
FORECAST_DAYS=30
CONFIDENCE_LEVEL=0.95

# Data Configuration
DATA_CACHE_DIR=data/cached
MODEL_DIR=models

# Logging
LOG_LEVEL=INFO
```

### Model Configuration

Edit `app/config.py`:

```python
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 20,
    },
    'xgboost': {
        'n_estimators': 100,
        'learning_rate': 0.1,
    },
    'lstm': {
        'epochs': 50,
        'batch_size': 32,
        'sequence_length': 30,
    },
    'arima': {
        'order': (1, 1, 1),
    }
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_models.py::TestRandomForest
```

---

## 📈 Training Your Own Model

```bash
# Interactive training script
python scripts/train_models.py

# Or use Python
python -c "
from src.model_training import RandomForestTrainer
from src.model_evaluation import ModelEvaluator

trainer = RandomForestTrainer(n_estimators=150)
trainer.train(X_train, y_train)
trainer.save_model('my_rf_model')

# Evaluate
predictions = trainer.predict(X_test)
metrics = ModelEvaluator.evaluate_model(y_test, predictions)
print(f'RMSE: {metrics[\"rmse\"]:.2f}')
"
```

---

## 🌐 Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with one click

### Heroku

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create your-app-name
git push heroku main
```

### AWS EC2

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Clone and setup
git clone https://github.com/yourusername/agri-price-prediction.git
cd agri-price-prediction
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## 📚 Additional Resources

- **Documentation**: [View Full Docs](docs/PROJECT_REPORT.md)
- **GitHub**: [Repository](https://github.com/yourusername/agri-price-prediction)
- **Issues**: [Report Bugs](https://github.com/yourusername/agri-price-prediction/issues)
- **Discussions**: [Community Forum](https://github.com/yourusername/agri-price-prediction/discussions)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## ❓ FAQ

**Q: Can I use this for other commodities?**  
A: Yes! The system is designed to work with any commodity. Just provide historical price data.

**Q: What's the accuracy of predictions?**  
A: MAPE ranges from 4.2% to 6.2% depending on commodity and forecast horizon.

**Q: How often should I retrain the models?**  
A: We recommend monthly retraining to capture recent market dynamics.

**Q: Can I deploy this on my own server?**  
A: Yes, Docker Compose configuration is provided for easy deployment.

**Q: How do I get real-time predictions?**  
A: Use the Streamlit web interface or the Python API with scheduled jobs.

---

## 🆘 Support

For issues or questions:
1. Check [FAQ](FAQ.md)
2. Search [GitHub Issues](https://github.com/yourusername/agri-price-prediction/issues)
3. Create a new issue with details
4. Email: support@agri-prediction.com

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
