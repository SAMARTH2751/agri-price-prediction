"""
Model Training Module for Agricultural Price Prediction System
Includes Random Forest, XGBoost, LSTM, and ARIMA models
"""

import numpy as np
import pandas as pd
import logging
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from statsmodels.tsa.arima.model import ARIMA
import pickle
from pathlib import Path
from typing import Tuple, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Base class for model training"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
    def split_data(self, X: np.ndarray, y: np.ndarray, 
                   test_size: float = 0.2, method: str = 'random') -> Tuple:
        """Split data for training and testing"""
        logger.info(f"Splitting data ({method} method, test_size={test_size})")
        
        if method == 'random':
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        elif method == 'time_series':
            # Time-series aware split
            split_idx = int(len(X) * (1 - test_size))
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
        else:
            raise ValueError(f"Unknown method: {method}")
        
        logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def save_model(self, model: Any, name: str):
        """Save model to disk"""
        path = self.model_dir / f"{name}.pkl"
        pickle.dump(model, open(path, 'wb'))
        logger.info(f"Model saved to {path}")
    
    def load_model(self, name: str) -> Any:
        """Load model from disk"""
        path = self.model_dir / f"{name}.pkl"
        if path.exists():
            model = pickle.load(open(path, 'rb'))
            logger.info(f"Model loaded from {path}")
            return model
        else:
            logger.warning(f"Model not found at {path}")
            return None


class RandomForestTrainer(ModelTrainer):
    """Train Random Forest regression model"""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 20):
        super().__init__()
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.model = None
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> RandomForestRegressor:
        """Train Random Forest model"""
        logger.info(f"Training Random Forest with {self.n_estimators} estimators")
        
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        logger.info("Random Forest training completed")
        
        return self.model
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        return self.model.predict(X)
    
    def get_feature_importance(self, feature_names: list = None) -> Dict:
        """Get feature importance"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        importance = self.model.feature_importances_
        if feature_names:
            return dict(zip(feature_names, importance))
        return importance


class XGBoostTrainer(ModelTrainer):
    """Train XGBoost regression model"""
    
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1):
        super().__init__()
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.model = None
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> xgb.XGBRegressor:
        """Train XGBoost model"""
        logger.info(f"Training XGBoost with {self.n_estimators} estimators")
        
        self.model = xgb.XGBRegressor(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective='reg:squarederror'
        )
        
        self.model.fit(X_train, y_train)
        logger.info("XGBoost training completed")
        
        return self.model
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        return self.model.predict(X)
    
    def get_feature_importance(self, feature_names: list = None) -> Dict:
        """Get feature importance"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        importance = self.model.feature_importances_
        if feature_names:
            return dict(zip(feature_names, importance))
        return importance


class LSTMTrainer(ModelTrainer):
    """Train LSTM neural network for time-series forecasting"""
    
    def __init__(self, sequence_length: int = 30, epochs: int = 50):
        super().__init__()
        self.sequence_length = sequence_length
        self.epochs = epochs
        self.model = None
        self.scaler = MinMaxScaler()
    
    def create_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for LSTM training"""
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length])
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple) -> Sequential:
        """Build LSTM architecture"""
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model
    
    def train(self, data: np.ndarray) -> Sequential:
        """Train LSTM model"""
        logger.info(f"Training LSTM with sequence length {self.sequence_length}")
        
        # Scale data
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        
        # Create sequences
        X, y = self.create_sequences(scaled_data)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Build and train model
        self.model = self.build_model((X.shape[1], 1))
        self.model.fit(X, y, epochs=self.epochs, batch_size=32, verbose=0)
        
        logger.info("LSTM training completed")
        return self.model
    
    def predict(self, last_sequence: np.ndarray, steps: int = 1) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        predictions = []
        sequence = last_sequence.reshape(1, -1, 1)
        
        for _ in range(steps):
            pred = self.model.predict(sequence, verbose=0)
            predictions.append(pred[0, 0])
            sequence = np.append(sequence[:, 1:, :], pred.reshape(1, 1, 1), axis=1)
        
        # Inverse transform
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        return predictions.flatten()


class ARIMATrainer(ModelTrainer):
    """Train ARIMA model for time-series forecasting"""
    
    def __init__(self, order: Tuple = (1, 1, 1)):
        super().__init__()
        self.order = order
        self.model = None
        self.fitted_model = None
    
    def find_best_order(self, data: pd.Series, p_range: range = range(0, 3), 
                       d_range: range = range(0, 2), q_range: range = range(0, 3)) -> Tuple:
        """Find best ARIMA order using AIC"""
        logger.info("Finding best ARIMA order")
        
        best_aic = np.inf
        best_order = None
        
        for p in p_range:
            for d in d_range:
                for q in q_range:
                    try:
                        model = ARIMA(data, order=(p, d, q))
                        fitted = model.fit()
                        if fitted.aic < best_aic:
                            best_aic = fitted.aic
                            best_order = (p, d, q)
                    except:
                        pass
        
        logger.info(f"Best order: {best_order} with AIC: {best_aic:.2f}")
        return best_order
    
    def train(self, data: pd.Series) -> ARIMA:
        """Train ARIMA model"""
        logger.info(f"Training ARIMA{self.order}")
        
        self.model = ARIMA(data, order=self.order)
        self.fitted_model = self.model.fit()
        
        logger.info(f"ARIMA training completed. AIC: {self.fitted_model.aic:.2f}")
        return self.fitted_model
    
    def predict(self, steps: int = 1) -> np.ndarray:
        """Make predictions"""
        if self.fitted_model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        forecast = self.fitted_model.get_forecast(steps=steps)
        predictions = forecast.predicted_mean.values
        
        return predictions
    
    def get_diagnostics(self) -> Dict:
        """Get model diagnostics"""
        if self.fitted_model is None:
            raise ValueError("Model not trained")
        
        return {
            'aic': self.fitted_model.aic,
            'bic': self.fitted_model.bic,
            'mse': self.fitted_model.mse,
            'rmse': np.sqrt(self.fitted_model.mse)
        }


class EnsemblePredictor:
    """Combine predictions from multiple models"""
    
    def __init__(self, models: Dict[str, Any], weights: Dict[str, float] = None):
        self.models = models
        self.weights = weights or {name: 1/len(models) for name in models}
    
    def predict(self, X: np.ndarray = None, **kwargs) -> np.ndarray:
        """Get ensemble predictions (weighted average)"""
        predictions = {}
        
        for name, model in self.models.items():
            if name == 'lstm':
                predictions[name] = model.predict(**kwargs)
            elif name == 'arima':
                predictions[name] = model.predict(**kwargs)
            else:
                predictions[name] = model.predict(X)
        
        # Weighted average
        ensemble_pred = np.zeros_like(predictions[list(predictions.keys())[0]])
        for name, pred in predictions.items():
            ensemble_pred += self.weights.get(name, 1/len(predictions)) * pred
        
        return ensemble_pred


def train_all_models(X_train: np.ndarray, y_train: np.ndarray, 
                    X_test: np.ndarray, y_test: np.ndarray) -> Dict:
    """Train all available models"""
    logger.info("Training all models")
    
    models = {}
    
    # Random Forest
    rf_trainer = RandomForestTrainer()
    rf_trainer.train(X_train, y_train)
    models['random_forest'] = rf_trainer
    
    # XGBoost
    xgb_trainer = XGBoostTrainer()
    xgb_trainer.train(X_train, y_train)
    models['xgboost'] = xgb_trainer
    
    logger.info("All models trained successfully")
    return models


if __name__ == "__main__":
    # Test model training
    from preprocessing import preprocess_and_engineer
    from data_loader import DataLoader
    
    loader = DataLoader()
    df = loader.load_commodity_data('onion')
    df = preprocess_and_engineer(df)
    
    # Prepare data
    X = df.drop(['date', 'commodity', 'price'], axis=1, errors='ignore').values
    y = df['price'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Train Random Forest
    rf_trainer = RandomForestTrainer()
    rf_trainer.train(X_train, y_train)
    rf_pred = rf_trainer.predict(X_test)
    print(f"Random Forest predictions shape: {rf_pred.shape}")
    
    # Train XGBoost
    xgb_trainer = XGBoostTrainer()
    xgb_trainer.train(X_train, y_train)
    xgb_pred = xgb_trainer.predict(X_test)
    print(f"XGBoost predictions shape: {xgb_pred.shape}")
