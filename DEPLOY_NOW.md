# 🚀 Deploy Newton Autopilot NOW! (10 Minutes)

Follow these steps to get your app live on the internet.

## ⚡ Before You Start

**Get these ready:**
1. ✅ GitHub account
2. ✅ Vercel account → [Sign up FREE](https://vercel.com/signup)
3. ✅ Railway account → [Sign up FREE](https://railway.app/)
4. ✅ Anthropic API key → [Get FREE key](https://console.anthropic.com/)
5. ✅ Your Newton School Gmail & password

---

## 🎯 Step 1: Push to GitHub (2 min)

```bash
cd /Users/vishal/Desktop/newton_automate

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/newton-autopilot.git
git branch -M main
git push -u origin main
```

---

## 🚂 Step 2: Deploy Backend to Railway (4 min)

1. **Go to [railway.app](https://railway.app/) → Login**

2. **Click "New Project" → "Deploy from GitHub"**

3. **Select your `newton-autopilot` repository**

4. **Set Root Directory:**
   - Settings → Service Settings → Root Directory: `backend`

5. **Add Environment Variables:**
   - Click "Variables" tab
   - Add these one by one:

```env
NEWTON_EMAIL=your.email@gmail.com
NEWTON_PASSWORD=your_password
ANTHROPIC_API_KEY=sk-ant-your-key-here
SECRET_KEY=YOUR_RANDOM_SECRET_HERE
API_HOST=0.0.0.0
FRONTEND_URL=https://your-app.vercel.app
DATABASE_URL=sqlite:///./data/newton_autopilot.db
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

6. **Generate Public Domain:**
   - Settings → Networking → Generate Domain
   - **Copy the URL** (e.g., `newton-autopilot-production.up.railway.app`)
   - ✅ **SAVE THIS - YOU NEED IT FOR VERCEL!**

7. **Wait 3-4 minutes for deployment**

8. **Test:** Visit `https://YOUR-RAILWAY-URL.railway.app/health`
   - Should see: `{"status":"healthy","api":"operational"}`

---

## 🔺 Step 3: Deploy Frontend to Vercel (4 min)

1. **Create production env file:**

```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=https://YOUR-RAILWAY-URL.railway.app" > .env.production
```

**⚠️ IMPORTANT: Replace `YOUR-RAILWAY-URL.railway.app` with your actual Railway URL from Step 2!**

2. **Commit and push:**

```bash
git add .
git commit -m "Add production config"
git push
```

3. **Go to [vercel.com](https://vercel.com/) → Login**

4. **Click "Add New Project" → Import your GitHub repo**

5. **Configure:**
   - **Framework:** Next.js ✅ (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` ✅ (auto-detected)
   - Click **Deploy**

6. **Add Environment Variable:**
   - After first deployment, go to **Settings** → **Environment Variables**
   - Add:
     - Name: `NEXT_PUBLIC_API_URL`
     - Value: `https://YOUR-RAILWAY-URL.railway.app`
   - Click **Save**

7. **Redeploy:**
   - Go to **Deployments** → Latest → Click "..." → **Redeploy**

8. **Copy your Vercel URL** (e.g., `newton-autopilot.vercel.app`)

---

## 🔗 Step 4: Connect Frontend & Backend (1 min)

**Update Railway to allow your Vercel domain:**

1. Go back to **Railway** → Your project → **Variables**
2. Update `FRONTEND_URL` to: `https://newton-autopilot.vercel.app` (your Vercel URL)
3. Railway will auto-redeploy (wait 1-2 min)

---

## ✅ Step 5: TEST IT!

1. **Visit your Vercel URL:** `https://your-app.vercel.app`
2. **Login** with your Newton School credentials
3. **Wait 30-60 seconds** for OAuth automation
4. **You should see your dashboard!** 🎉

---

## 🎊 YOU'RE LIVE!

**Your URLs:**
- 🌐 **App:** `https://your-app.vercel.app`
- 📡 **API:** `https://your-railway-url.railway.app/docs`

---

## 🐛 Something Wrong?

### Frontend shows error
```bash
# Check Vercel logs
Vercel Dashboard → Deployments → Latest → Function Logs

# Common fix: Environment variable
Settings → Environment Variables → Verify NEXT_PUBLIC_API_URL
```

### Backend not responding
```bash
# Check Railway logs
Railway Dashboard → Logs tab

# Common fix: Environment variables
Variables tab → Verify all variables are set correctly
```

### Can't login
```bash
# Check Railway logs for authentication errors
# Verify NEWTON_EMAIL and NEWTON_PASSWORD are correct (no extra spaces!)
```

### Still stuck?
Check the detailed guide: `VERCEL_DEPLOYMENT.md`

---

## 💰 Cost

**TOTALLY FREE!**
- Railway: $5/month free credit ✅
- Vercel: Free tier ✅
- Anthropic: Pay-as-you-go (~$0.001 per request)

**Estimated cost:** $0-2/month for moderate use

---

## 🚀 Next Steps

1. ✅ Test all features
2. ✅ Bookmark your app URL
3. ✅ Share with classmates!
4. ✅ Star the GitHub repo ⭐

---

## 🔄 Updating Your App

Make changes and deploy:

```bash
# Make your changes
git add .
git commit -m "Update feature"
git push

# Both Vercel and Railway auto-deploy! 🎉
# Wait 2-3 minutes and refresh
```

---

**Congrats! Your Newton Autopilot is LIVE on the internet! 🌐🎉**

Share your deployment URL and help your classmates! 🚀
