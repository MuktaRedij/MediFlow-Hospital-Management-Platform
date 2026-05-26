# 🏥 MediFlow – Hospital Management Platform 

MediFlow is a full-stack Hospital Management Platform built with Django that streamlines appointment booking, doctor availability, patient management, email notifications, and calendar integrations.

---

## 🚀 Features

### 👤 Authentication & Roles
- Custom user model with **Doctor** and **Patient** roles
- Secure login, signup, and logout
- Role-based dashboard redirection

### 🩺 Doctor Dashboard
- Create and manage availability slots
- View booked appointments
- Google Calendar integration
- Appointment statistics

### 🧑‍⚕️ Patient Dashboard
- Browse doctors
- Book and cancel appointments
- View upcoming appointments
- Google Calendar integration

### 📅 Appointment Management
- Slot-based booking system
- Transaction-safe booking (prevents double booking)
- Cancellation support

### ✉️ Email Notifications
- Signup welcome email
- Booking confirmation (patient & doctor)
- Cancellation email
- Appointment reminder (1 hour before)
- Powered by a **Serverless email microservice**

### 🔗 Integrations
- Google Calendar (OAuth 2.0)
- Serverless email service (AWS Lambda style)

---

## 🛠️ Tech Stack

**Backend**
- Django
- Python
- SQLite (dev) / PostgreSQL (production-ready)

**Frontend**
- HTML
- CSS
- JavaScript
- Django Templates

**Services**
- Google Calendar API
- Serverless Framework
- REST-based Email Service

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/MuktaRedij/MediFlow-Hospital-Management-Platform.git
cd MediFlow-Hospital-Management-Platform/hms
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Environment Variables
Create a .env file based on .env.example and add:

- Google OAuth credentials
- Email service URL
### 5️⃣ Run Migrations
```bash
python manage.py migrate
```
### 6️⃣ Start Server
```bash
python manage.py runserver
```
---
### Demo Email Reminders

Run manually:
```bash
python manage.py send_reminders
```
---
🔐 Security Notes

Secrets are never committed

.env, tokens, and credentials are git-ignored

Google OAuth handled securely
---
👩‍💻 Author

Mukta Redij
=======
# MediFlow Healthcare Platform

A full-stack hospital management system with enterprise-grade DevOps infrastructure, comprehensive test automation, and infrastructure-as-code provisioning.

---

## Project Overview

MediFlow is a Django-based healthcare platform designed to streamline hospital workflows through digital appointment management, role-based access control, and real-time notifications. Built with production-ready DevOps practices, the platform includes automated CI/CD pipelines, infrastructure automation via Ansible and Puppet, and comprehensive Selenium test coverage.

**Core Purpose**: Enable doctors and patients to manage appointments efficiently while maintaining security, data consistency, and multi-environment deployment capabilities.

**Key Achievement**: Demonstrates full-stack engineering competency across backend development, infrastructure automation, and quality assurance.

---

## Key Features

- **Role-Based Dashboards**: Separate interfaces for doctors (availability management) and patients (appointment booking)
- **Appointment Scheduling**: Concurrent-safe booking system preventing double-bookings via database transactions
- **Real-Time Notifications**: Email alerts on booking confirmation, reminder notifications via serverless functions
- **Google Calendar Integration**: OAuth2-based calendar synchronization for appointment visibility
- **Authentication & Security**: Session-based auth, password hashing, CSRF protection, role-based access control
- **Multi-Environment Support**: Seamless deployment across development, staging, and production environments
- **Automated Testing**: 41 Selenium tests covering UI workflows and database integrity
- **Infrastructure Automation**: Ansible playbooks and Puppet manifests for reproducible infrastructure

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│                   Django Templates (HTML/CSS)                │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      Django Backend                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Accounts │ Doctors │ Patients │ Bookings │ Services │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
         ┌──────────▼───────┐   ┌─────▼──────────┐
         │   PostgreSQL     │   │ External APIs  │
         │   Database       │   │ (Google Cal)   │
         └──────────────────┘   └─────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DevOps Layer                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Jenkins (CI/CD) → Ansible (Infrastructure) → Puppet    │ │
│  │                  → Selenium (Testing)                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
- **Python 3.10+**: Core language
- **Django 4+**: Web framework with ORM
- **Django ORM**: Database abstraction and query builder
- **Gunicorn**: WSGI application server
- **Nginx**: Reverse proxy and load balancer

### Frontend
- **HTML5/CSS3**: Markup and styling
- **Django Templates**: Server-side rendering
- **JavaScript**: Client-side interactivity

### Database
- **PostgreSQL 14+**: Production database
- **SQLite**: Development database
- **Database Transactions**: Atomic booking operations

### DevOps & Automation
- **Jenkins 2.387+**: CI/CD pipeline orchestration (12 stages)
- **Ansible 2.10+**: Infrastructure provisioning and configuration
- **Puppet 7+**: Infrastructure-as-code declarations
- **Jinja2 Templates**: Environment-specific configuration management
- **Serverless Framework**: Email service deployment

### Testing & Quality
- **Pytest 7.4+**: Python testing framework
- **Selenium 4.15+**: Browser automation (40+ UI tests)
- **Django Test Client**: Unit testing utilities
- **Pytest Fixtures**: Test data management

### Tools & Infrastructure
- **Git/GitHub**: Version control
- **Docker**: Containerization ready
- **Systemd**: Service management
- **SSL/TLS**: HTTPS encryption

---

## DevOps Workflow

### Jenkins Pipeline (12 Stages)

```
1. Checkout → 2. Setup Environment → 3. Dependencies → 4. Code Quality
    ↓              ↓                  ↓                ↓
5. Database → 6. Unit Tests → 7. Selenium Tests → 8. Build
    ↓         ↓               ↓                     ↓
9. Deploy to Infrastructure → 10. Documentation → 11. Cleanup → 12. Report
```

**Key Pipeline Features:**
- Parameterized builds (environment selection: dev/staging/production)
- Automated database migrations
- Code quality scanning (pylint, coverage)
- Conditional Selenium tests
- Ansible playbook validation before deployment
- Build artifact archiving

### Infrastructure Automation

**Ansible Playbooks:**
- `site.yml`: Main orchestration playbook
- `setup-django.yml`: Django application deployment
- `setup-database.yml`: PostgreSQL configuration
- `setup-services.yml`: Serverless email service

**Multi-Environment Inventories:**
- `inventory/development.ini`: Local development
- `inventory/staging.ini`: Pre-production testing
- `inventory/production.ini`: Production deployment

**Jinja2 Configuration Templates:**
- `django.env.j2`: Django environment variables
- `gunicorn.service.j2`: Systemd service unit
- `nginx.conf.j2`: Reverse proxy configuration
- `postgresql.conf.j2`: Database server settings
- `gunicorn.conf.py.j2`: Application server configuration

### Puppet Infrastructure-as-Code

**Manifests:**
- `base.pp`: System baseline (packages, users, firewall)
- `web.pp`: Web server configuration (Nginx, SSL)
- `database.pp`: PostgreSQL server setup
- `cache.pp`: Caching layer (Redis)
- `monitoring.pp`: Application monitoring

---

## Project Structure

```
mediflow/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
│
├── config/                      # Django project settings
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # URL routing
│   ├── asgi.py                 # ASGI application
│   └── wsgi.py                 # WSGI application
│
├── accounts/                    # User authentication
│   ├── models.py               # CustomUser model
│   ├── views.py                # Auth views (signup, login)
│   ├── forms.py                # Auth forms
│   ├── urls.py                 # Auth URLs
│   └── migrations/
│
├── doctors/                     # Doctor management
│   ├── models.py               # Doctor, Availability models
│   ├── views.py                # Doctor dashboards
│   ├── forms.py                # Availability forms
│   ├── urls.py                 # Doctor URLs
│   └── migrations/
│
├── patients/                    # Patient management
│   ├── models.py               # Patient model
│   ├── views.py                # Patient dashboards
│   ├── urls.py                 # Patient URLs
│   └── migrations/
│
├── bookings/                    # Appointment management
│   ├── models.py               # Booking model
│   ├── views.py                # Booking logic
│   ├── urls.py                 # Booking URLs
│   ├── management/commands/
│   │   └── send_appointment_reminders.py
│   └── migrations/
│
├── services/                    # External integrations
│   ├── email_client.py         # Email service
│   └── google_calendar.py      # Calendar API
│
├── templates/                   # Django HTML templates
│   ├── base.html               # Base template
│   ├── accounts/               # Auth templates
│   ├── doctors/                # Doctor templates
│   ├── patients/               # Patient templates
│   └── bookings/               # Booking templates
│
├── static/                      # CSS, JS, images
│   └── css/
│       └── style.css
│
├── tests/                       # Test suite
│   ├── selenium/
│   │   ├── conftest.py         # Pytest fixtures & config
│   │   ├── test_login.py       # Auth workflow tests
│   │   ├── test_booking.py     # Booking workflow tests
│   │   └── test_dashboard.py   # Dashboard tests
│   └── __init__.py
│
├── jenkins/                     # Jenkins configuration
│   ├── Jenkinsfile             # Pipeline definition
│   └── scripts/                # Helper scripts
│
├── ansible/                     # Infrastructure automation
│   ├── playbooks/
│   │   ├── site.yml
│   │   ├── setup-django.yml
│   │   ├── setup-database.yml
│   │   └── setup-services.yml
│   ├── inventory/
│   │   ├── development.ini
│   │   ├── staging.ini
│   │   └── production.ini
│   ├── group_vars/
│   │   ├── all.yml
│   │   ├── webservers.yml
│   │   └── databases.yml
│   └── templates/
│       ├── django.env.j2
│       ├── gunicorn.service.j2
│       ├── nginx.conf.j2
│       ├── postgresql.conf.j2
│       └── gunicorn.conf.py.j2
│
├── puppet/                      # Infrastructure-as-code
│   └── manifests/
│       ├── init.pp
│       ├── base.pp
│       ├── web.pp
│       ├── database.pp
│       └── monitoring.pp
│
├── email-service/               # Serverless email function
│   ├── handler.py
│   ├── serverless.yml
│   └── requirements.txt
│
└── docs/                        # Documentation
    ├── PROFESSIONAL_AUDIT.md
    ├── CRITICAL_FIXES_COMPLETED.md
    └── AUDIT_QUICK_REFERENCE.md
```

---

## CI/CD Pipeline

### Pipeline Stages

1. **Checkout**: Clone repository from Git
2. **Environment Setup**: Configure Python 3.10, virtual environment
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Code Quality**: Pylint analysis, coverage metrics
5. **Database Migration**: Run Django migrations against test database
6. **Unit Tests**: Run test suite with pytest
7. **Selenium Tests**: Execute 41 browser automation tests (conditional)
8. **Build**: Create application artifacts
9. **Deploy to Infrastructure**: Validate and deploy via Ansible
10. **Documentation Generation**: Auto-generate API docs
11. **Cleanup**: Archive artifacts, clean workspace
12. **Report**: Build status reporting

### Environment Variables

```
PYTHON_VERSION=3.10
DEPLOYMENT_ENV=staging|production
DATABASE_URL=postgresql://user:pass@host:5432/db
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<generated-key>
```

---

## Testing Strategy

### Test Coverage: 41 Tests

**UI Workflow Tests (37 tests)**
- Login/Authentication (13 tests)
  - Valid credentials, invalid credentials
  - Session management, logout
  - Role-based access control
  
- Appointment Booking (10 tests)
  - Doctor list display
  - Availability slot visibility
  - Booking form submission
  - Slot unavailability after booking
  
- Dashboard Navigation (8 tests)
  - Doctor dashboard functionality
  - Patient booking view
  - Availability management
  
- Form Validation (6 tests)
  - Email format validation
  - Password strength requirements
  - Required field highlighting

**Database Integrity Tests (4 tests)**
- Booking creates valid database record
- Availability slot isolation by doctor
- Patient data isolation enforcement
- Role-based access at database level

### Test Execution

```bash
# Run all Selenium tests
pytest tests/selenium/ -v

# Run specific test class
pytest tests/selenium/test_booking.py::TestAppointmentBooking -v

# Generate coverage report
pytest --cov=. --cov-report=html
```

---

## Infrastructure Automation

### Ansible Provisioning

**Configuration Management:**
- OS package installation
- PostgreSQL database setup
- Gunicorn application server
- Nginx reverse proxy
- SSL/TLS certificate configuration
- System logging and monitoring

**Example Playbook Execution:**
```bash
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml -v
```

**Multi-Environment Support:**
- Development: SQLite, local Gunicorn
- Staging: PostgreSQL, Nginx, SSL testing
- Production: Full stack with monitoring

### Configuration Templates

**Django Environment (`django.env.j2`)**
- DEBUG, SECRET_KEY, ALLOWED_HOSTS
- Database credentials with environment-specific values
- Email service configuration
- Google Calendar API settings
- Logging levels and directories

**Gunicorn Service (`gunicorn.service.j2`)**
- Worker process configuration (auto-scaling based on CPU)
- Timeout and connection settings
- Systemd integration
- Automatic restart on failure
- Resource limits and security settings

**Nginx Configuration (`nginx.conf.j2`)**
- HTTPS with TLS 1.2+
- Rate limiting (10 req/s for general, 30 req/s for API)
- Gzip compression
- Security headers (X-Frame-Options, CSP)
- Static asset caching (30 days)

**PostgreSQL Settings (`postgresql.conf.j2`)**
- Connection pooling configuration
- Query optimization parameters
- Logging and monitoring
- Backup scheduling
- Replication support

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+ (production only)
- Git
- Virtual environment support

### Quick Start

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/mediflow.git
cd mediflow
```

**2. Create Virtual Environment**
```bash
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
# - SECRET_KEY: Django secret key
# - DATABASE_URL: PostgreSQL connection (if using production)
# - EMAIL_* : Email service credentials
# - GOOGLE_CALENDAR_* : Calendar API credentials
```

**5. Run Migrations**
```bash
python manage.py migrate
```

**6. Create Admin User**
```bash
python manage.py createsuperuser
```

**7. Start Development Server**
```bash
python manage.py runserver
```

Access at `http://localhost:8000`

### Admin Interface
- URL: `http://localhost:8000/admin/`
- Manage users, bookings, availability slots

---

## Key Implementation Details

### Concurrency-Safe Booking

Prevents double-booking using database-level transactions:

```python
with transaction.atomic():
    slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)
    if not slot.is_booked:
        Booking.objects.create(patient=patient, slot=slot)
        slot.is_booked = True
        slot.save()
```

### Role-Based Access Control

Decorator-based access enforcement:
```python
@login_required
@require_role('doctor')
def doctor_dashboard(request):
    # Only doctors can access
```

### Email Integration

Asynchronous notification via serverless function:
- Booking confirmation emails
- Appointment reminders (1-hour and 24-hour before)
- New appointment notifications for doctors

### Database Models

**CustomUser**
- Email, first_name, last_name
- role: DOCTOR | PATIENT
- google_calendar_token: JSON (OAuth token)

**AvailabilitySlot**
- doctor (ForeignKey)
- date, start_time, end_time
- is_booked (Boolean)

**Booking**
- patient (OneToOneField)
- doctor (ForeignKey)
- slot (OneToOneField)
- created_at, updated_at

---

## API Endpoints

### Authentication
- `POST /auth/signup/doctor/` - Doctor registration
- `POST /auth/signup/patient/` - Patient registration
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout

### Doctor Operations
- `GET /doctors/dashboard/` - Doctor dashboard
- `POST /doctors/create-availability/` - Create appointment slot
- `GET /doctors/availability/` - Manage availability
- `DELETE /doctors/availability/<id>/` - Remove availability

### Patient Operations
- `GET /patients/dashboard/` - Patient dashboard
- `GET /doctors/` - Browse doctors
- `GET /doctors/<id>/slots/` - View available slots
- `POST /bookings/book/<slot_id>/` - Book appointment

### Admin
- `GET /admin/` - Django admin panel

---

## Future Improvements

- **Docker Containerization**: Multi-container setup with docker-compose
- **Kubernetes Deployment**: Helm charts for cloud-native deployment
- **Advanced Monitoring**: Prometheus metrics and Grafana dashboards
- **Real-Time Notifications**: WebSocket implementation for live updates
- **Mobile App**: React Native client for iOS/Android
- **Analytics Dashboard**: Appointment statistics and performance metrics
- **Payment Integration**: Stripe/PayPal for appointment fees
- **Telemedicine**: Video consultation capability

---

## Learning Outcomes

This project demonstrates:
- **Full-Stack Development**: Backend (Django), Database (PostgreSQL), Frontend (HTML/CSS)
- **DevOps Engineering**: CI/CD pipelines, infrastructure automation, configuration management
- **Quality Assurance**: Automated testing, test coverage analysis
- **System Design**: Database transactions, concurrency control, security
- **Production Practices**: Multi-environment deployment, monitoring, logging
- **Infrastructure-as-Code**: Ansible playbooks, Puppet manifests

---

## Documentation

- [Professional Audit](PROFESSIONAL_AUDIT.md) - Detailed quality analysis
- [Critical Fixes](CRITICAL_FIXES_COMPLETED.md) - Infrastructure improvements
- [Quick Reference](AUDIT_QUICK_REFERENCE.md) - Quick lookup guide

---

## Author

**Mukta Redij**

- GitHub: [github.com/yourusername](https://github.com/yourusername)
- LinkedIn: [linkedin.com/in/yourusername](https://linkedin.com/in/yourusername)
- Portfolio: [yourportfolio.com](https://yourportfolio.com)

---

## License

MIT License - See LICENSE file for details

---



