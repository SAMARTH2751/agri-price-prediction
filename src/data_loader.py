"""
Data Loading Module for Agricultural Price Prediction System
Handles downloading, loading, and caching of market data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import json
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and cache agricultural market data"""
    
    def __init__(self, cache_dir: str = "data/cached"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_synthetic_data(self, commodity: str, days: int = 1826) -> pd.DataFrame:
        """
        Generate synthetic agricultural commodity price data
        (1826 days ≈ 5 years)
        
        Each commodity has unique characteristics:
        - Onion: Moderate prices, medium volatility
        - Potato: Lower prices, lower volatility
        - Pulses: Highest prices, highest volatility
        """
        # Use commodity-specific seed for reproducibility but unique patterns
        seed = int(hashlib.md5(commodity.lower().encode()).hexdigest(), 16) % (10**8)
        np.random.seed(seed)
        
        # Generate date range
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Base prices by commodity (in Indian Rupees)
        base_prices = {
            'onion': 2000,
            'potato': 1500,
            'pulses': 5000
        }
        
        commodity_lower = commodity.lower()
        base_price = base_prices.get(commodity_lower, 2000)
        
        # Generate price patterns specific to each commodity
        if commodity_lower == 'onion':
            # Onion: Moderate trend, strong seasonality, medium noise
            trend = np.linspace(0, 300, days)
            seasonality = 400 * np.sin(np.arange(days) * 2 * np.pi / 365)
            noise = np.random.normal(0, 200, days)
            volume_base = 5000
            supply_base = 2500
            demand_base = 2500
            
        elif commodity_lower == 'potato':
            # Potato: Lower trend, moderate seasonality, lower noise
            trend = np.linspace(0, 250, days)
            seasonality = 300 * np.sin(np.arange(days) * 2 * np.pi / 365 + np.pi/4)
            noise = np.random.normal(0, 150, days)
            volume_base = 4000
            supply_base = 2000
            demand_base = 2000
            
        else:  # pulses
            # Pulses: Strong trend, high seasonality, higher noise
            trend = np.linspace(0, 800, days)
            seasonality = 600 * np.sin(np.arange(days) * 2 * np.pi / 365 + np.pi/2)
            noise = np.random.normal(0, 300, days)
            volume_base = 3000
            supply_base = 1500
            demand_base = 1500
        
        # Calculate prices
        prices = base_price + trend + seasonality + noise
        prices = np.maximum(prices, base_price * 0.5)  # Ensure prices don't go negative
        
        # Create DataFrame with all numeric data
        df = pd.DataFrame({
            'date': dates,
            'commodity': [commodity.capitalize()] * days,
            'price': prices.astype(float),
            'open': (prices * (1 + np.random.uniform(-0.02, 0.02, days))).astype(float),
            'high': (prices * (1 + np.random.uniform(0, 0.05, days))).astype(float),
            'low': (prices * (1 - np.random.uniform(0, 0.05, days))).astype(float),
            'volume': np.random.uniform(volume_base * 0.7, volume_base * 1.3, days).astype(float),
            'supply': np.random.uniform(supply_base * 0.5, supply_base * 1.5, days).astype(float),
            'demand': np.random.uniform(demand_base * 0.5, demand_base * 1.5, days).astype(float),
            'temperature': (25 + 10 * np.sin(np.arange(days) * 2 * np.pi / 365) + np.random.normal(0, 2, days)).astype(float),
            'humidity': (60 + 20 * np.sin(np.arange(days) * 2 * np.pi / 365) + np.random.normal(0, 5, days)).astype(float),
        })
        
        return df.sort_values('date').reset_index(drop=True)
    
    def load_commodity_data(self, commodity: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Load price data for specified commodity
        
        Args:
            commodity: Commodity name (onion, potato, pulses)
            use_cache: Whether to use cached data if available
        
        Returns:
            DataFrame with commodity price data
        """
        commodity_lower = commodity.lower().strip()
        cache_file = self.cache_dir / f"{commodity_lower}_data.csv"
        
        # Try to load from cache
        if use_cache and cache_file.exists():
            logger.info(f"Loading {commodity_lower} data from cache")
            df = pd.read_csv(cache_file)
            df['date'] = pd.to_datetime(df['date'])
            return df
        
        # Generate synthetic data (in production, this would fetch from AGMARKET API)
        logger.info(f"Generating synthetic data for {commodity_lower}")
        df = self.generate_synthetic_data(commodity_lower)
        
        # Cache the data
        df.to_csv(cache_file, index=False)
        logger.info(f"Cached {commodity_lower} data to {cache_file}")
        
        return df
    
    def load_all_commodities(self, commodities: List[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Load data for all commodities
        
        Args:
            commodities: List of commodity names. Defaults to onion, potato, pulses
        
        Returns:
            Dictionary with commodity names as keys and DataFrames as values
        """
        if commodities is None:
            commodities = ['onion', 'potato', 'pulses']
        
        data = {}
        for commodity in commodities:
            data[commodity] = self.load_commodity_data(commodity)
            logger.info(f"Loaded {len(data[commodity])} records for {commodity}")
        
        return data
    
    def get_data_stats(self, df: pd.DataFrame) -> Dict:
        """
        Get basic statistics for commodity data
        
        Args:
            df: DataFrame with price data
        
        Returns:
            Dictionary with various statistics
        """
        return {
            'commodity': df['commodity'].iloc[0] if 'commodity' in df.columns else 'unknown',
            'records': len(df),
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'price_mean': float(df['price'].mean()),
            'price_std': float(df['price'].std()),
            'price_min': float(df['price'].min()),
            'price_max': float(df['price'].max()),
            'price_median': float(df['price'].median()),
            'missing_values': df.isnull().sum().to_dict()
        }


class APIDataLoader(DataLoader):
    """Fetch data from AGMARKET API (when available)"""
    
    def __init__(self, api_key: str = None, cache_dir: str = "data/cached"):
        super().__init__(cache_dir)
        self.api_key = api_key
        self.api_url = "https://api.agmarket.gov.in/v1"
    
    def fetch_from_agmarket_api(self, commodity: str, state: str = None, 
                                market: str = None) -> pd.DataFrame:
        """
        Fetch data from AGMARKET API
        In production, this would connect to real API
        Falls back to synthetic data if API is unavailable
        
        Args:
            commodity: Commodity name
            state: State name (optional)
            market: Market name (optional)
        
        Returns:
            DataFrame with market data
        """
        logger.info(f"Attempting to fetch {commodity} data from AGMARKET API")
        
        try:
            # In production, implement actual API call here
            # Example:
            # response = requests.get(
            #     f"{self.api_url}/commodities/{commodity}",
            #     headers={"Authorization": f"Bearer {self.api_key}"},
            #     params={"state": state, "market": market}
            # )
            # return pd.json_normalize(response.json())
            
            logger.warning("API not configured, using synthetic data")
            return self.generate_synthetic_data(commodity)
            
        except Exception as e:
            logger.error(f"Failed to fetch from API: {str(e)}")
            logger.warning("Falling back to synthetic data")
            return self.generate_synthetic_data(commodity)


def load_data(commodity: str, data_source: str = 'cache') -> pd.DataFrame:
    """
    Convenience function to load data
    
    Args:
        commodity: Commodity name
        data_source: Source type ('cache' or 'api')
    
    Returns:
        DataFrame with commodity data
    """
    loader = DataLoader()
    use_cache = (data_source == 'cache')
    return loader.load_commodity_data(commodity, use_cache=use_cache)


if __name__ == "__main__":
    # Test data loading
    print("\n" + "="*60)
    print("AGRICULTURAL PRICE PREDICTION - DATA LOADER TEST")
    print("="*60)
    
    loader = DataLoader()
    
    for commodity in ['onion', 'potato', 'pulses']:
        print(f"\n{commodity.upper()} Data:")
        print("-" * 60)
        
        df = loader.load_commodity_data(commodity, use_cache=False)
        stats = loader.get_data_stats(df)
        
        print(json.dumps(stats, indent=2, default=str))
        
        print(f"\nSample data (first 5 rows):")
        print(df.head())
        print(f"\nPrice range: ₹{stats['price_min']:.2f} - ₹{stats['price_max']:.2f}")
        print(f"Average price: ₹{stats['price_mean']:.2f}")