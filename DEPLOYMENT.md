# 🚀 Deployment Guide - Render (Free Tier)

## Prerequisites
- GitHub account
- GitHub repository with code pushed
- Render account (free): https://render.com

---

## 📋 Step-by-Step Deployment

### **Step 1: Sign Up for Render**

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repositories

---

### **Step 2: Create New Web Service**

1. Click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository: `crm-registration-system`
4. Click "Connect"

---

### **Step 3: Configure Web Service**

**Basic Settings:**
- **Name**: `crm-backend` (or your choice)
- **Region**: `Oregon (US West)` (or closest to you)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select: **Free** (512 MB RAM, 0.1 CPU)

---

### **Step 4: Add PostgreSQL Database**

1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. **Name**: `crm-db`
4. **Database**: `crm_db`
5. **User**: `crmuser`
6. **Region**: Same as web service
7. **Plan**: **Free** (1 GB, 90 days free)
8. Click "Create Database"

**Copy the Internal Database URL** (you'll need it in Step 5)

---

### **Step 5: Configure Environment Variables**

Back in your web service settings, go to "Environment" tab and add:

#### **Required Variables:**

```
DATABASE_URL
# Paste the Internal Database URL from Step 4
# Format: postgresql://user:password@host:5432/crm_db

ENVIRONMENT=production

FRONTEND_URL
# Will be: https://crm-backend.onrender.com (your actual URL)

SECRET_KEY
# Generate a random string (or let Render auto-generate)

VERIFICATION_TOKEN_EXPIRE_HOURS=24
```

#### **Optional (Add When Ready):**

```
# Email (SendGrid)
SENDGRID_API_KEY=your_sendgrid_key_here
FROM_EMAIL=noreply@yourdomain.com

# AWS S3 (for profile pictures)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1
```

---

### **Step 6: Deploy!**

1. Click "Create Web Service"
2. Render will start building and deploying
3. Wait 5-10 minutes for first deploy
4. Watch the logs in real-time

**You'll see:**
```
Building...
Installing dependencies...
Starting server...
🚀 Starting CRM Application in production mode
✅ Database initialized successfully
```

---

### **Step 7: Get Your URL**

Once deployed, you'll get a URL like:
```
https://crm-backend.onrender.com
```

**Update FRONTEND_URL:**
1. Go to Environment variables
2. Update `FRONTEND_URL` to your actual Render URL
3. Save (will trigger redeploy)

---

### **Step 8: Test Your Deployment**

Open your browser:

1. **Homepage**: https://crm-backend.onrender.com/
2. **API Docs**: https://crm-backend.onrender.com/docs
3. **Health Check**: https://crm-backend.onrender.com/api/health

**Test Registration:**
- Fill out the form
- Check Render logs for verification email
- Copy verification link and test

---

## 🛌 **Preventing Sleep (Optional)**

### **Option 1: UptimeRobot (Recommended)**

1. Sign up: https://uptimerobot.com (free)
2. Add New Monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://crm-backend.onrender.com/api/health`
   - **Interval**: 5 minutes
3. Save!

Your app will never sleep! ✅

### **Option 2: Cron-Job.org**

1. Sign up: https://cron-job.org (free)
2. Create Cronjob:
   - **URL**: `https://crm-backend.onrender.com/api/health`
   - **Schedule**: Every 10 minutes
3. Enable!

---

## 🔧 **Troubleshooting**

### **Build Failed**

Check logs for errors:
- Python version mismatch?
- Missing dependencies?
- Build script not executable?

**Fix:**
```bash
# Make sure build.sh is executable
chmod +x build.sh
git add build.sh
git commit -m "Fix build script permissions"
git push
```

### **Database Connection Error**

- Check `DATABASE_URL` is correctly set
- Make sure database is in same region
- Use **Internal Database URL**, not External

### **App Not Starting**

- Check start command is correct
- Check PORT environment variable (Render sets this automatically)
- View logs for Python errors

### **502 Bad Gateway**

- App is still starting (wait a minute)
- App crashed (check logs)
- Health check failed

---

## 📊 **Monitoring**

### **View Logs:**
1. Go to your service in Render
2. Click "Logs" tab
3. See real-time logs

### **Check Metrics:**
1. Go to "Metrics" tab
2. See CPU, Memory, Request stats

### **Database:**
1. Go to PostgreSQL database
2. Click "Connect"
3. Use provided credentials to connect via psql or pgAdmin

---

## 💰 **Costs**

### **Free Tier (First 90 Days):**
- Web Service: **Free** (with sleep)
- PostgreSQL: **Free** (1 GB)
- **Total: $0/month**

### **After 90 Days:**
- Web Service: **Free** (still!)
- PostgreSQL: **$7/month**
- **Total: $7/month**

### **When You Need More:**
- Upgrade to Starter: $7/month (no sleep)
- PostgreSQL: $7/month
- **Total: $14/month**

---

## 🚀 **Next Steps**

Once deployed:

1. ✅ Set up UptimeRobot (keep awake)
2. ✅ Test all features
3. ✅ Add custom domain (optional)
4. ✅ Configure SendGrid for real emails
5. ✅ Add AWS S3 for profile pictures
6. ✅ Continue building Phase 1b/2!

---

## 🔗 **Useful Links**

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Support**: https://community.render.com

---

## 📝 **Notes**

- First deploy takes 5-10 minutes
- Subsequent deploys: 3-5 minutes
- Auto-deploys on git push to main
- Free tier sleeps after 15 min inactivity
- Cold start: 30-60 seconds

---

**Need help? Come back to Claude Code and ask!** 💙
