# Puppet Main Manifest
# Defines the complete infrastructure configuration for MediFlow

# Define the main class
class { 'mediflow':
  environment   => $environment,
  app_home      => '/opt/mediflow',
  python_version => '3.10',
  db_host       => lookup('db_host', { 'default_value' => 'localhost' }),
  db_name       => lookup('db_name', { 'default_value' => 'mediflow' }),
  db_user       => lookup('db_user', { 'default_value' => 'mediflow' }),
  db_password   => lookup('db_password', { 'default_value' => 'changeme' }),
  app_port      => 8000,
}

# Apply base configuration
include mediflow::base

# Apply web server configuration based on node role
case $::mediflow_role {
  'webserver': {
    include mediflow::web
    include mediflow::nginx
    include mediflow::gunicorn
  }
  'database': {
    include mediflow::database
  }
  'cache': {
    include mediflow::cache
  }
  'email': {
    include mediflow::email
  }
  default: {
    notify { 'unknown-role': message => "Unknown role: ${mediflow_role}" }
  }
}

# Apply monitoring to all nodes
include mediflow::monitoring

# Apply logging to all nodes
include mediflow::logging

# Fire events for Puppet notifications
if $apply_success {
  notify { 'apply-success':
    message => "Successfully applied Puppet catalog to ${::hostname}",
  }
}
