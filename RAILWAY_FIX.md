# 🔧 Railway Deployment Fix

If you're seeing "Script start.sh not found" or build errors, follow these steps:

## 🎯 Solution: Configure Railway Correctly

### Step 1: Set Root Directory

Railway needs to know you're deploying from the `backend` folder:

1. Go to **Railway Dashboard** → Your Project
2. Click **Settings** (left sidebar)
3. Under **Service Settings**, find **Root Directory**
4. Set it to: `backend`
5. Click **Save**

### Step 2: Verify Build & Start Commands

Make sure these are set (Railway usually auto-detects, but let's verify):

**In Settings → Deploy:**

- **Build Command:**
  ```bash
  pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
  ```

- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### Step 3: Deploy Again

After setting the root directory:

1. Click **Deployments** (left sidebar)
2. Click **Deploy** button (top right)
3. Wait 3-5 minutes for build

## 🐛 Alternative: Deploy with Railway CLI

If web interface doesn't work, use Railway CLI:

### Install Railway CLI

```bash
# macOS
brew install railway

# npm (all platforms)
npm install -g @railway/cli

# Verify
railway --version
```

### Deploy from CLI

```bash
cd /Users/vishal/Desktop/newton_automate

# Login
railway login

# Link to project (or create new)
railway link

# Deploy backend
cd backend
railway up

# Add environment variables
railway variables set NEWTON_EMAIL="your.email@gmail.com"
railway variables set NEWTON_PASSWORD="your_password"
railway variables set ANTHROPIC_API_KEY="sk-ant-your-key"
railway variables set SECRET_KEY="your-secret-key"
railway variables set API_HOST="0.0.0.0"
railway variables set FRONTEND_URL="https://your-app.vercel.app"
```

## 🎯 Method 2: Use GitHub Integration

If Railway dashboard is confusing, try this simpler approach:

### Step 1: Push Code to GitHub

```bash
cd /Users/vishal/Desktop/newton_automate

git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/newton-autopilot.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy from GitHub

1. **Railway Dashboard** → **New Project**
2. Click **Deploy from GitHub repo**
3. Select your `newton-autopilot` repository
4. Railway will start deploying

### Step 3: Configure After First Deploy

After the first deployment (even if it fails):

1. Go to **Settings**
2. Set **Root Directory** to: `backend`
3. Click **Redeploy** (top right)

## ✅ Verify Configuration

Your Railway project should have:

- ✅ **Root Directory:** `backend`
- ✅ **Build Command:** Set or auto-detected
- ✅ **Start Command:** Set or auto-detected
- ✅ **Environment Variables:** All 7 variables added
- ✅ **nixpacks.toml** file in backend/ (already created)
- ✅ **railway.toml** file in backend/ (already created)

## 🔍 Check Build Logs

If deployment fails:

1. Railway Dashboard → **Deployments**
2. Click the failed deployment
3. Click **View Logs**
4. Look for specific error messages

Common errors and fixes:

### Error: "Module not found"
**Fix:** Verify `requirements.txt` is in `backend/` folder

### Error: "Playwright not found"
**Fix:** Add to build command:
```bash
pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
```

### Error: "Port already in use"
**Fix:** Ensure start command uses `$PORT`:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Error: "Permission denied"
**Fix:** Add to environment variables:
```env
API_HOST=0.0.0.0
```

## 🚀 Complete Railway Configuration

Here's the complete setup that should work:

### In Railway Dashboard

**Settings → Service:**
- Root Directory: `backend`

**Settings → Deploy:**
- Build Command: `pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Variables:**
```env
NEWTON_EMAIL=your.email@gmail.com
NEWTON_PASSWORD=your_password
ANTHROPIC_API_KEY=sk-ant-your-key
SECRET_KEY=your-secret-key
API_HOST=0.0.0.0
FRONTEND_URL=https://your-app.vercel.app
DATABASE_URL=sqlite:///./data/newton_autopilot.db
```

## 🎯 Still Not Working?

### Try Render.com Instead

Render is sometimes simpler than Railway:

1. Go to [render.com](https://render.com)
2. Sign up (free)
3. Click **New +** → **Web Service**
4. Connect your GitHub repository
5. Configure:
   - **Name:** newton-autopilot-backend
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

6. Add environment variables (same as above)
7. Click **Create Web Service**

**Note:** Render free tier has cold starts (30-60 seconds after inactivity)

## 📞 Need More Help?

If you're still stuck, please share:

1. **Screenshot** of Railway build logs
2. **Specific error message** from logs
3. **Your Railway settings** (root directory, commands)

I'll help you debug! 🔧

## ✅ Success Indicators

You'll know it's working when:

- ✅ Build completes without errors
- ✅ Service shows "Active" status
- ✅ Can access health endpoint: `https://your-app.railway.app/health`
- ✅ API docs load: `https://your-app.railway.app/docs`

---

**Most common fix:** Just set Root Directory to `backend` in Railway Settings! 🎯
