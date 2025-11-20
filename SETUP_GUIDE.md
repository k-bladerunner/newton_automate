# Newton Autopilot - Complete Setup Guide

This guide will walk you through setting up Newton Autopilot from scratch.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [First Run](#first-run)
5. [Production Deployment](#production-deployment)

## System Requirements

### Required Software

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 20+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Optional (for Docker deployment)

- **Docker** - [Download](https://www.docker.com/get-started)
- **Docker Compose** - Usually included with Docker Desktop

### Required Accounts

- Newton School account with Google login
- Anthropic API account - [Sign up](https://www.anthropic.com/)

## Installation Steps

### Step 1: Get Anthropic API Key

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)
6. Keep it secure - you'll need it for configuration

### Step 2: Clone or Download Project

If using Git:
```bash
git clone <repository-url>
cd newton_automate
```

Or download and extract the ZIP file, then navigate to the directory.

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows Command Prompt:
venv\Scripts\activate.bat

# On Windows PowerShell:
venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Install system dependencies for Playwright (Linux/macOS)
playwright install-deps chromium
```

### Step 4: Frontend Setup

Open a new terminal window/tab:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# This may take a few minutes
```

## Configuration

### Backend Configuration

1. Create `.env` file:

```bash
cd backend
cp .env.example .env
```

2. Edit `.env` file with your actual credentials:

```env
# Newton School Credentials
NEWTON_EMAIL=your.email@gmail.com
NEWTON_PASSWORD=your_actual_password

# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here

# Server Configuration (can leave as default)
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000

# Database (can leave as default)
DATABASE_URL=sqlite:///./newton_autopilot.db

# Security (CHANGE THIS IN PRODUCTION!)
SECRET_KEY=your-secret-key-change-this-in-production
```

**Important:**
- Replace `your.email@gmail.com` with your Newton School Gmail
- Replace `your_actual_password` with your Google password
- Replace `sk-ant-your-actual-api-key-here` with your Anthropic API key
- Change `SECRET_KEY` to a random string in production

### Frontend Configuration

1. Create `.env.local` file:

```bash
cd frontend
cp .env.local.example .env.local
```

2. Edit if needed (default should work for local development):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## First Run

### Start Backend

```bash
# In backend directory, with venv activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Backend is now running at:** `http://localhost:8000`
**API Documentation:** `http://localhost:8000/docs`

### Start Frontend

Open a **new terminal window/tab**:

```bash
# In frontend directory
cd frontend
npm run dev
```

You should see:
```
   ▲ Next.js 14.1.0
   - Local:        http://localhost:3000
   - Ready in 2.3s
```

**Frontend is now running at:** `http://localhost:3000`

### Test the Application

1. Open your browser and go to `http://localhost:3000`
2. You should see the login page
3. Enter your Newton School credentials
4. Click "Login with Google"
5. A browser window will open automatically (Playwright automation)
6. Wait for authentication to complete
7. You'll be redirected to the dashboard

**Note:** The first login may take 30-60 seconds as Playwright automates the Google OAuth flow.

## Production Deployment

### Option 1: Docker Deployment (Recommended)

1. **Install Docker and Docker Compose**

2. **Configure environment:**

```bash
# Edit backend .env file
nano backend/.env
# Add your production credentials
```

3. **Build and start containers:**

```bash
docker-compose up -d
```

4. **Verify deployment:**

```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs -f

# Access application
# Frontend: http://your-server-ip:3000
# Backend: http://your-server-ip:8000
```

### Option 2: VPS/Server Deployment

#### On Your Server (Ubuntu/Debian):

1. **Install requirements:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Install Git
sudo apt install git -y
```

2. **Clone repository:**

```bash
git clone <repository-url>
cd newton_automate
```

3. **Set up backend:**

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
playwright install-deps

# Configure .env
nano .env
# Add your credentials
```

4. **Set up frontend:**

```bash
cd ../frontend
npm install
npm run build
```

5. **Run with process manager (PM2):**

```bash
# Install PM2
sudo npm install -g pm2

# Start backend
cd backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name newton-backend

# Start frontend
cd ../frontend
pm2 start "npm start" --name newton-frontend

# Save PM2 configuration
pm2 save
pm2 startup
```

6. **Set up Nginx (optional but recommended):**

```bash
# Install Nginx
sudo apt install nginx -y

# Create configuration
sudo nano /etc/nginx/sites-available/newton-autopilot
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/newton-autopilot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Set up SSL (recommended):**

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Certbot will automatically configure Nginx for HTTPS
```

## Troubleshooting

### Common Issues

**Issue: "Module not found" errors**
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue: "Playwright browser not found"**
```bash
cd backend
source venv/bin/activate
playwright install chromium
playwright install-deps
```

**Issue: "Authentication failed"**
- Verify your email and password in `.env`
- Make sure your Google account has access to Newton School
- Check if 2FA is enabled (may need app-specific password)

**Issue: "API connection refused"**
- Make sure backend is running on port 8000
- Check firewall settings
- Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`

**Issue: Database errors**
```bash
# Delete and recreate database
cd backend
rm newton_autopilot.db
python main.py  # Will create new database
```

### Getting Help

If you encounter issues:

1. Check the logs:
   - Backend: Terminal where `python main.py` is running
   - Frontend: Terminal where `npm run dev` is running
   - Docker: `docker-compose logs -f`

2. Check API documentation: `http://localhost:8000/docs`

3. Verify all environment variables are set correctly

## Security Best Practices

1. **Never commit `.env` files to Git**
2. **Use strong SECRET_KEY in production**
3. **Keep API keys secure**
4. **Use HTTPS in production**
5. **Regularly update dependencies**
6. **Set up firewall rules on production servers**

## Next Steps

After successful setup:

1. Explore the dashboard
2. Try solving an assignment in "Learning Mode" first
3. Review the AI solutions to understand the logic
4. Check your performance analytics
5. Set up notifications for upcoming deadlines

---

**Congratulations! Your Newton Autopilot is ready to use! 🎉**
