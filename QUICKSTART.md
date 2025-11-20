# Newton Autopilot - Quick Start Guide ⚡

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 20+ installed
- [ ] Newton School Google account
- [ ] Anthropic API key ([Get one here](https://console.anthropic.com/))

## Setup in 4 Steps

### 1️⃣ Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2️⃣ Configure Environment

**Backend** (`backend/.env`):
```bash
cp .env.example .env
nano .env  # or use any editor
```

Add your credentials:
```env
NEWTON_EMAIL=your.email@gmail.com
NEWTON_PASSWORD=your_password
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Frontend** (`frontend/.env.local`):
```bash
cp .env.local.example .env.local
# Default settings work for local development
```

### 3️⃣ Start Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4️⃣ Access Application

Open your browser: **http://localhost:3000**

Login with your Newton School credentials and you're ready! 🎉

## Quick Docker Start (Alternative)

If you have Docker installed:

```bash
# 1. Configure backend/.env as shown above
# 2. Run:
docker-compose up -d

# Access at http://localhost:3000
```

## What to Do Next?

1. **Explore Dashboard** - See your performance stats and upcoming classes
2. **Try AI Solver** - Go to Assignments → Pick one → Click "Solve"
3. **Learning Mode** - Start with "Learning Mode" to see how AI solves problems
4. **Auto Mode** - Use "Auto-Submit" when you're confident

## Need Help?

- Full documentation: See `README.md`
- Detailed setup: See `SETUP_GUIDE.md`
- API docs: http://localhost:8000/docs
- Issues? Check the Troubleshooting section in README.md

## Important Notes

⚠️ **Security:**
- Never commit your `.env` file
- Keep your API keys secure
- Use strong passwords

💡 **Usage Tips:**
- Start with Learning Mode to understand solutions
- Use for learning, not cheating
- Review AI-generated solutions before submitting
- Understand the logic behind solutions

---

**Happy Learning! 📚✨**
