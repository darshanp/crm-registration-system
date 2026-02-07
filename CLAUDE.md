# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Vision

Building a **full-fledged CRM system** with e-commerce capabilities, starting with a simple user registration feature and evolving into a complete platform with:
- User registration and authentication
- Product catalog and shopping cart
- Order management with e-signatures
- Payment processing (Stripe)
- Email and SMS notifications
- Admin panel for employees
- Mobile-responsive web app
- Future: iOS and Android native apps

## Current Phase: Phase 1a - User Registration with Email Verification

### What's Built
- Basic project structure
- User registration form with profile picture upload
- Email verification workflow
- PostgreSQL database setup
- Local development environment with Docker

### What's Next
- Phase 1b: OTP phone verification
- Phase 2: User authentication (login/logout)
- Phase 3: Product catalog and orders
- Phase 4: CRM features

## Architecture

### Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL (via Docker locally, Railway in production)
- SQLAlchemy ORM
- Pydantic for validation

**Frontend:**
- Vanilla HTML/CSS/JavaScript (mobile-first, responsive)
- Future: React or Vue for better state management

**Infrastructure:**
- Local: Docker Compose (PostgreSQL)
- Production: Railway.app or Render.com
- File Storage: AWS S3 or Cloudflare R2
- Email: SendGrid (free tier: 100 emails/day)
- SMS: Twilio (for OTP verification)
- Payments: Stripe

**External Services:**
- didit.me (identity verification - stubbed initially)
- SendGrid/Resend (transactional emails)
- Twilio (SMS/OTP)
- Stripe (payment processing)
- AWS S3 (file storage)

### High-Level Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (HTML/CSS/JS)                 │
│  - Registration form                    │
│  - Email verification                   │
│  - Product catalog (future)             │
│  - Checkout with e-signature (future)   │
└──────────────┬──────────────────────────┘
               │ REST API (JSON)
┌──────────────▼──────────────────────────┐
│  FastAPI Backend                        │
│  - API routes (/api/*)                  │
│  - Business logic (services/)           │
│  - Database models (SQLAlchemy)         │
│  - External service integrations        │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼──┐  ┌────▼─────┐
│  DB   │  │ S3  │  │ External │
│ (PG)  │  │     │  │ Services │
└───────┘  └─────┘  └──────────┘
```

## Project Structure

```
Try-ClaudeCode/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + routes
│   │   ├── config.py            # Environment config
│   │   ├── database.py          # SQLAlchemy setup
│   │   │
│   │   ├── models/              # Database models (ORM)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py       # Phase 3
│   │   │   └── order.py         # Phase 3
│   │   │
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   │
│   │   ├── api/                 # API routes
│   │   │   ├── __init__.py
│   │   │   ├── users.py         # Registration + verification
│   │   │   ├── auth.py          # Phase 2
│   │   │   ├── products.py      # Phase 3
│   │   │   └── payments.py      # Phase 3
│   │   │
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── email.py         # SendGrid integration
│   │   │   ├── sms.py           # Twilio (Phase 1b)
│   │   │   ├── storage.py       # S3 upload/download
│   │   │   ├── pdf_generator.py # Phase 3
│   │   │   ├── stripe.py        # Phase 3
│   │   │   └── didit.py         # Identity verification (stubbed)
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       └── tokens.py        # JWT, verification tokens
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                     # Gitignored
│
├── frontend/
│   ├── index.html               # Registration page
│   ├── verify-email.html        # Email verification
│   ├── products.html            # Phase 3
│   ├── checkout.html            # Phase 3
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── api.js
│       ├── signature.js         # Phase 3: E-signature
│       └── upload.js            # Image upload
│
├── docker-compose.yml           # PostgreSQL + pgAdmin
├── Makefile                     # Common commands
├── .gitignore
├── README.md
└── CLAUDE.md                    # This file
```

## Database Schema

### Phase 1: Users + Email Verification

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    date_of_birth DATE NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    phone_verified BOOLEAN DEFAULT FALSE,

    profile_picture_url VARCHAR(500),

    verification_id VARCHAR(255),  -- didit.me
    verified BOOLEAN DEFAULT FALSE,

    password_hash VARCHAR(255),  -- Phase 2

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_phone (country_code, phone_number)
);

-- Email verification tokens
CREATE TABLE email_verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Phase 2: OTP Verification

```sql
CREATE TABLE otp_codes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    phone_number VARCHAR(20) NOT NULL,
    code VARCHAR(6) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Phase 3: Products, Orders, Payments

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,  -- pending, paid, cancelled

    terms_accepted BOOLEAN DEFAULT FALSE,
    signature_image_url VARCHAR(500),
    signed_at TIMESTAMP,

    transaction_pdf_url VARCHAR(500),

    stripe_payment_id VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

## API Endpoints

### Phase 1a: Registration + Email Verification

```
POST   /api/register
  Body (multipart/form-data):
    - name: string
    - email: string (email format)
    - date_of_birth: string (YYYY-MM-DD)
    - country_code: string (e.g., "+1")
    - phone_number: string (digits only)
    - profile_picture: file (optional, JPEG/PNG, max 5MB)

  Response (201):
    {
      "success": true,
      "user_id": 1,
      "message": "Registration successful. Please check your email."
    }

  Errors:
    - 400: Duplicate email, invalid input
    - 422: Validation error

GET    /api/verify-email?token={token}
  Response (200):
    {
      "success": true,
      "message": "Email verified successfully"
    }

GET    /api/country-codes
  Response (200):
    {
      "success": true,
      "data": [
        {"code": "+1", "country": "United States/Canada"},
        {"code": "+44", "country": "United Kingdom"},
        ...
      ]
    }

GET    /api/health
  Response (200): {"status": "healthy"}
```

### Phase 2: Authentication (Future)

```
POST   /api/login
POST   /api/logout
POST   /api/refresh-token
POST   /api/send-otp
POST   /api/verify-otp
```

### Phase 3: Products & Orders (Future)

```
GET    /api/products
GET    /api/products/:id
POST   /api/orders
GET    /api/orders/:id
POST   /api/payments/create-intent
POST   /api/payments/stripe-webhook
```

## Development Commands

### Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Start PostgreSQL
docker-compose up -d

# Run database migrations (create tables)
python -m app.database init

# Start FastAPI dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Or use Makefile

```bash
make setup     # Install deps + start Docker
make run       # Start backend server
make db-shell  # Open PostgreSQL shell
make logs      # View logs
make clean     # Stop all services
```

### Testing Locally

```bash
# Open browser
http://localhost:8000/

# API health check
curl http://localhost:8000/api/health

# Test registration
curl -X POST http://localhost:8000/api/register \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "date_of_birth=1990-01-01" \
  -F "country_code=+1" \
  -F "phone_number=5551234567" \
  -F "profile_picture=@/path/to/image.jpg"
```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/crm_db

# AWS S3 (for profile pictures, PDFs)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1

# Email Service (SendGrid)
SENDGRID_API_KEY=your_sendgrid_key
FROM_EMAIL=noreply@yourdomain.com

# SMS Service (Twilio - Phase 1b)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# Stripe (Phase 3)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# didit.me (when ready)
DIDIT_API_KEY=your_didit_key

# App Config
SECRET_KEY=your-secret-key-for-jwt
FRONTEND_URL=http://localhost:8000
VERIFICATION_TOKEN_EXPIRE_HOURS=24
```

## Deployment (Production)

### Railway.app (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create new project
railway init

# Add PostgreSQL
railway add postgresql

# Set environment variables
railway variables set AWS_ACCESS_KEY_ID=xxx
railway variables set SENDGRID_API_KEY=xxx
# ... (set all vars from .env)

# Deploy
railway up
```

### Cost Estimate

- Railway Hobby Plan: $5/month (includes PostgreSQL)
- AWS S3: ~$1-3/month
- SendGrid: Free tier (100 emails/day)
- Twilio: Pay-as-you-go (~$0.01/SMS)
- Stripe: 2.9% + $0.30 per transaction

**Total MVP: $5-10/month**

## Phase Roadmap

### ✅ Phase 1a: User Registration (Current)
- [x] Project setup
- [x] Database schema
- [ ] Registration form with profile picture upload
- [ ] Email verification
- [ ] S3 integration for images
- [ ] Local testing

### Phase 1b: OTP Phone Verification
- [ ] Send OTP via Twilio
- [ ] Verify OTP endpoint
- [ ] Phone verification UI

### Phase 2: Authentication
- [ ] Password hashing (bcrypt)
- [ ] Login endpoint
- [ ] JWT token generation
- [ ] Protected routes middleware
- [ ] Logout functionality

### Phase 3: Products & Orders
- [ ] Product catalog
- [ ] Shopping cart (frontend state)
- [ ] Checkout flow
- [ ] E-signature integration (SignaturePad.js)
- [ ] Terms & conditions modal
- [ ] Stripe payment integration
- [ ] Transaction PDF generation
- [ ] Email transaction PDF to user

### Phase 4: CRM Features
- [ ] Admin panel
- [ ] Employee management
- [ ] Order tracking dashboard
- [ ] Analytics
- [ ] Reports

### Phase 5: Mobile Apps
- [ ] API ready for mobile consumption
- [ ] React Native or Flutter app
- [ ] Push notifications

## Key Design Decisions

1. **PostgreSQL over SQLite**: Better for production CRM with concurrent users, transactions, and complex queries
2. **FastAPI over Flask**: Modern, fast, automatic API docs, async support
3. **S3 for file storage**: Scalable, cheap, reliable (vs storing in database)
4. **SendGrid for email**: Free tier sufficient for MVP, easy integration
5. **Stripe for payments**: Best API, reliable, standard for e-commerce
6. **JWT for sessions**: Stateless, works for web + mobile apps
7. **Modular structure**: Easy to add features incrementally

## Security Considerations

- ✅ Password hashing with bcrypt (Phase 2)
- ✅ Email verification to prevent fake signups
- ✅ OTP phone verification (Phase 1b)
- ✅ HTTPS only in production
- ✅ CORS properly configured
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Rate limiting on API endpoints (add middleware)
- ✅ Stripe webhook signature verification
- ✅ S3 signed URLs for private files

## Common Issues & Solutions

### Database connection fails
```bash
# Check if PostgreSQL is running
docker ps

# Restart PostgreSQL
docker-compose restart db
```

### Email not sending
- Check SendGrid API key is valid
- Verify sender email is authenticated in SendGrid
- Check spam folder

### S3 upload fails
- Verify AWS credentials are correct
- Check bucket permissions (public-read for profile pictures)
- Ensure bucket exists and region matches

### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

## Testing Strategy

- Unit tests: pytest for backend logic
- Integration tests: Test API endpoints with TestClient
- E2E tests: Playwright or Selenium (Phase 3+)
- Manual testing: Use Postman or curl for API testing

## Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, Facebook OAuth)
- [ ] Multi-language support (i18n)
- [ ] Dark mode
- [ ] Progressive Web App (PWA)
- [ ] Real-time notifications (WebSockets)
- [ ] Advanced analytics dashboard
- [ ] Export data (CSV, PDF reports)
- [ ] API rate limiting
- [ ] Redis caching for performance
- [ ] CDN for static assets (Cloudflare)

## Contact & Support

- GitHub: [Your repo URL]
- Email: [Your email]
- Documentation: [Your docs URL]

---

**Last Updated**: 2026-02-07
**Current Version**: 0.1.0 (Phase 1a in progress)
