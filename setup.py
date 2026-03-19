"""
Setup configuration for Agricultural Price Prediction System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="agri-price-prediction",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI/ML-Based Price Prediction System for Agricultural Commodities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/agri-price-prediction",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Farmers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "xgboost>=2.0.0",
        "tensorflow>=2.13.0",
        "statsmodels>=0.14.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "pylint>=2.17.0",
            "flake8>=6.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "notebook>=7.0.0",
            "ipython>=8.14.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agri-predict=app.streamlit_app:main",
        ],
    },
    include_package_data=True,
    keywords="agriculture machine-learning price-prediction forecasting",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/agri-price-prediction/issues",
        "Source": "https://github.com/yourusername/agri-price-prediction",
        "Documentation": "https://github.com/yourusername/agri-price-prediction/wiki",
    },
)
