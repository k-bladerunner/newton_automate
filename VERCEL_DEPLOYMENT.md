# Vercel Deployment Guide 🚀

Deploy Newton Autopilot to production using Vercel (frontend) + Railway/Render (backend).

## 📋 Deployment Architecture

```
┌─────────────────────────────────────────────┐
│                                             │
│  Frontend (Next.js)  →  Vercel              │
│                                             │
│  Backend (FastAPI)   →  Railway/Render      │
│                                             │
└─────────────────────────────────────────────┘
```

**Why this architecture?**
- ✅ Vercel is optimized for Next.js (instant deployments, global CDN)
- ✅ Railway/Render support long-running Python processes (needed for FastAPI + Playwright)
- ✅ Both have generous free tiers
- ✅ Easy to set up and maintain

---

## 🎯 Quick Deployment (10 Minutes)

### Prerequisites

- [ ] GitHub account
- [ ] Vercel account ([Sign up free](https://vercel.com/signup))
- [ ] Railway account ([Sign up free](https://railway.app/)) OR Render account ([Sign up free](https://render.com/))
- [ ] Anthropic API key
- [ ] Newton School credentials

---

## Part 1: Deploy Backend to Railway 🚂

Railway offers $5/month free credit (enough for this project).

### Step 1: Push Code to GitHub

```bash
cd /Users/vishal/Desktop/newton_automate

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Newton Autopilot"

# Create GitHub repo and push
# (Create a new repo on github.com first)
git remote add origin https://github.com/YOUR_USERNAME/newton-autopilot.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app/)**
2. **Click "Start a New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Connect your GitHub account** and select your repository
5. **Railway will auto-detect Python** and start deployment

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Click your project → **Variables** tab
2. Add the following environment variables:

```env
NEWTON_EMAIL=your.email@gmail.com
NEWTON_PASSWORD=your_password
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
SECRET_KEY=generate-a-random-secret-key-here
API_HOST=0.0.0.0
FRONTEND_URL=https://your-app.vercel.app
DATABASE_URL=sqlite:///./data/newton_autopilot.db
```

**To generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Configure Build & Start Commands

Railway should auto-detect these, but verify:

- **Build Command:**
  ```bash
  pip install -r requirements.txt && playwright install chromium
  ```

- **Start Command:**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### Step 5: Set Root Directory

1. In Railway Settings → **Service Settings**
2. Set **Root Directory** to: `backend`
3. Click **Save**

### Step 6: Enable Public Domain

1. Go to **Settings** → **Networking**
2. Click **Generate Domain**
3. Copy your Railway URL (e.g., `https://newton-autopilot-production.up.railway.app`)
4. **Save this URL** - you'll need it for Vercel

### Step 7: Verify Backend

Visit: `https://your-railway-url.railway.app/health`

You should see:
```json
{"status": "healthy", "api": "operational"}
```

And check API docs: `https://your-railway-url.railway.app/docs`

---

## Part 2: Deploy Frontend to Vercel 🔺

### Step 1: Prepare Frontend

Update frontend environment variable for production:

```bash
cd frontend

# Create .env.production
echo "NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app" > .env.production
```

**Replace `your-railway-url.railway.app` with your actual Railway URL!**

### Step 2: Commit Changes

```bash
git add .env.production
git commit -m "Add production environment"
git push
```

### Step 3: Deploy to Vercel

1. **Go to [Vercel.com](https://vercel.com/)**
2. **Click "Add New Project"**
3. **Import your GitHub repository**
4. **Configure Project:**
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `.next` (auto-detected)

### Step 4: Add Environment Variable

In Vercel project settings:

1. Go to **Settings** → **Environment Variables**
2. Add:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://your-railway-url.railway.app` (your Railway backend URL)
   - **Environment:** Production, Preview, Development (select all)
3. Click **Save**

### Step 5: Deploy

1. Click **Deploy**
2. Wait 2-3 minutes for build to complete
3. Vercel will provide your URL: `https://your-app.vercel.app`

### Step 6: Update Backend CORS

Go back to Railway → Variables and update:

```env
FRONTEND_URL=https://your-app.vercel.app
```

Railway will auto-redeploy.

---

## ✅ Verification

### Test Your Deployment

1. **Visit your Vercel URL:** `https://your-app.vercel.app`
2. **You should see the login page**
3. **Try logging in** with your Newton School credentials
4. **Check if dashboard loads** with your data

### Check Backend API

Visit: `https://your-railway-url.railway.app/docs`

You should see the FastAPI Swagger documentation.

---

## 🔧 Troubleshooting

### Frontend Issues

**Issue: "API connection failed"**
```bash
# Check environment variable
# In Vercel → Settings → Environment Variables
# Verify NEXT_PUBLIC_API_URL is set correctly

# Redeploy
# In Vercel → Deployments → Click "..." → Redeploy
```

**Issue: Build fails**
```bash
# Check build logs in Vercel
# Common fix: Clear cache and redeploy
# Vercel → Deployments → Click "..." → Redeploy (with cache cleared)
```

### Backend Issues

**Issue: "Application failed to respond"**
```bash
# Check Railway logs
# Railway Dashboard → Your Service → Logs tab

# Verify environment variables are set
# Railway Dashboard → Variables tab

# Check if Playwright installed correctly
# Look for "playwright install chromium" in build logs
```

**Issue: "Module not found"**
```bash
# Railway → Settings → Redeploy
# Or update requirements.txt and push to GitHub
```

**Issue: Authentication failing**
```bash
# Check NEWTON_EMAIL and NEWTON_PASSWORD in Railway variables
# Ensure no extra spaces or quotes
# Verify credentials work locally first
```

---

## 🎨 Custom Domain (Optional)

### For Frontend (Vercel)

1. Go to Vercel → **Settings** → **Domains**
2. Click **Add**
3. Enter your domain: `autopilot.yourdomain.com`
4. Follow DNS configuration instructions
5. Vercel auto-provisions SSL certificate

### For Backend (Railway)

1. Go to Railway → **Settings** → **Networking**
2. Click **Custom Domain**
3. Enter: `api.yourdomain.com`
4. Add CNAME record to your DNS:
   ```
   CNAME api.yourdomain.com → your-app.up.railway.app
   ```

**Update environment variables:**
- Vercel: `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`
- Railway: `FRONTEND_URL=https://autopilot.yourdomain.com`

---

## 💰 Cost Breakdown

### Free Tier Limits

**Railway:**
- $5/month free credit
- ~500 hours/month (enough for this app)
- 1GB RAM, 1 vCPU
- 100GB outbound bandwidth

**Vercel:**
- Unlimited deployments
- 100GB bandwidth/month
- Automatic SSL
- Global CDN

**Anthropic Claude:**
- Pay-as-you-go
- ~$0.001-0.015 per request
- Set usage limits in Anthropic dashboard

**Estimated monthly cost:** $0-5 (depending on usage)

---

## 🔐 Security Best Practices

### 1. Environment Variables
✅ Never commit `.env` files
✅ Use different secrets for production
✅ Rotate API keys regularly

### 2. API Keys
✅ Set spending limits on Anthropic dashboard
✅ Monitor usage regularly
✅ Use separate keys for dev/prod

### 3. Database
✅ Railway provides persistent storage
✅ Set up automatic backups (Railway Pro)
✅ Export database regularly

### 4. CORS
✅ Only allow your Vercel domain
✅ Don't use wildcards (`*`) in production

---

## 📊 Monitoring

### Railway Metrics
- CPU, Memory, Network usage
- Application logs
- Deployment history

### Vercel Analytics
- Page views, unique visitors
- Performance metrics (Web Vitals)
- Geographic distribution

### Set Up Alerts

**Railway:**
1. Go to **Settings** → **Notifications**
2. Enable deployment notifications
3. Add webhook for errors (optional)

**Vercel:**
1. **Settings** → **Notifications**
2. Enable deployment notifications
3. Connect Slack/Discord (optional)

---

## 🔄 Continuous Deployment

Both Vercel and Railway auto-deploy on git push:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Vercel: Auto-deploys frontend (2-3 min)
# Railway: Auto-deploys backend (3-5 min)
```

**View deployment status:**
- Vercel: Dashboard → Deployments
- Railway: Dashboard → Deployments

---

## 🚀 Alternative: Deploy Backend to Render

If you prefer Render over Railway:

### Render Deployment Steps

1. **Go to [Render.com](https://render.com/)**
2. **Click "New +" → "Web Service"**
3. **Connect GitHub repository**
4. **Configure:**
   - **Name:** newton-autopilot-backend
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && playwright install chromium && playwright install-deps`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

5. **Add Environment Variables** (same as Railway)

6. **Deploy**

**Note:** Render free tier has some limitations:
- Spins down after 15 min of inactivity
- Cold start takes 30-60 seconds
- 750 hours/month free

---

## 📝 Post-Deployment Checklist

- [ ] Backend health check working
- [ ] Frontend loads correctly
- [ ] Login with Google OAuth works
- [ ] Dashboard displays data
- [ ] Assignments page loads
- [ ] AI solver functions
- [ ] Schedule displays correctly
- [ ] All API endpoints working
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Custom domain configured (optional)
- [ ] SSL certificates active
- [ ] Monitoring set up

---

## 🆘 Getting Help

### Check Logs

**Railway:**
```
Dashboard → Service → Logs tab
```

**Vercel:**
```
Dashboard → Deployment → Function Logs
```

### Common Issues

1. **CORS errors** → Update FRONTEND_URL in Railway
2. **API not responding** → Check Railway logs, verify environment variables
3. **Build fails** → Clear cache, check dependencies
4. **Authentication fails** → Verify credentials, check Playwright installation
5. **Slow response** → Railway/Render free tier cold starts

### Support Resources

- Railway Docs: https://docs.railway.app/
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs

---

## 🎉 Success!

Your Newton Autopilot is now live on the internet! 🌐

**Share your deployment:**
- Frontend: `https://your-app.vercel.app`
- API Docs: `https://your-railway-url.railway.app/docs`

---

**Pro Tip:** Bookmark both dashboards for easy access to logs and metrics!

**Next Steps:**
1. Test all features thoroughly
2. Monitor usage and costs
3. Set up error tracking (Sentry)
4. Add analytics (if needed)
5. Share with friends!

---

Made with ❤️ for Newton School students
