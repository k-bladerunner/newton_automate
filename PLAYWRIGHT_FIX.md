# 🔧 Playwright Installation Fix for Railway

The error you're seeing is because Playwright can't install browser dependencies in Railway's environment.

## 🎯 Quick Fix: Use Render.com Instead

**Render.com handles Playwright better than Railway.** Here's how:

### Deploy to Render (5 minutes)

1. **Go to [render.com](https://render.com/)** and sign up (free)

2. **Create New Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub account
   - Select **`newton-autopilot`** repository

3. **Configure Service:**
   - **Name:** `newton-autopilot-backend`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Region:** Oregon (or closest to you)
   - **Branch:** `main`

4. **Build Command:**
   ```bash
   pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
   ```

5. **Start Command:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

6. **Plan:** Select **Free**

7. **Add Environment Variables:**

   Click **"Advanced"** → **"Add Environment Variable"**

   Add these one by one:
   ```
   NEWTON_EMAIL=your.email@gmail.com
   NEWTON_PASSWORD=your_password
   ANTHROPIC_API_KEY=sk-ant-your-key
   SECRET_KEY=random-secret-key
   API_HOST=0.0.0.0
   FRONTEND_URL=https://your-app.vercel.app
   DATABASE_URL=sqlite:///./data/newton_autopilot.db
   PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/.cache/ms-playwright
   ```

8. **Click "Create Web Service"**

9. **Wait 5-7 minutes** for deployment

**✅ Render will install Playwright correctly!**

---

## 🔄 Alternative: Fix Railway (Advanced)

If you really want to use Railway, try this:

### Option 1: Simplify Playwright Installation

1. **In Railway Settings**, set these **Environment Variables:**
   ```
   PLAYWRIGHT_BROWSERS_PATH=0
   PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=false
   ```

2. **Update Build Command** (in Railway Settings):
   ```bash
   pip install -r requirements.txt && PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
   ```

3. **Redeploy**

### Option 2: Use Docker Instead

Create a custom Dockerfile that handles Playwright better.

**But honestly, Render.com is easier!** 😊

---

## 📊 Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| Playwright Support | ✅ Excellent | ⚠️ Tricky |
| Free Tier | 750hrs/month | $5 credit/month |
| Setup | Simpler | More complex |
| Cold Starts | 30-60s | Minimal |
| Best For | Python apps | Node.js apps |

**For this project, Render is the better choice!**

---

## 🚀 After Deploying to Render

1. **Copy your Render URL:**
   - It will be like: `https://newton-autopilot-backend.onrender.com`

2. **Update Vercel:**
   - Go to Vercel → Your project → Settings → Environment Variables
   - Update `NEXT_PUBLIC_API_URL` to your Render URL
   - Redeploy Vercel

3. **Update Render:**
   - Go back to Render → Environment Variables
   - Update `FRONTEND_URL` to your Vercel URL
   - Redeploy will happen automatically

4. **Test:**
   - Visit `https://your-render-url.onrender.com/health`
   - Should see: `{"status":"healthy","api":"operational"}`

---

## ✅ Why Render Works Better

Render has:
- ✅ Built-in support for Playwright
- ✅ Better Ubuntu environment for browser automation
- ✅ More reliable builds
- ✅ Simpler configuration

---

## 🎯 Recommended Path Forward

**Stop fighting with Railway.**

**Use Render instead:**
1. Takes 5 minutes
2. Works first try
3. Free tier is great
4. Better for Python + Playwright

---

## 💡 Pro Tip

Render free tier:
- Spins down after 15 min of inactivity
- Cold start takes 30-60 seconds
- This is fine! The first request after inactivity will just be slower

If you need always-on:
- Upgrade to Render Starter ($7/month)
- Or use Railway with simpler app (no Playwright)

---

**Ready to try Render?** Follow the steps above! 🚀

It will work much better than Railway for this project.
