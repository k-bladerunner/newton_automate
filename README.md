# Newton Autopilot 🚀

> AI-powered automation system for Newton School portal with intelligent assignment solving capabilities

## 🎯 Overview

Newton Autopilot is a comprehensive web-based automation system that helps Newton School students manage their coursework efficiently using AI. It features automatic assignment solving, schedule management, performance tracking, and more.

### Key Features

- ✨ **AI-Powered Assignment Solver** - Automatically solve MCQ, coding, and frontend assignments using Claude AI
- 📅 **Smart Schedule Management** - View and join classes with one click
- 📊 **Performance Analytics** - Track attendance, assignments, XP, and streaks
- 🔐 **Secure Authentication** - Google OAuth automation via Playwright
- 🎨 **Modern UI** - Built with Next.js 14, TypeScript, and Tailwind CSS
- 🐳 **Docker Ready** - Easy deployment with Docker Compose

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database for sessions and logs
- **Playwright** - Browser automation for Google OAuth
- **Anthropic Claude** - AI for solving assignments
- **Python 3.11+**

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful UI components
- **SWR** - Data fetching and caching

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 20 or higher
- Docker and Docker Compose (for containerized deployment)
- Google account with Newton School access
- Anthropic API key

## 🚀 Quick Start

### Option 1: Deploy to Production (Vercel + Railway) ⭐ RECOMMENDED

Deploy to the cloud in 10 minutes! See **[DEPLOY_NOW.md](DEPLOY_NOW.md)** for step-by-step guide.

**Quick overview:**
1. Push code to GitHub
2. Deploy backend to Railway (free)
3. Deploy frontend to Vercel (free)
4. Done! Your app is live 🎉

**Full guide:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

### Option 2: Local Development

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Create .env file
cp .env.example .env

# Edit .env file with your credentials
# Add your Newton School email, password, and Anthropic API key
nano .env  # or use your preferred editor

# Run backend server
python main.py
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit if needed (default API URL is http://localhost:8000)
nano .env.local

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Option 3: Docker Deployment (Local)

```bash
# Make sure you have Docker and Docker Compose installed

# Create .env file for backend
cd backend
cp .env.example .env
# Edit .env with your credentials
nano .env

# Return to root directory
cd ..

# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

Access the application:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## ⚙️ Configuration

### Backend Environment Variables (`.env`)

```env
# Newton School Credentials
NEWTON_EMAIL=your.email@gmail.com
NEWTON_PASSWORD=your_password

# AI API Key
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000

# Database
DATABASE_URL=sqlite:///./newton_autopilot.db

# Security
SECRET_KEY=change-this-secret-key-in-production
```

### Frontend Environment Variables (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📖 Usage Guide

### 1. Login

1. Open `http://localhost:3000` in your browser
2. Enter your Newton School Gmail credentials
3. The system will automate Google OAuth login using Playwright
4. You'll be redirected to the dashboard after successful authentication

### 2. Dashboard

The dashboard provides:
- **Performance Overview** - Attendance, assignments completion, total XP, and streak
- **Today's Schedule** - Upcoming classes with join links
- **Deadlines** - Pending assignments sorted by due date
- **Quick Actions** - Fast access to key features

### 3. Assignments

#### View Assignments
- Navigate to "Assignments" from the sidebar
- Filter by status (pending/completed) or difficulty (easy/medium/hard)
- See assignment details, due dates, and XP

#### Solve Assignments
1. Click "Solve" on any assignment
2. Choose solving mode:
   - **Learning Mode** - View AI solutions without submitting
   - **Auto-Submit Mode** - Automatically submit AI-generated answers
3. AI will solve:
   - **MCQ Questions** - Select correct option with explanation
   - **Coding Problems** - Generate complete code solutions
   - **Frontend Tasks** - Create HTML, CSS, and JavaScript

### 4. Schedule

- View today's classes and weekly schedule
- See class times, rooms, and instructors
- Join classes directly with one click

### 5. Performance

- Track overall statistics
- View course-wise performance
- Monitor attendance and assignment completion rates

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - Login with Google OAuth
- `POST /api/auth/logout` - Logout
- `GET /api/auth/status` - Check authentication status
- `GET /api/auth/user/me` - Get current user info

### Assignments
- `GET /api/assignments` - List assignments with filters
- `GET /api/assignments/{hash}` - Get assignment details
- `POST /api/assignments/{hash}/solve` - Solve assignment with AI
- `GET /api/assignments/{hash}/status` - Get completion status

### Schedule
- `GET /api/schedule/today` - Today's schedule
- `GET /api/schedule/week` - Week's schedule
- `POST /api/schedule/join-class` - Get join URL for class

### Performance
- `GET /api/performance/overview` - Overall performance stats
- `GET /api/performance/course/{hash}` - Course-specific performance
- `GET /api/performance/courses` - All courses performance

### AI Solver
- `POST /api/solve/mcq` - Solve MCQ question
- `POST /api/solve/coding` - Solve coding problem
- `POST /api/solve/frontend` - Solve frontend task

## 🏃 Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if you add them)
pytest

# Format code
black .

# Type checking
mypy .
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint
npm run lint
```

## 🔒 Security Notes

- Never commit `.env` files with real credentials
- Keep your Anthropic API key secure
- Use strong `SECRET_KEY` in production
- The authentication uses browser automation - credentials are not stored
- Session cookies are encrypted and stored in SQLite

## 🐛 Troubleshooting

### Backend Issues

**Playwright browser not found:**
```bash
playwright install chromium
playwright install-deps
```

**Database errors:**
```bash
# Delete and recreate database
rm newton_autopilot.db
python main.py  # Database will be recreated automatically
```

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend Issues

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Check that backend is running on `http://localhost:8000`
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📁 Project Structure

```
newton-autopilot/
├── backend/
│   ├── api/              # API route handlers
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   │   ├── newton_client.py    # Newton API wrapper
│   │   ├── ai_solver.py        # Claude AI integration
│   │   └── auth_service.py     # Google OAuth automation
│   ├── utils/            # Utility functions
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── app/              # Next.js app directory
│   │   ├── dashboard/    # Dashboard page
│   │   ├── assignments/  # Assignments page
│   │   ├── schedule/     # Schedule page
│   │   ├── performance/  # Performance page
│   │   └── login/        # Login page
│   ├── components/       # React components
│   │   ├── ui/           # shadcn/ui components
│   │   ├── layout/       # Layout components
│   │   ├── dashboard/    # Dashboard widgets
│   │   └── ...
│   ├── lib/              # Utilities and API client
│   └── package.json      # Node dependencies
├── docker-compose.yml    # Docker Compose config
└── README.md            # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is for educational purposes only. Use responsibly and in accordance with Newton School's terms of service.

## ⚠️ Disclaimer

This tool is designed to assist with learning and should not be used to cheat or violate academic integrity policies. Always ensure you understand the solutions provided by the AI and use them as learning aids.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- AI powered by [Anthropic Claude](https://www.anthropic.com/)
- Browser automation by [Playwright](https://playwright.dev/)

---

**Made with ❤️ for Newton School students**
