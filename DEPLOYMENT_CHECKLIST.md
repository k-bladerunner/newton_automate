# 🚀 Deployment Checklist

Use this checklist to ensure successful deployment to Vercel + Railway.

## 📋 Pre-Deployment

- [ ] Code is working locally
- [ ] All tests pass (if you have tests)
- [ ] Environment variables documented
- [ ] GitHub repository created
- [ ] Code pushed to GitHub

## 🔑 Accounts Setup

- [ ] GitHub account ready
- [ ] Vercel account created ([vercel.com](https://vercel.com))
- [ ] Railway account created ([railway.app](https://railway.app))
- [ ] Anthropic API key obtained ([console.anthropic.com](https://console.anthropic.com))
- [ ] Newton School credentials verified

## 🚂 Backend Deployment (Railway)

- [ ] Railway project created
- [ ] GitHub repository connected
- [ ] Root directory set to `backend`
- [ ] Environment variables added:
  - [ ] `NEWTON_EMAIL`
  - [ ] `NEWTON_PASSWORD`
  - [ ] `ANTHROPIC_API_KEY`
  - [ ] `SECRET_KEY` (generated)
  - [ ] `API_HOST=0.0.0.0`
  - [ ] `FRONTEND_URL` (will update after Vercel)
  - [ ] `DATABASE_URL`
- [ ] Build command verified
- [ ] Start command verified
- [ ] Public domain generated
- [ ] Railway URL saved for later
- [ ] Health endpoint tested (`/health`)
- [ ] API docs accessible (`/docs`)

## 🔺 Frontend Deployment (Vercel)

- [ ] Production env file created (`.env.production`)
- [ ] Railway URL added to `.env.production`
- [ ] Changes committed and pushed to GitHub
- [ ] Vercel project created
- [ ] GitHub repository connected
- [ ] Root directory set to `frontend`
- [ ] Framework preset: Next.js
- [ ] Environment variable added:
  - [ ] `NEXT_PUBLIC_API_URL` (Railway URL)
- [ ] First deployment successful
- [ ] Vercel URL saved
- [ ] Redeployed after adding env variable

## 🔗 Connection & Configuration

- [ ] Vercel URL added to Railway `FRONTEND_URL`
- [ ] Railway redeployed
- [ ] CORS working (no errors in browser console)
- [ ] API calls working from frontend

## ✅ Testing

- [ ] Frontend loads at Vercel URL
- [ ] Login page displays correctly
- [ ] Google OAuth authentication works
- [ ] Dashboard loads with user data
- [ ] Assignments page displays
- [ ] Schedule page loads
- [ ] Performance page shows stats
- [ ] AI solver works (test in learning mode)
- [ ] No console errors
- [ ] Mobile responsive works

## 📊 Monitoring Setup

- [ ] Railway notifications enabled
- [ ] Vercel deployment notifications enabled
- [ ] Error tracking configured (optional)
- [ ] Usage monitoring set up
- [ ] Spending limits set on Anthropic

## 🔐 Security

- [ ] Environment variables set (not committed to git)
- [ ] Strong SECRET_KEY generated
- [ ] CORS properly configured
- [ ] API keys secured
- [ ] Spending limits set
- [ ] No sensitive data in logs

## 📝 Documentation

- [ ] README updated with production URLs
- [ ] Team members notified
- [ ] Usage instructions shared
- [ ] Support process defined

## 🎉 Post-Deployment

- [ ] All features tested in production
- [ ] Performance verified
- [ ] Logs checked for errors
- [ ] Backup strategy planned
- [ ] Update schedule defined

## 🔄 Continuous Deployment

- [ ] Git push auto-deploys verified
- [ ] Deployment time noted
- [ ] Rollback procedure understood
- [ ] Branch strategy defined (main/develop)

## 💰 Cost Management

- [ ] Railway free credits tracked
- [ ] Vercel usage monitored
- [ ] Anthropic usage monitored
- [ ] Alerts set for usage thresholds
- [ ] Billing information verified

---

## 🆘 Emergency Contacts

**Railway Issues:**
- Dashboard: https://railway.app/dashboard
- Docs: https://docs.railway.app/
- Status: https://status.railway.app/

**Vercel Issues:**
- Dashboard: https://vercel.com/dashboard
- Docs: https://vercel.com/docs
- Status: https://vercel-status.com/

**Anthropic Issues:**
- Console: https://console.anthropic.com/
- Docs: https://docs.anthropic.com/
- Support: https://support.anthropic.com/

---

## 📞 Quick Links

- **Live App:** `https://your-app.vercel.app`
- **API Docs:** `https://your-railway-url.railway.app/docs`
- **Railway Dashboard:** https://railway.app/dashboard
- **Vercel Dashboard:** https://vercel.com/dashboard
- **GitHub Repo:** `https://github.com/YOUR_USERNAME/newton-autopilot`

---

**🎯 Deployment Status:**

- [ ] ✅ Successfully deployed
- [ ] ✅ All tests passing
- [ ] ✅ Team notified
- [ ] ✅ Documentation updated

**Deployment Date:** ___________

**Deployed By:** ___________

**Production URLs:**
- Frontend: ___________
- Backend: ___________

---

**Ready to deploy? Follow [DEPLOY_NOW.md](DEPLOY_NOW.md)!** 🚀
