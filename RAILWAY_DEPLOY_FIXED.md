# 🚀 Railway Deployment - FIXED!

The "start.sh not found" error is now fixed! Follow these steps:

## ✅ Step 1: Commit & Push New Files

I've created the missing files. Now commit them:

```bash
cd /Users/vishal/Desktop/newton_automate

# Add all files
git add .

# Commit
git commit -m "Add Railway start and build scripts"

# Push to GitHub
git push
```

## ✅ Step 2: Configure Railway (IMPORTANT!)

### Option A: Set Root Directory (Required!)

**This is the KEY step most people miss:**

1. Go to **Railway Dashboard** → Your project
2. Click **Settings** (⚙️ icon on left sidebar)
3. Scroll to **Service Settings**
4. Find **Root Directory**
5. Type: `backend`
6. Click **Save**

### Option B: Set Build & Start Commands

Still in Settings:

1. Scroll to **Build** section
2. Set **Build Command:**
   ```bash
   ./build.sh
   ```

3. Scroll to **Deploy** section
4. Set **Start Command:**
   ```bash
   ./start.sh
   ```

5. Click **Save**

## ✅ Step 3: Redeploy

After setting root directory:

1. Click **Deployments** (left sidebar)
2. Click **New Deployment** or **Redeploy** button
3. Wait 3-5 minutes
4. ✅ Should work now!

---

## 🎯 Alternative: Fresh Railway Setup

If still not working, delete and recreate:

### 1. Delete Current Railway Project

1. Railway Dashboard → Your project
2. Settings → Danger Zone → Delete Service
3. Confirm deletion

### 2. Create New Project

1. Railway Dashboard → **New Project**
2. Click **Deploy from GitHub repo**
3. Select your `newton-autopilot` repository
4. **IMMEDIATELY after creating:**
   - Go to Settings
   - Set Root Directory: `backend`
   - Save
5. Railway will auto-deploy

---

## 🆘 Still Getting Errors?

### Check Railway Logs

1. Railway Dashboard → Deployments
2. Click the active deployment
3. Click **View Logs**
4. Look for specific error messages

### Common Issues:

**"Module not found: main"**
→ Root directory not set to `backend`

**"Permission denied: start.sh"**
→ The files should be executable (already fixed)

**"playwright: command not found"**
→ Add to environment variables: `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0`

---

## ⚡ Faster Alternative: Use Render.com

Render is simpler and works first try:

### Quick Render Deploy:

1. **Go to [render.com](https://render.com/)** → Sign up (free)

2. **Click "New +"** → "Web Service"

3. **Connect GitHub** → Select `newton-autopilot` repo

4. **Configure:**
   - Name: `newton-autopilot-backend`
   - **Root Directory:** `backend` ← IMPORTANT!
   - Environment: `Python 3`
   - Build Command:
     ```bash
     pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - Start Command:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

5. **Add Environment Variables:**
   - `NEWTON_EMAIL`
   - `NEWTON_PASSWORD`
   - `ANTHROPIC_API_KEY`
   - `SECRET_KEY`
   - `API_HOST=0.0.0.0`
   - `FRONTEND_URL` (add after Vercel)

6. **Click "Create Web Service"**

7. Wait 5-7 minutes → Done! ✅

**Render free tier:**
- ✅ Works great
- ⚠️ Spins down after 15 min inactivity (cold start 30-60s)
- ✅ 750 hours/month free

---

## 📋 Deployment Checklist

Make sure you have:

- [x] Created `start.sh` and `build.sh` (done ✅)
- [x] Made them executable (done ✅)
- [ ] Committed and pushed to GitHub
- [ ] Set Root Directory to `backend` in Railway
- [ ] Added all environment variables
- [ ] Redeployed

---

## ✅ Success Indicators

You'll know it worked when:

- ✅ Build logs show "Build complete!"
- ✅ Deploy logs show "Starting Newton Autopilot Backend..."
- ✅ Service status shows "Active" 🟢
- ✅ Health check works: `https://your-app.railway.app/health`

---

## 🎯 My Recommendation

**For easiest deployment:**

1. **Use Render.com** instead of Railway
   - More reliable for Python apps
   - Simpler configuration
   - Works first try

2. **Or fix Railway** by setting root directory

Both are free and work great!

---

## 💡 Pro Tip

After deploying backend successfully:

1. Copy your backend URL (Railway or Render)
2. Update Vercel environment variable:
   - `NEXT_PUBLIC_API_URL=https://your-backend-url`
3. Redeploy Vercel frontend
4. Update backend environment variable:
   - `FRONTEND_URL=https://your-vercel-url`

---

**The files are ready! Now just:**
1. Commit & push ✅
2. Set root directory in Railway ✅
3. Redeploy ✅

**Or use Render.com for a simpler experience!** 🚀
