# MediFlow Ansible Playbooks
# Infrastructure and Configuration Management for Healthcare Platform

## Directory Structure
```
ansible/
├── playbooks/
│   ├── site.yml
│   ├── deploy.yml
│   ├── setup-django.yml
│   ├── setup-database.yml
│   └── setup-services.yml
├── roles/
│   ├── common/
│   ├── django/
│   ├── postgresql/
│   └── email-service/
├── inventory/
│   ├── production.ini
│   ├── staging.ini
│   └── development.ini
├── group_vars/
│   ├── all.yml
│   ├── webservers.yml
│   └── databases.yml
├── host_vars/
│   └── mediflow-prod-01.yml
└── ansible.cfg
```

## Usage

```bash
# Deploy to staging
ansible-playbook -i inventory/staging.ini playbooks/site.yml

# Deploy to production
ansible-playbook -i inventory/production.ini playbooks/site.yml

# Run specific playbook
ansible-playbook -i inventory/staging.ini playbooks/setup-django.yml

# Check syntax
ansible-playbook -i inventory/staging.ini playbooks/site.yml --syntax-check

# Dry run
ansible-playbook -i inventory/staging.ini playbooks/site.yml --check
```

## Notes
- All playbooks use idempotent modules
- Handlers manage service restarts
- Variables are environment-specific
- Secrets stored in vault (not in version control)
