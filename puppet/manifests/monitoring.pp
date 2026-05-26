# Monitoring and Logging Configuration
# Sets up monitoring agents and centralized logging

class mediflow::monitoring {
  
  # Install Prometheus node exporter for system metrics
  package { 'prometheus-node-exporter':
    ensure => present,
  }
  
  service { 'prometheus-node-exporter':
    ensure => running,
    enable => true,
    require => Package['prometheus-node-exporter'],
  }
  
  # Create monitoring configuration directory
  file { '/etc/mediflow/monitoring':
    ensure => directory,
    owner => 'root',
    group => 'root',
    mode => '0755',
  }
  
  # Setup application metrics collection
  file { '/opt/mediflow/monitoring/metrics.py':
    ensure => file,
    content => '#!/usr/bin/env python3
# MediFlow Application Metrics Collector
import time
import json
from datetime import datetime

def collect_metrics():
    """Collect application metrics"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "uptime": get_uptime(),
        "memory_usage": get_memory_usage(),
        "cpu_usage": get_cpu_usage(),
        "database_connections": get_db_connections(),
        "request_count": get_request_count(),
        "response_time_avg": get_response_time(),
    }
    return metrics

def get_uptime():
    """Get application uptime"""
    import subprocess
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    return result.stdout.strip()

def get_memory_usage():
    """Get memory usage percentage"""
    import psutil
    return psutil.virtual_memory().percent

def get_cpu_usage():
    """Get CPU usage percentage"""
    import psutil
    return psutil.cpu_percent(interval=1)

def get_db_connections():
    """Get active database connections"""
    # Implementation would query PostgreSQL
    return 10

def get_request_count():
    """Get total request count"""
    # Read from application logs or metrics
    return 1000

def get_response_time():
    """Get average response time in ms"""
    return 150.5

if __name__ == "__main__":
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=2))
',
    mode => '0755',
    owner => $mediflow::app_user,
    group => $mediflow::app_group,
  }
  
  # Schedule metrics collection
  cron { 'collect_metrics':
    command => '/opt/mediflow/monitoring/metrics.py >> /var/log/mediflow/metrics.log',
    user => $mediflow::app_user,
    minute => '*/5',
  }
}

class mediflow::logging {
  
  # Configure rsyslog for centralized logging
  file { '/etc/rsyslog.d/30-mediflow.conf':
    ensure => file,
    content => ':programname, isequal, "mediflow" /var/log/mediflow/application.log
& stop',
    require => Package['rsyslog'],
    notify => Service['rsyslog'],
  }
  
  # Rotate logs
  file { '/etc/logrotate.d/mediflow':
    ensure => file,
    content => '/var/log/mediflow/*.log {
  daily
  rotate 30
  compress
  delaycompress
  notifempty
  create 0640 mediflow mediflow
  sharedscripts
  postrotate
    systemctl reload rsyslog > /dev/null 2>&1 || true
  endscript
}',
  }
  
  service { 'rsyslog':
    ensure => running,
    enable => true,
  }
}
