# 🚀 Quick Start Guide

## ✅ What's Ready

Your CRM application is fully built and ready to run! Here's what we created:

- ✅ **Backend**: FastAPI with PostgreSQL
- ✅ **Frontend**: Beautiful, mobile-responsive registration form
- ✅ **Database**: User model with email verification
- ✅ **Services**: Email, S3 storage, didit.me (stubbed)
- ✅ **API**: Registration, email verification, country codes

## 📋 Prerequisites to Install

You need to install Docker Desktop to run the PostgreSQL database.

### Install Docker Desktop

1. **Download Docker Desktop**:
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download for macOS (M1/M2/Intel compatible)
   - Install and launch Docker Desktop

2. **Verify Docker is running**:
   ```bash
   docker --version
   ```

## 🎯 Start the Application (3 Steps)

Once Docker is installed:

### Step 1: Start the Database
```bash
cd ~/Store/Try-ClaudeCode
docker compose up -d db
```

Wait ~5 seconds for PostgreSQL to start.

### Step 2: Install Python Dependencies
```bash
cd backend
pip3 install -r requirements.txt
```

### Step 3: Run the Application
```bash
cd backend
python3 -m app.database  # Create database tables
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Open Your Browser

- **Frontend**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs

## 🧪 Test It

1. Fill out the registration form
2. Upload a profile picture (optional)
3. Submit the form
4. Check the terminal where uvicorn is running for the verification email
5. Copy the verification link and open it in your browser

## 📧 Email Verification (Local Dev)

Since SendGrid is not configured, verification emails are **printed to the console** where the backend is running. Look for a message like:

```
============================================================
📧 EMAIL VERIFICATION (SendGrid not configured)
============================================================
To: your@email.com
...
http://localhost:8000/verify-email?token=abc123...
============================================================
```

Copy that link and open it to verify the email!

## 🎨 Features

- ✅ User registration with validation
- ✅ Profile picture upload (S3 ready, works without AWS for dev)
- ✅ Email verification flow
- ✅ Date of birth validation (18+ years)
- ✅ International phone numbers with country codes
- ✅ Mobile-responsive design
- ✅ Beautiful, modern UI

## 🗄 View Database

### Option 1: pgAdmin (GUI)
```bash
docker compose up -d pgadmin
```
Open http://localhost:5050 (Email: admin@crm.local, Password: admin)

### Option 2: Command Line
```bash
docker exec -it crm_postgres psql -U crmuser -d crm_db
# Then: SELECT * FROM users;
```

## 🛑 Stop Everything

```bash
docker compose down
```

## 📝 Next Steps

Once Phase 1a is working:
- **Phase 1b**: Add OTP phone verification (Twilio)
- **Phase 2**: User authentication (login/logout)
- **Phase 3**: Products, orders, payments (Stripe)
- **Phase 4**: Admin panel, CRM features

See `CLAUDE.md` for the full roadmap!

---

**Need help?** Check `README.md` for detailed documentation.
