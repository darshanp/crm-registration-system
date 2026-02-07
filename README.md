# CRM Application - User Registration System

A full-featured CRM application starting with user registration, progressing to e-commerce, payments, and more.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker Desktop (for PostgreSQL)
- Make (optional, but recommended)

### Setup & Run

```bash
# 1. Clone/navigate to the project
cd Try-ClaudeCode

# 2. Setup everything (install deps + start database)
make setup

# 3. Run the backend server
make run

# 4. Open your browser
# http://localhost:8000/
```

That's it! The application is now running.

---

## 📁 Project Structure

```
Try-ClaudeCode/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── requirements.txt
│   └── .env             # Environment variables
├── frontend/            # HTML/CSS/JS frontend
│   ├── css/
│   ├── js/
│   └── index.html
├── docker-compose.yml   # PostgreSQL setup
├── Makefile            # Common commands
├── CLAUDE.md           # Context for Claude Code
└── README.md           # This file
```

---

## 🛠 Development Commands

### Using Makefile (Recommended)

```bash
make setup      # Install dependencies + start database
make run        # Start backend server
make db-start   # Start PostgreSQL only
make db-stop    # Stop PostgreSQL
make db-shell   # Open PostgreSQL shell
make pgadmin    # Start pgAdmin (database GUI)
make clean      # Clean up everything
make logs       # View database logs
```

### Manual Commands

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start PostgreSQL
docker-compose up -d db

# Initialize database tables
cd backend
python -m app.database

# Start FastAPI server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 Endpoints

### Frontend
- **http://localhost:8000/** - Registration page
- **http://localhost:8000/verify-email?token=xxx** - Email verification page

### API
- **http://localhost:8000/docs** - Interactive API documentation (Swagger)
- **http://localhost:8000/redoc** - Alternative API docs (ReDoc)

### API Routes
- `POST /api/register` - Register new user
- `GET /api/verify-email?token=xxx` - Verify email
- `GET /api/country-codes` - Get country codes for dropdown
- `GET /api/health` - Health check

---

## 📧 Email Verification (Local Dev)

Since SendGrid is not configured by default, verification emails are printed to the console where the backend is running.

**To enable real emails:**
1. Sign up for SendGrid (free tier: 100 emails/day)
2. Get API key from SendGrid dashboard
3. Update `.env`:
   ```bash
   SENDGRID_API_KEY=your_actual_key_here
   FROM_EMAIL=noreply@yourdomain.com
   ```

---

## 🗄 Database Access

### Using pgAdmin (GUI)

```bash
make pgadmin
```

Then open: **http://localhost:5050**
- Email: `admin@crm.local`
- Password: `admin`

Add server connection:
- Host: `db` (or `localhost` from host machine)
- Port: `5432`
- Database: `crm_db`
- Username: `crmuser`
- Password: `crmpassword`

### Using Command Line

```bash
# Open PostgreSQL shell
make db-shell

# Then run SQL commands
crm_db=# SELECT * FROM users;
crm_db=# \dt    # List tables
crm_db=# \q     # Quit
```

---

## 📤 Profile Picture Upload

### Local Development (without AWS S3)
- Profile pictures are optional
- If uploaded without S3 configured, a warning is shown but registration succeeds
- `profile_picture_url` will be `NULL` in database

### Production Setup (with AWS S3)
1. Create S3 bucket
2. Create IAM user with S3 permissions
3. Update `.env`:
   ```bash
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_S3_BUCKET=your-bucket-name
   AWS_REGION=us-east-1
   ```

---

## 🧪 Testing the Application

### Test Registration Flow

1. Open http://localhost:8000/
2. Fill out the form:
   - Name: John Doe
   - Email: john@example.com
   - Date of Birth: 1990-01-01
   - Country Code: +1
   - Phone: 5551234567
   - Upload a profile picture (optional)
3. Submit the form
4. Check the backend console for the verification email
5. Copy the verification link and open it in your browser

### Test API with curl

```bash
# Register a user
curl -X POST http://localhost:8000/api/register \
  -F "name=Jane Doe" \
  -F "email=jane@example.com" \
  -F "date_of_birth=1995-05-15" \
  -F "country_code=+1" \
  -F "phone_number=5559876543" \
  -F "profile_picture=@/path/to/image.jpg"

# Get country codes
curl http://localhost:8000/api/country-codes

# Health check
curl http://localhost:8000/api/health
```

---

## 🎯 Phase Roadmap

### ✅ Phase 1a (Current)
- [x] User registration form
- [x] Profile picture upload
- [x] Email verification
- [x] PostgreSQL database
- [x] Local development setup

### 🔄 Phase 1b (Next)
- [ ] OTP phone verification (Twilio)

### 📅 Phase 2
- [ ] User authentication (login/logout)
- [ ] Password management
- [ ] JWT sessions

### 📅 Phase 3
- [ ] Product catalog
- [ ] Shopping cart
- [ ] E-signature for orders
- [ ] Stripe payment integration
- [ ] Transaction PDFs

### 📅 Phase 4
- [ ] Admin panel
- [ ] Employee management
- [ ] CRM features

---

## 🐛 Troubleshooting

### Database connection fails
```bash
# Check if PostgreSQL is running
docker ps

# Restart database
make db-stop
make db-start
```

### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### "Module not found" errors
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Database tables not created
```bash
# Manually initialize database
cd backend
python -m app.database
```

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **SendGrid API**: https://docs.sendgrid.com/
- **AWS S3 Documentation**: https://docs.aws.amazon.com/s3/

---

## 📝 Environment Variables

See `backend/.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SENDGRID_API_KEY` - For sending emails
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` - For S3 uploads
- `SECRET_KEY` - For JWT tokens (Phase 2)

---

## 🤝 Contributing

This is a learning project. Feel free to experiment and extend!

---

## 📄 License

MIT License - Feel free to use this for learning and personal projects.

---

**Built with ❤️ using FastAPI, PostgreSQL, and vanilla JavaScript**
