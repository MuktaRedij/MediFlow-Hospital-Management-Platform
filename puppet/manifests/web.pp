# Web Server Configuration
# Configures Nginx and Gunicorn for Django application

class mediflow::web {
  
  require mediflow::base
  
  # Install Nginx
  class { '::nginx':
    ensure => present,
    manage_repo => true,
    package_ensure => 'latest',
  }
  
  # Create Nginx configuration for MediFlow
  nginx::resource::server { 'mediflow':
    listen_port => 80,
    listen_ipv6_port => 80,
    server_name => [
      'mediflow.local',
      'www.mediflow.local',
      $::ipaddress,
    ],
    proxy => 'http://gunicorn_backend',
    access_log => '/var/log/nginx/mediflow_access.log',
    error_log => '/var/log/nginx/mediflow_error.log',
    format_log => 'combined',
  }
  
  # Upstream backend for Gunicorn
  nginx::resource::upstream { 'gunicorn_backend':
    members => [
      "unix:${mediflow::app_home}/run/gunicorn.sock",
    ],
    keepalive => 32,
  }
  
  # Create run directory for socket file
  file { "${mediflow::app_home}/run":
    ensure => directory,
    owner => $mediflow::app_user,
    group => $mediflow::app_group,
    mode => '0755',
  }
  
  # Install Gunicorn
  package { 'gunicorn':
    ensure => present,
    provider => 'pip3',
  }
  
  # Create Gunicorn systemd service
  systemd::unit_file { 'mediflow-gunicorn.service':
    content => epp('mediflow/gunicorn.service.epp', {
      app_home => $mediflow::app_home,
      app_user => $mediflow::app_user,
      app_group => $mediflow::app_group,
      app_port => $mediflow::app_port,
    }),
    enable => true,
    active => true,
  }
  
  # Enable and start Nginx
  service { 'nginx':
    ensure => running,
    enable => true,
    require => Class['::nginx'],
  }
  
  # Setup SSL/TLS (if certificates available)
  if lookup('enable_ssl', { 'default_value' => false }) {
    nginx::resource::server { 'mediflow-ssl':
      listen_port => 443,
      listen_ipv6_port => 443,
      server_name => [
        'mediflow.local',
        'www.mediflow.local',
      ],
      ssl => true,
      ssl_cert => lookup('ssl_cert_path', { 'default_value' => '/etc/ssl/certs/mediflow.crt' }),
      ssl_key => lookup('ssl_key_path', { 'default_value' => '/etc/ssl/private/mediflow.key' }),
      proxy => 'http://gunicorn_backend',
      access_log => '/var/log/nginx/mediflow_ssl_access.log',
      error_log => '/var/log/nginx/mediflow_ssl_error.log',
    }
    
    # Redirect HTTP to HTTPS
    nginx::resource::server { 'mediflow-redirect':
      listen_port => 80,
      server_name => ['mediflow.local', 'www.mediflow.local'],
      rewrite_rules => [
        '^(.*)$ https://mediflow.local$1 permanent',
      ],
    }
  }
  
  # Configure Nginx performance tuning
  file { '/etc/nginx/nginx.conf':
    ensure => file,
    content => epp('mediflow/nginx.conf.epp', {
      worker_processes => $::processorcount,
      worker_connections => 1024,
      keepalive_timeout => 65,
    }),
    require => Class['::nginx'],
    notify => Service['nginx'],
  }
  
  # Create health check endpoint
  file { "${mediflow::app_home}/health_check.sh":
    ensure => file,
    content => '#!/bin/bash
curl -f -s http://localhost:8000/health/ > /dev/null && echo "OK" || echo "FAILED"',
    mode => '0755',
    owner => $mediflow::app_user,
    group => $mediflow::app_group,
  }
}

# Nginx module
class mediflow::nginx {
  package { 'nginx':
    ensure => latest,
  }
  
  service { 'nginx':
    ensure => running,
    enable => true,
    require => Package['nginx'],
  }
}

# Gunicorn module
class mediflow::gunicorn {
  package { 'gunicorn':
    ensure => present,
    provider => 'pip3',
  }
  
  service { 'mediflow-gunicorn':
    ensure => running,
    enable => true,
    require => Package['gunicorn'],
  }
}
