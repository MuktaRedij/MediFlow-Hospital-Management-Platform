# MediFlow DevOps Documentation
## Production-Grade Healthcare Platform Infrastructure

This comprehensive guide covers the DevOps and automation infrastructure for the MediFlow Healthcare Management System.

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [CI/CD Pipeline](#cicd-pipeline)
3. [Testing Automation](#testing-automation)
4. [Infrastructure as Code](#infrastructure-as-code)
5. [Configuration Management](#configuration-management)
6. [Deployment Procedures](#deployment-procedures)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Best Practices](#security-best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   LOAD BALANCER (Nginx)                 │
│                     Port 80/443                          │
└──────────────┬──────────────────────────────────────────┘
               │
     ┌─────────┴────────────┐
     │                      │
┌────▼─────────────┐  ┌────▼─────────────┐
│  WEB SERVER 1    │  │  WEB SERVER 2    │
│  Gunicorn        │  │  Gunicorn        │
│  Django App      │  │  Django App      │
│  Port 8000       │  │  Port 8000       │
└────┬─────────────┘  └────┬─────────────┘
     │                      │
     └──────────┬───────────┘
                │
        ┌───────▼────────┐
        │  DATABASE      │
        │  PostgreSQL    │
        │  Port 5432     │
        └────────────────┘
```

### Technology Stack

**Web Application:**
- Django 4.2+ (Python 3.10+)
- PostgreSQL 14+ (Production)
- Gunicorn (WSGI Application Server)
- Nginx (Reverse Proxy)

**CI/CD:**
- Jenkins (Pipeline Orchestration)
- Selenium (UI Testing)
- pytest (Unit Testing)

**Infrastructure Automation:**
- Ansible (Configuration Management)
- Puppet (Infrastructure as Code)

**Monitoring:**
- Prometheus (Metrics Collection)
- Node Exporter (System Metrics)
- Custom Application Metrics

---

## CI/CD Pipeline

### Jenkins Pipeline Stages

The Jenkins pipeline (`Jenkinsfile`) orchestrates the complete build and deployment workflow:

```
┌─────────────┐
│  Checkout   │ - Clone source code from repository
└──────┬──────┘
       │
┌──────▼──────────────┐
│ Environment Setup   │ - Create Python virtual environment
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Install Dependencies│ - Install Python and system packages
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Code Quality        │ - Run Flake8, Pylint analysis
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Database Migration  │ - Run Django migrations
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Django Unit Tests   │ - Run pytest for Django apps
└──────┬──────────────┘
       │
┌──────▼──────────────────┐
│ Selenium Tests          │ - Run browser automation tests
│ (Optional)              │
└──────┬──────────────────┘
       │
┌──────▼──────────────┐
│ Build Application   │ - Collect static files, create artifacts
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Deploy Simulation   │ - Prepare deployment manifest
└──────┬──────────────┘
       │
┌──────▼──────────────┐
│ Generate Reports    │ - Create build report and documentation
└─────────────────────┘
```

### Pipeline Configuration

**Location:** `Jenkinsfile`

**Key Features:**
- Supports multiple deployment environments (dev, staging, production)
- Parameterized builds for flexibility
- Clean console output with ASCII art
- Comprehensive error handling
- Artifact archiving
- Automatic cleanup

### Running the Pipeline

```bash
# Trigger Jenkins pipeline
curl -X POST http://jenkins-server:8080/job/MediFlow/build

# With parameters
curl -X POST http://jenkins-server:8080/job/MediFlow/buildWithParameters \
  -d "DEPLOYMENT_ENV=staging" \
  -d "SKIP_SELENIUM=false"
```

### Pipeline Configuration Example

```groovy
// View Jenkinsfile for complete configuration
// Key parameters:
// - DEPLOYMENT_ENV: dev | staging | production
// - SKIP_SELENIUM: true | false (skip browser tests)
```

---

## Testing Automation

### Selenium Test Suite

**Location:** `tests/selenium/`

#### Test Structure

```
tests/selenium/
├── conftest.py           # Pytest fixtures and configuration
├── test_login.py         # Authentication tests
├── test_booking.py       # Appointment booking tests
└── test_dashboard.py     # Dashboard navigation tests
```

#### Test Coverage

**Login & Authentication:**
- Page load verification
- Valid credential authentication
- Invalid credential handling
- Session persistence
- Logout functionality

**Appointment Booking:**
- Doctor list display
- Availability slots viewing
- Form validation
- Time slot selection
- Booking confirmation
- Double-booking prevention

**Dashboard:**
- Page load and structure
- Navigation menu
- Profile menu access
- Responsive design (mobile, tablet)
- Accessibility (keyboard navigation)

**Form Validation:**
- Email format validation
- Password strength
- Required field checking

#### Running Selenium Tests

```bash
# Run all Selenium tests
pytest tests/selenium/ -v

# Run specific test file
pytest tests/selenium/test_login.py -v

# Run specific test
pytest tests/selenium/test_login.py::TestLoginFlow::test_doctor_login_success -v

# Run with headless browser
HEADLESS_BROWSER=true pytest tests/selenium/ -v

# Generate HTML report
pytest tests/selenium/ --html=report.html --self-contained-html
```

#### Test Fixtures

**conftest.py provides:**
- Chrome WebDriver configuration
- Django test user fixtures
- WebDriverWait helper
- SeleniumTestHelper utility class

```python
# Using fixtures in tests
def test_login(driver, wait, test_doctor, selenium_helper):
    SeleniumTestHelper.login(driver, 'testdoctor', 'password', wait)
    # Test continues...
```

### Unit Tests

```bash
# Run Django unit tests
python manage.py test accounts doctors patients bookings

# Run with coverage
coverage run --source='.' manage.py test
coverage report

# Generate HTML coverage report
coverage html
```

---

## Infrastructure as Code

### Ansible Configuration

**Location:** `ansible/`

Ansible automates environment provisioning and configuration management.

#### Directory Structure

```
ansible/
├── playbooks/
│   ├── site.yml              # Main playbook (orchestrates all)
│   ├── setup-django.yml      # Django application setup
│   ├── setup-database.yml    # PostgreSQL configuration
│   └── setup-services.yml    # Email service setup
├── inventory/
│   ├── production.ini        # Production hosts
│   ├── staging.ini           # Staging hosts
│   └── development.ini       # Development hosts
├── group_vars/
│   ├── all.yml               # Global variables
│   ├── webservers.yml        # Web server config
│   └── databases.yml         # Database config
└── roles/                    # (Extensible for custom roles)
```

#### Running Ansible Playbooks

```bash
# Deploy to staging
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml

# Deploy to production
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml

# Dry run (check mode)
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml --check

# Verbose output
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml -vvv

# Run specific playbook
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/setup-django.yml
```

#### Playbook Capabilities

**site.yml (Main Orchestration):**
- System package updates
- System dependency installation
- Hostname configuration
- Timezone setup
- System limits configuration
- Web server health checks
- Database connectivity verification
- Email service validation

**setup-django.yml (Application Setup):**
- Create application directories
- Clone application repository
- Create Python virtual environment
- Install dependencies
- Configure Django environment
- Run database migrations
- Collect static files
- Setup Gunicorn service
- Configure Nginx reverse proxy
- Create health check script

**setup-database.yml (Database Configuration):**
- Install PostgreSQL server
- Configure PostgreSQL settings
- Create database user
- Create application database
- Enable PostgreSQL extensions
- Setup automated backups
- Configure monitoring user

**setup-services.yml (Email Service):**
- Install service dependencies
- Deploy email service
- Configure environment
- Start and enable service

#### Configuration Variables

**Global Variables (all.yml):**
```yaml
app_name: mediflow
app_user: django
app_home: /opt/mediflow
python_version: "3.10"
django_settings: "config.settings"
```

**Web Server Variables (webservers.yml):**
```yaml
gunicorn_workers: 4
nginx_port: 80
enable_gzip: true
```

**Database Variables (databases.yml):**
```yaml
postgresql_version: "14"
postgresql_max_connections: 200
enable_replication: false
```

---

## Configuration Management

### Puppet Infrastructure

**Location:** `puppet/`

Puppet ensures consistent infrastructure configuration across all nodes.

#### Puppet Manifests

```
puppet/manifests/
├── init.pp          # Main manifest (node definitions)
├── base.pp          # Base system configuration
├── web.pp           # Web server configuration
├── database.pp      # Database configuration
└── monitoring.pp    # Monitoring setup
```

#### Resource Types Managed

**Base System:**
- System packages installation
- User and group management
- Directory creation
- SSH key configuration
- Firewall rules
- NTP service
- System logging

**Web Configuration:**
- Nginx installation and configuration
- Gunicorn setup
- Systemd services
- SSL/TLS certificate management
- Performance tuning

**Database Configuration:**
- PostgreSQL installation
- Database and user creation
- Extension installation
- Performance tuning
- Backup scheduling
- Monitoring user setup

**Monitoring:**
- Prometheus node exporter
- Application metrics collection
- Centralized logging
- Log rotation

#### Applying Puppet Configuration

```bash
# Apply local catalog
sudo puppet apply puppet/manifests/init.pp

# Apply with specific environment
sudo puppet apply puppet/manifests/init.pp \
  -e "environment=production"

# Validate syntax
puppet parser validate puppet/manifests/init.pp

# Generate graph
puppet graph --resources puppet/manifests/init.pp
```

---

## Deployment Procedures

### Pre-Deployment Checklist

- [ ] Code review approved
- [ ] All tests passing
- [ ] Database migrations prepared
- [ ] Backup created
- [ ] Deployment window scheduled
- [ ] Team notified
- [ ] Rollback plan documented

### Staging Deployment

```bash
# 1. Checkout code
cd /opt/mediflow
git fetch origin
git checkout staging

# 2. Run Ansible playbook
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml

# 3. Run tests
python manage.py test --failfast

# 4. Run Selenium tests
pytest tests/selenium/ -v

# 5. Health checks
curl http://staging.mediflow.local/health/
```

### Production Deployment

```bash
# 1. Pre-deployment
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml \
  --check  # Dry run

# 2. Execute deployment
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml

# 3. Verify deployment
curl https://mediflow.local/health/

# 4. Monitor logs
tail -f /var/log/mediflow/application.log

# 5. Smoke tests
pytest tests/selenium/test_login.py::TestLoginFlow::test_doctor_login_success
```

### Rollback Procedure

```bash
# 1. Identify current version
git log --oneline -5

# 2. Revert to previous version
git revert HEAD

# 3. Re-run deployment
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml

# 4. Verify
curl https://mediflow.local/health/

# 5. Notify team
echo "Rollback completed to previous version"
```

---

## Monitoring & Logging

### Application Logs

**Location:** `/var/log/mediflow/`

```bash
# View application logs
tail -f /var/log/mediflow/application.log

# View Gunicorn logs
journalctl -u mediflow-gunicorn -f

# View Nginx logs
tail -f /var/log/nginx/mediflow_access.log
tail -f /var/log/nginx/mediflow_error.log
```

### System Monitoring

**Prometheus Metrics:**
```
http://localhost:9090/
```

**Node Exporter:**
```
http://localhost:9100/metrics
```

### Health Checks

```bash
# Application health
curl http://localhost:8000/health/

# Database connection
python manage.py dbshell

# Email service
curl http://email-service.local/health/

# System status
systemctl status mediflow-gunicorn
systemctl status nginx
systemctl status postgresql
```

---

## Security Best Practices

### Environment Variables

Store sensitive data in `.env` (not in version control):

```bash
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=mediflow.local,www.mediflow.local
DATABASE_URL=postgresql://user:password@db:5432/mediflow_db
EMAIL_API_KEY=your-email-service-api-key
GOOGLE_OAUTH_SECRET=your-google-oauth-secret
```

### Database Security

- Enable SSL for database connections
- Use strong passwords
- Restrict database user privileges
- Regular backups with encryption
- Monitor failed login attempts

### Application Security

- HTTPS/TLS enabled
- CSRF protection enabled
- XSS protection headers
- SQL injection prevention (ORM)
- Password hashing (bcrypt)
- Session cookie security

### Infrastructure Security

- Firewall rules configured
- SSH key-based authentication
- Automatic security updates
- Fail2ban for brute-force protection
- Regular security audits

---

## Troubleshooting

### Common Issues

**1. Database Connection Failed**
```bash
# Check PostgreSQL service
systemctl status postgresql

# Test connection
psql -h db_host -U db_user -d mediflow_db

# Check logs
tail -f /var/log/postgresql/postgresql.log
```

**2. Gunicorn Not Starting**
```bash
# Check service status
systemctl status mediflow-gunicorn

# View logs
journalctl -u mediflow-gunicorn -n 50

# Test manually
source /opt/mediflow/venv/bin/activate
cd /opt/mediflow
gunicorn config.wsgi:application
```

**3. Nginx 502 Bad Gateway**
```bash
# Check upstream
curl http://127.0.0.1:8000/

# Check socket file
ls -la /opt/mediflow/run/gunicorn.sock

# Reload Nginx
systemctl reload nginx
```

**4. Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check permissions
ls -la /opt/mediflow/static/

# Check Nginx config
nginx -t
```

### Debug Mode

```bash
# Enable debug logging
export DEBUG=True
export LOG_LEVEL=DEBUG

# Run application
python manage.py runserver 0.0.0.0:8000

# Check logs
tail -f /var/log/mediflow/debug.log
```

---

## Support & Documentation

- **Jenkins Documentation:** https://www.jenkins.io/doc/
- **Ansible Documentation:** https://docs.ansible.com/
- **Puppet Documentation:** https://puppet.com/docs/
- **Django Documentation:** https://docs.djangoproject.com/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial release with Jenkins, Ansible, Puppet integration |

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** DevOps Team
