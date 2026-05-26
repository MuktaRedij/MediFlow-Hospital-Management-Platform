# Puppet Configuration
# Infrastructure as Code for MediFlow Platform
# Ensures consistent environment configuration

## Puppet Modules Structure
```
puppet/
├── manifests/
│   ├── init.pp           # Main manifest
│   ├── base.pp           # Base system configuration
│   ├── web.pp            # Web server configuration
│   ├── database.pp       # Database configuration
│   └── monitoring.pp     # Monitoring setup
├── modules/
│   ├── mediflow/
│   │   ├── manifests/
│   │   ├── files/
│   │   ├── templates/
│   │   └── hiera.yaml
│   ├── nginx/
│   ├── postgresql/
│   └── gunicorn/
└── hiera/
    ├── common.yaml
    ├── production.yaml
    ├── staging.yaml
    └── development.yaml
```

## Usage

```bash
# Apply catalog on local machine
puppet apply manifests/site.pp

# Apply to specific node
puppet agent -t

# Validate syntax
puppet parser validate manifests/site.pp

# Generate catalog
puppet master --compile <nodename>

# Check before applying (dry run)
puppet apply --noop manifests/site.pp
```

## Key Features
- Declarative configuration management
- Environment consistency
- Automatic service management
- Package version pinning
- Templated configurations
