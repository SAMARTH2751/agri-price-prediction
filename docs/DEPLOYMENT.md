# 🚀 Deployment Guide

## Complete Instructions for Deploying AI/ML Price Prediction System

---

## Table of Contents

1. [Local Development](#1-local-development)
2. [Streamlit Cloud (Free)](#2-streamlit-cloud-free--recommended)
3. [Heroku](#3-heroku-paid--easiest-paid)
4. [AWS EC2](#4-aws-ec2-flexible)
5. [Docker Hub](#5-docker-hub-registry)
6. [GitHub Actions CI/CD](#6-github-actions-cicd)

---

## 1. Local Development

### Prerequisites
- Python 3.8+
- Git
- 4GB RAM minimum

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/agri-price-prediction.git
cd agri-price-prediction

# Create virtual environment
python -m venv venv

# Activate environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app/streamlit_app.py
```

### Access
```
Local: http://localhost:8501
```

### Development Workflow

```bash
# Make changes to code

# Test locally
pytest tests/

# Format code
black src/ app/

# Check linting
pylint src/

# Commit and push
git add .
git commit -m "Your message"
git push origin main
```

---

## 2. Streamlit Cloud (Free - Recommended)

### Why Streamlit Cloud?
- ✅ **Free tier available**
- ✅ **Automatic deployment from GitHub**
- ✅ **HTTPS included**
- ✅ **Easy to manage**
- ✅ **Perfect for demos**

### Step-by-Step Setup

#### Step 1: GitHub Repository
```bash
# Initialize git repo (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Agricultural price prediction system"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/agri-price-prediction.git
git branch -M main
git push -u origin main
```

#### Step 2: Create Streamlit Cloud Account
1. Go to [streamlit.app](https://streamlit.app)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your repositories

#### Step 3: Deploy Application
1. Click "Create app"
2. Select your repository: `agri-price-prediction`
3. Branch: `main`
4. File path: `app/streamlit_app.py`
5. Click "Deploy"

#### Step 4: Configure Secrets (Optional)
Create `.streamlit/secrets.toml`:
```toml
[api]
agmarket_key = "your_api_key_here"

[database]
connection_string = "your_db_string"
```

### Access Your App
```
https://yourusername-agri-price-prediction.streamlit.app
```

### Continuous Deployment
- Automatically redeploys on every push to `main` branch
- See logs in Streamlit dashboard

---

## 3. Heroku (Paid - Easiest Paid Option)

### Cost: $7/month minimum

### Prerequisites
- Heroku account (create at heroku.com)
- Heroku CLI installed

### Setup

#### Step 1: Install Heroku CLI
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Windows
Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli.heroku.com/install.sh | sh
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create `Procfile`
```
web: streamlit run --server.port=$PORT app/streamlit_app.py
```

#### Step 4: Create `runtime.txt`
```
python-3.10.11
```

#### Step 5: Deploy
```bash
# Create Heroku app
heroku create agri-price-prediction

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

#### Step 6: Scale (Optional)
```bash
# Single dyno (free tier)
heroku ps:scale web=1

# Multiple dynos (paid)
heroku ps:scale web=2
```

### Access Your App
```
https://agri-price-prediction.herokuapp.com
```

### Environment Variables
```bash
heroku config:set AGMARKET_API_KEY=your_key_here
```

### Monitor Performance
```bash
# View dashboard
heroku open

# View metrics
heroku metrics
```

---

## 4. AWS EC2 (Flexible - Most Control)

### Cost: $5-50/month depending on instance

### Prerequisites
- AWS Account
- AWS CLI installed
- SSH client

### Step-by-Step

#### Step 1: Launch EC2 Instance
```bash
# Using AWS Console:
1. Go to EC2 Dashboard
2. Launch Instance
3. Select: Ubuntu 22.04 LTS (Free tier eligible)
4. Instance type: t2.micro (Free tier)
5. Create security group allowing:
   - SSH (Port 22): 0.0.0.0/0
   - HTTP (Port 80): 0.0.0.0/0
   - HTTPS (Port 443): 0.0.0.0/0
6. Create key pair (save .pem file safely)
7. Launch
```

#### Step 2: Connect to Instance
```bash
# Change permissions
chmod 400 your-key.pem

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-public-ip
```

#### Step 3: Install Dependencies
```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3-pip python3-venv

# Install git
sudo apt install -y git

# Install nginx (optional, for reverse proxy)
sudo apt install -y nginx
```

#### Step 4: Clone and Setup Project
```bash
# Clone repository
git clone https://github.com/yourusername/agri-price-prediction.git
cd agri-price-prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 5: Run with Systemd (Background Service)
Create `/etc/systemd/system/agri-predict.service`:
```ini
[Unit]
Description=Agricultural Price Prediction System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agri-price-prediction
Environment="PATH=/home/ubuntu/agri-price-prediction/venv/bin"
ExecStart=/home/ubuntu/agri-price-prediction/venv/bin/streamlit run app/streamlit_app.py --server.port=8501

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable agri-predict
sudo systemctl start agri-predict
sudo systemctl status agri-predict
```

#### Step 6: Configure Nginx as Reverse Proxy (Optional)
Edit `/etc/nginx/sites-available/default`:
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Enable:
```bash
sudo systemctl restart nginx
```

#### Step 7: Setup SSL Certificate (Optional)
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

### Access Your App
```
http://your-instance-public-ip:8501
or
https://your-domain.com (if configured)
```

### Monitor
```bash
# Check service status
sudo systemctl status agri-predict

# View logs
sudo journalctl -u agri-predict -f

# Monitor resource usage
top
```

---

## 5. Docker Hub Registry

### Push Docker Image to Docker Hub

#### Step 1: Create Docker Hub Account
- Go to [Docker Hub](https://hub.docker.com)
- Sign up for free account

#### Step 2: Create Repository
1. Click "Create Repository"
2. Name: `agri-price-prediction`
3. Make it public
4. Create

#### Step 3: Build and Push
```bash
# Login to Docker Hub
docker login

# Build image
docker build -t yourusername/agri-price-prediction:latest .

# Push to Docker Hub
docker push yourusername/agri-price-prediction:latest

# Verify
docker search yourusername/agri-price-prediction
```

#### Step 4: Deploy from Docker Hub
```bash
# Pull and run
docker run -p 8501:8501 yourusername/agri-price-prediction:latest

# Or with Docker Compose
docker pull yourusername/agri-price-prediction:latest
docker-compose up
```

---

## 6. GitHub Actions CI/CD

### Automated Testing and Deployment

Create `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        files: ./coverage.xml
    
    - name: Lint with pylint
      run: |
        pip install pylint
        pylint src/ --fail-under=7.0 || true
    
    - name: Format check with black
      run: |
        pip install black
        black --check src/ app/ || true

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Streamlit Cloud
      env:
        STREAMLIT_CLOUD_TOKEN: ${{ secrets.STREAMLIT_CLOUD_TOKEN }}
      run: |
        # Streamlit cloud auto-deploys on push
        echo "Deployment triggered!"
    
    - name: Deploy to Heroku
      env:
        HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
      run: |
        npm install -g heroku
        heroku login
        heroku git:remote -a agri-price-prediction
        git push heroku main
```

Set secrets in GitHub:
```bash
# In GitHub settings > Secrets:
- STREAMLIT_CLOUD_TOKEN
- HEROKU_API_KEY
```

---

## 7. Comparison Table

| Platform | Cost | Setup Time | Best For | Deployment |
|----------|------|-----------|----------|-----------|
| Local | Free | 5 min | Development | Manual |
| Streamlit Cloud | Free | 10 min | Demo/Prototype | Auto (Git) |
| Heroku | $7+/mo | 15 min | Small production | Git push |
| AWS EC2 | $5-50/mo | 30 min | Scalable prod | Manual/SSH |
| Docker Hub | Free | 20 min | Container registry | Docker pull |

---

## 8. Production Checklist

Before deploying to production:

- [ ] All tests passing (pytest)
- [ ] Code formatted (black)
- [ ] No linting errors (pylint)
- [ ] Security secrets in .env (not in code)
- [ ] Database backups configured
- [ ] Monitoring/logging enabled
- [ ] Error handling comprehensive
- [ ] Documentation updated
- [ ] README has deploy instructions
- [ ] Environment variables documented

---

## 9. Monitoring & Maintenance

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
```bash
# Check service running
curl http://localhost:8501/_stcore/health

# Monitor resource usage
docker stats agri-price-prediction
```

### Auto-Restart
```bash
# Systemd (Linux)
Restart=always
RestartSec=10

# Docker
docker run --restart always agri-price-prediction
```

---

## 10. Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>
```

**Module not found**
```bash
# Ensure virtual environment activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**GPU not detected (LSTM)**
```bash
# Install CUDA-enabled TensorFlow
pip install tensorflow[and-cuda]
```

**Database connection error**
```bash
# Check connection string in .env
# Verify database is running
# Check firewall rules
```

---

## 11. Scaling Considerations

### As Traffic Increases

1. **Load Balancing**
   - Nginx load balancer
   - AWS Application Load Balancer
   - Kubernetes

2. **Caching**
   - Redis for predictions
   - CDN for static assets

3. **Database**
   - Migrate to managed DB (RDS)
   - Add read replicas
   - Implement sharding

4. **Containerization**
   - Kubernetes orchestration
   - Auto-scaling policies
   - Multi-region deployment

---

## Quick Links

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Heroku Python Buildpack](https://github.com/heroku/heroku-buildpack-python)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Last Updated**: March 2026  
**Status**: ✅ Production Ready
