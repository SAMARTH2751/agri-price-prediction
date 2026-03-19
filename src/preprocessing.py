"""
Data Preprocessing and Feature Engineering Module
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess agricultural market data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def handle_missing_values(self, df):
        """Handle missing values in the data"""
        # Only calculate mean for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        # For non-numeric columns, fill with 0
        df = df.fillna(value=0)
        return df
    
    def detect_and_remove_outliers(self, df):
        """Detect and handle outliers using IQR method"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col != 'price':  # Don't remove price outliers
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_count = len(df[(df[col] < lower_bound) | (df[col] > upper_bound)])
                if outlier_count > 0:
                    logger.info(f"{col}: {outlier_count} outliers found")
                    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        return df
    
    def preprocess_pipeline(self, df):
        """Complete preprocessing pipeline"""
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # 1. Handle missing values
        df = self.handle_missing_values(df)
        
        # 2. Detect and remove outliers (except price)
        df = self.detect_and_remove_outliers(df)
        
        # 3. Check missing values
        missing_count = df.isnull().sum().sum()
        logger.info(f"Missing values remaining: {missing_count}")
        
        # NOTE: DO NOT SCALE PRICE - Keep actual rupee values!
        # We only scale other features if needed
        
        return df


class FeatureEngineer:
    """Create new features for model training"""
    
    @staticmethod
    def create_lagged_features(df, lags=[1, 7, 14, 30]):
        """Create lagged price features"""
        for lag in lags:
            df[f'price_lag_{lag}'] = df['price'].shift(lag)
        return df
    
    @staticmethod
    def create_rolling_features(df, windows=[7, 14, 30]):
        """Create rolling statistics"""
        for window in windows:
            df[f'price_ma_{window}'] = df['price'].rolling(window=window).mean()
            df[f'price_std_{window}'] = df['price'].rolling(window=window).std()
            df[f'price_max_{window}'] = df['price'].rolling(window=window).max()
            df[f'price_min_{window}'] = df['price'].rolling(window=window).min()
        return df
    
    @staticmethod
    def create_trend_features(df):
        """Create trend features"""
        df['price_change'] = df['price'].diff()
        df['price_pct_change'] = df['price'].pct_change()
        df['trend'] = np.where(df['price_change'] > 0, 1, 0)
        return df
    
    @staticmethod
    def create_volatility_features(df, window=30):
        """Create volatility features"""
        df['volatility'] = df['price'].rolling(window=window).std()
        return df
    
    @staticmethod
    def create_date_features(df):
        """Create date-based features"""
        if 'date' in df.columns:
            df['day_of_week'] = df['date'].dt.dayofweek
            df['day_of_year'] = df['date'].dt.dayofyear
            df['month'] = df['date'].dt.month
            df['quarter'] = df['date'].dt.quarter
        return df
    
    @staticmethod
    def engineer_features(df):
        """Apply all feature engineering techniques"""
        df = df.copy()
        
        # Create all features
        df = FeatureEngineer.create_lagged_features(df)
        df = FeatureEngineer.create_rolling_features(df)
        df = FeatureEngineer.create_trend_features(df)
        df = FeatureEngineer.create_volatility_features(df)
        df = FeatureEngineer.create_date_features(df)
        
        # Remove NaN values created by feature engineering
        df = df.dropna()
        
        return df


def preprocess_and_engineer(df):
    """Complete preprocessing and feature engineering pipeline"""
    preprocessor = DataPreprocessor()
    engineer = FeatureEngineer()
    
    # Preprocess
    df = preprocessor.preprocess_pipeline(df)
    
    # Engineer features
    df = engineer.engineer_features(df)
    
    logger.info("Preprocessing and feature engineering completed")
    
    return df


if __name__ == "__main__":
    # Test preprocessing
    from src.data_loader import DataLoader
    
    loader = DataLoader()
    df = loader.load_commodity_data('onion')
    
    preprocessor = DataPreprocessor()
    df_clean = preprocessor.preprocess_pipeline(df)
    
    print("\n=== Original Data ===")
    print(df['price'].describe())
    
    print("\n=== Preprocessed Data ===")
    print(df_clean['price'].describe())