# Ansible Playbook Execution Guide
## Infrastructure Provisioning and Configuration

This guide covers running Ansible playbooks for MediFlow infrastructure.

## Prerequisites

### Install Ansible

```bash
# Ubuntu/Debian
sudo apt-get install -y ansible

# macOS
brew install ansible

# Python package (any OS)
pip install ansible==2.10.0

# Verify installation
ansible --version
```

### Setup SSH Access

```bash
# Generate SSH key if needed
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mediflow-key

# Copy key to target hosts
ssh-copy-id -i ~/.ssh/mediflow-key ubuntu@10.0.1.10

# Test connectivity
ssh -i ~/.ssh/mediflow-key ubuntu@10.0.1.10
```

## Inventory Configuration

### Production Inventory

**File:** `ansible/inventory/production.ini`

```ini
[webservers]
mediflow-prod-web-01 ansible_host=10.0.1.10 ansible_user=ubuntu
mediflow-prod-web-02 ansible_host=10.0.1.11 ansible_user=ubuntu

[databases]
mediflow-prod-db-01 ansible_host=10.0.2.10 ansible_user=ubuntu

[all:vars]
ansible_ssh_private_key_file=~/.ssh/mediflow-prod.pem
```

### Staging Inventory

**File:** `ansible/inventory/staging.ini`

```ini
[webservers]
mediflow-staging-web-01 ansible_host=10.1.1.10 ansible_user=ubuntu

[databases]
mediflow-staging-db-01 ansible_host=10.1.2.10 ansible_user=ubuntu
```

## Running Playbooks

### Syntax Check

```bash
# Validate playbook syntax
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --syntax-check
```

### Dry Run (Check Mode)

```bash
# Preview changes without applying
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --check

# Verbose dry run
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --check -vvv
```

### Full Playbook Execution

```bash
# Deploy to staging
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml

# Deploy to production
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml

# With extra verbosity
ansible-playbook -i ansible/inventory/production.ini \
  ansible/playbooks/site.yml -vvv
```

## Individual Playbooks

### Setup Django Application

```bash
# Install and configure Django app
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/setup-django.yml

# Dry run
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/setup-django.yml \
  --check
```

**What it does:**
- Creates application directories
- Clones repository
- Creates Python virtual environment
- Installs dependencies
- Configures Django settings
- Runs migrations
- Collects static files
- Sets up Gunicorn service
- Configures Nginx

### Setup Database

```bash
# Install and configure PostgreSQL
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/setup-database.yml

# Only database users
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/setup-database.yml \
  --tags "user-creation"
```

**What it does:**
- Installs PostgreSQL
- Configures PostgreSQL settings
- Creates database user
- Creates application database
- Enables extensions
- Sets up backups
- Configures monitoring

### Setup Services

```bash
# Deploy email service
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/setup-services.yml
```

## Variable Management

### Global Variables

**File:** `ansible/group_vars/all.yml`

```yaml
app_name: mediflow
app_user: django
app_home: /opt/mediflow
python_version: "3.10"
```

### Web Server Variables

**File:** `ansible/group_vars/webservers.yml`

```yaml
gunicorn_workers: 4
nginx_port: 80
enable_gzip: true
```

### Overriding Variables

```bash
# Via command line
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  -e "app_port=9000"

# Multiple variables
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  -e "gunicorn_workers=8 nginx_port=8080"

# From file
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  -e "@vars.yml"
```

## Ad Hoc Commands

### Gather Host Facts

```bash
# Get information about hosts
ansible -i ansible/inventory/staging.ini webservers -m setup

# Get specific facts
ansible -i ansible/inventory/staging.ini webservers \
  -m setup -a "filter=ansible_os_family"
```

### Run Commands

```bash
# Execute command on all webservers
ansible -i ansible/inventory/staging.ini webservers \
  -m command -a "python --version"

# Copy file to hosts
ansible -i ansible/inventory/staging.ini webservers \
  -m copy -a "src=file.txt dest=/tmp/file.txt"

# Restart service
ansible -i ansible/inventory/staging.ini webservers \
  -m systemd -a "name=nginx state=restarted"
```

## Secrets Management

### Using Ansible Vault

```bash
# Create encrypted variables file
ansible-vault create ansible/vars/secrets.yml

# Edit encrypted file
ansible-vault edit ansible/vars/secrets.yml

# Run playbook with vault password
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --ask-vault-pass

# Or with password file
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --vault-password-file=.vault_password
```

### Vault File Example

```yaml
# vars/secrets.yml (encrypted)
vault_django_secret_key: "your-secret-key-here"
vault_db_user: "mediflow_user"
vault_db_password: "secure-password"
vault_monitoring_password: "monitoring-password"
```

## Monitoring Execution

### Verbose Output

```bash
# Show task details
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml -v

# Very verbose (debug info)
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml -vvv

# Extremely verbose
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml -vvvv
```

### Callback Plugins

```bash
# Use profile callback
ANSIBLE_STDOUT_CALLBACK=profile \
  ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml

# Use dense callback
ANSIBLE_STDOUT_CALLBACK=dense \
  ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml
```

## Troubleshooting

### Connection Issues

```bash
# Test connectivity
ansible -i ansible/inventory/staging.ini all -m ping

# With verbose output
ansible -i ansible/inventory/staging.ini all -m ping -vvv

# Specify SSH key
ansible -i ansible/inventory/staging.ini all \
  -m ping \
  -e "ansible_ssh_private_key_file=~/.ssh/mediflow-key"
```

### Permission Issues

```bash
# Use sudo without password
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  -k  # Ask for password

# Or use become password
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  -K  # Ask for become password
```

### Failed Tasks

```bash
# Continue on failed hosts
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --continue-on-errors

# Fail on first error (default)
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  --fail-fast
```

## Idempotency

Ansible playbooks should be idempotent (safe to run multiple times):

```bash
# Run playbook twice - should produce same result
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml

ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml
```

## Performance Tuning

### Parallel Execution

```bash
# Run on multiple hosts in parallel (default: 5)
ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml \
  -f 10  # Run on 10 hosts in parallel
```

### Callback Timing

```bash
# See how long each task takes
ANSIBLE_STDOUT_CALLBACK=profile \
  ansible-playbook -i ansible/inventory/staging.ini \
  ansible/playbooks/site.yml
```

## Backup and Rollback

### Backup Configuration

```bash
# Backup host files before changes
ansible -i ansible/inventory/staging.ini all \
  -m shell -a "tar -czf /backup/config-$(date +%s).tar.gz /etc"
```

### Rollback Strategy

1. Keep previous versions in version control
2. Use Ansible handlers for graceful restarts
3. Test in staging before production
4. Have rollback playbook ready

## Best Practices

1. **Test in staging first** - Always test in staging environment
2. **Use version control** - Keep playbooks in Git
3. **Document variables** - Comment configuration
4. **Use roles** - Organize into reusable roles
5. **Encrypt secrets** - Use Ansible Vault
6. **Idempotent tasks** - Safe to run multiple times
7. **Error handling** - Graceful failure recovery
8. **Logging** - Enable detailed logging

---

For more information, see:
- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
