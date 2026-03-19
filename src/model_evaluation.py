"""
Model Evaluation Module for Agricultural Price Prediction System
Comprehensive metrics and evaluation tools
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging
from typing import Dict, Tuple
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate model performance with multiple metrics"""
    
    @staticmethod
    def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Root Mean Squared Error"""
        return np.sqrt(mean_squared_error(y_true, y_pred))
    
    @staticmethod
    def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Error"""
        return mean_absolute_error(y_true, y_pred)
    
    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Percentage Error"""
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    @staticmethod
    def calculate_mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Squared Error"""
        return mean_squared_error(y_true, y_pred)
    
    @staticmethod
    def calculate_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate R² Score"""
        return r2_score(y_true, y_pred)
    
    @staticmethod
    def calculate_adjusted_r2(y_true: np.ndarray, y_pred: np.ndarray, 
                            n_features: int) -> float:
        """Calculate Adjusted R² Score"""
        r2 = r2_score(y_true, y_pred)
        n = len(y_true)
        adj_r2 = 1 - (1 - r2) * (n - 1) / (n - n_features - 1)
        return adj_r2
    
    @staticmethod
    def calculate_smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Symmetric Mean Absolute Percentage Error"""
        denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
        diff = np.abs(y_true - y_pred) / denominator
        diff[denominator == 0] = 0
        return 100.0 * np.mean(diff)
    
    @staticmethod
    def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, 
                      model_name: str = "Model", n_features: int = None) -> Dict:
        """Comprehensive model evaluation"""
        logger.info(f"Evaluating {model_name}")
        
        metrics = {
            'model': model_name,
            'timestamp': datetime.now().isoformat(),
            'rmse': ModelEvaluator.calculate_rmse(y_true, y_pred),
            'mae': ModelEvaluator.calculate_mae(y_true, y_pred),
            'mse': ModelEvaluator.calculate_mse(y_true, y_pred),
            'mape': ModelEvaluator.calculate_mape(y_true, y_pred),
            'smape': ModelEvaluator.calculate_smape(y_true, y_pred),
            'r2_score': ModelEvaluator.calculate_r2(y_true, y_pred),
        }
        
        if n_features:
            metrics['adjusted_r2'] = ModelEvaluator.calculate_adjusted_r2(
                y_true, y_pred, n_features
            )
        
        # Additional metrics
        metrics['min_error'] = np.min(np.abs(y_true - y_pred))
        metrics['max_error'] = np.max(np.abs(y_true - y_pred))
        metrics['mean_error'] = np.mean(y_true - y_pred)
        metrics['std_error'] = np.std(y_true - y_pred)
        
        logger.info(f"RMSE: {metrics['rmse']:.2f}, MAPE: {metrics['mape']:.2f}%, R²: {metrics['r2_score']:.4f}")
        
        return metrics
    
    @staticmethod
    def compare_models(models_metrics: Dict[str, Dict]) -> pd.DataFrame:
        """Compare multiple models"""
        logger.info("Comparing models")
        
        df = pd.DataFrame(models_metrics).T
        df = df.sort_values('rmse')
        
        return df
    
    @staticmethod
    def print_evaluation_report(metrics: Dict):
        """Print detailed evaluation report"""
        print("\n" + "="*60)
        print(f"MODEL EVALUATION REPORT: {metrics.get('model', 'Unknown')}")
        print("="*60)
        print(f"\nKey Metrics:")
        print(f"  RMSE (Root Mean Squared Error): {metrics.get('rmse', 0):.4f}")
        print(f"  MAE (Mean Absolute Error):      {metrics.get('mae', 0):.4f}")
        print(f"  MAPE (Mean Absolute % Error):   {metrics.get('mape', 0):.2f}%")
        print(f"  SMAPE (Symmetric MAPE):         {metrics.get('smape', 0):.2f}%")
        print(f"  R² Score:                       {metrics.get('r2_score', 0):.4f}")
        
        if 'adjusted_r2' in metrics:
            print(f"  Adjusted R²:                    {metrics.get('adjusted_r2'):.4f}")
        
        print(f"\nError Analysis:")
        print(f"  Mean Error:                     {metrics.get('mean_error', 0):.4f}")
        print(f"  Std Error:                      {metrics.get('std_error', 0):.4f}")
        print(f"  Min Error:                      {metrics.get('min_error', 0):.4f}")
        print(f"  Max Error:                      {metrics.get('max_error', 0):.4f}")
        print("\n" + "="*60)


class TimeSeriesEvaluator:
    """Specialized evaluation for time-series models"""
    
    @staticmethod
    def calculate_directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate directional accuracy (% of correct direction predictions)"""
        true_direction = np.diff(y_true) > 0
        pred_direction = np.diff(y_pred) > 0
        accuracy = np.mean(true_direction == pred_direction) * 100
        return accuracy
    
    @staticmethod
    def calculate_theil_u(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Theil's U statistic for forecast accuracy"""
        numerator = np.sum((y_true[1:] - y_pred[1:])**2)
        denominator = np.sum((y_true[1:] - y_true[:-1])**2)
        return np.sqrt(numerator / denominator)
    
    @staticmethod
    def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray, 
                         model_name: str = "Forecast") -> Dict:
        """Comprehensive time-series forecast evaluation"""
        logger.info(f"Evaluating forecast: {model_name}")
        
        metrics = {
            'model': model_name,
            'rmse': ModelEvaluator.calculate_rmse(y_true, y_pred),
            'mae': ModelEvaluator.calculate_mae(y_true, y_pred),
            'mape': ModelEvaluator.calculate_mape(y_true, y_pred),
            'r2_score': ModelEvaluator.calculate_r2(y_true, y_pred),
            'directional_accuracy': TimeSeriesEvaluator.calculate_directional_accuracy(y_true, y_pred),
            'theil_u': TimeSeriesEvaluator.calculate_theil_u(y_true, y_pred),
        }
        
        return metrics


class ResidualAnalyzer:
    """Analyze model residuals"""
    
    @staticmethod
    def analyze_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """Analyze residuals"""
        residuals = y_true - y_pred
        
        analysis = {
            'mean': np.mean(residuals),
            'std': np.std(residuals),
            'min': np.min(residuals),
            'max': np.max(residuals),
            'median': np.median(residuals),
            'q1': np.percentile(residuals, 25),
            'q3': np.percentile(residuals, 75),
            'skewness': (np.mean(residuals) - np.median(residuals)) / np.std(residuals) if np.std(residuals) > 0 else 0,
            'autocorrelation_lag1': np.corrcoef(residuals[:-1], residuals[1:])[0, 1],
        }
        
        return analysis
    
    @staticmethod
    def check_residual_normality(residuals: np.ndarray) -> Dict:
        """Check if residuals are normally distributed"""
        from scipy import stats
        
        stat, p_value = stats.shapiro(residuals)
        
        return {
            'shapiro_stat': stat,
            'p_value': p_value,
            'is_normal': p_value > 0.05
        }
    
    @staticmethod
    def check_residual_heteroscedasticity(y_true: np.ndarray, 
                                         y_pred: np.ndarray) -> Dict:
        """Check for heteroscedasticity in residuals"""
        residuals = np.abs(y_true - y_pred)
        
        # Group by prediction quartiles
        quartiles = np.array_split(np.sort(y_pred), 4)
        variances = [residuals[np.isin(y_pred, q)].var() for q in quartiles]
        
        return {
            'quartile_variances': variances,
            'is_homoscedastic': np.std(variances) / np.mean(variances) < 0.5
        }


class ModelComparison:
    """Compare multiple models comprehensively"""
    
    def __init__(self):
        self.results = {}
    
    def add_evaluation(self, model_name: str, metrics: Dict):
        """Add model evaluation results"""
        self.results[model_name] = metrics
    
    def get_comparison_dataframe(self) -> pd.DataFrame:
        """Get comparison as DataFrame"""
        return pd.DataFrame(self.results).T
    
    def rank_models(self, metric: str = 'rmse', ascending: bool = True) -> pd.DataFrame:
        """Rank models by specific metric"""
        df = self.get_comparison_dataframe()
        return df.sort_values(metric, ascending=ascending)
    
    def save_comparison(self, filepath: str):
        """Save comparison results to JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        logger.info(f"Comparison saved to {filepath}")
    
    def print_summary(self):
        """Print summary comparison"""
        df = self.rank_models('rmse')
        print("\n" + "="*80)
        print("MODEL COMPARISON SUMMARY (Ranked by RMSE)")
        print("="*80)
        print(df[['rmse', 'mae', 'mape', 'r2_score']].to_string())
        print("="*80 + "\n")


def evaluate_all_models(models_dict: Dict, X_test: np.ndarray, 
                       y_test: np.ndarray) -> Dict:
    """Evaluate all models and return comprehensive results"""
    logger.info("Evaluating all models")
    
    comparison = ModelComparison()
    
    for model_name, trainer in models_dict.items():
        try:
            y_pred = trainer.predict(X_test)
            metrics = ModelEvaluator.evaluate_model(y_test, y_pred, model_name, X_test.shape[1])
            comparison.add_evaluation(model_name, metrics)
        except Exception as e:
            logger.error(f"Error evaluating {model_name}: {e}")
    
    comparison.print_summary()
    return comparison.results


if __name__ == "__main__":
    # Test evaluation
    y_true = np.random.rand(100) * 1000
    y_pred = y_true + np.random.normal(0, 50, 100)
    
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate_model(y_true, y_pred, "Test Model", n_features=10)
    evaluator.print_evaluation_report(metrics)
