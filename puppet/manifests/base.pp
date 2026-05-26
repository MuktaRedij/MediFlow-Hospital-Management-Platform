# Base System Configuration
# Common configuration applied to all nodes

class mediflow::base {
  
  # Update system packages
  exec { 'update-system':
    command => '/usr/bin/apt-get update && /usr/bin/apt-get upgrade -y',
    refreshonly => false,
    logoutput => true,
  }
  
  # Set timezone
  class { 'timezone':
    timezone => 'UTC',
  }
  
  # Install common packages
  package { [
    'curl',
    'wget',
    'git',
    'vim',
    'htop',
    'net-tools',
    'build-essential',
    'libssl-dev',
    'libffi-dev',
    'python3-dev',
    'python3-pip',
    'python3-venv',
  ]:
    ensure => present,
    require => Exec['update-system'],
  }
  
  # Create application user
  user { $mediflow::app_user:
    ensure => present,
    home => $mediflow::app_home,
    shell => '/bin/bash',
    managehome => true,
  }
  
  # Create application group
  group { $mediflow::app_group:
    ensure => present,
  }
  
  # Create application home directory
  file { $mediflow::app_home:
    ensure => directory,
    owner => $mediflow::app_user,
    group => $mediflow::app_group,
    mode => '0755',
  }
  
  # Create log directory
  file { '/var/log/mediflow':
    ensure => directory,
    owner => $mediflow::app_user,
    group => $mediflow::app_group,
    mode => '0755',
  }
  
  # Configure sysctl for performance
  sysctl { 'net.ipv4.ip_forward':
    value => '1',
  }
  
  sysctl { 'net.ipv4.conf.all.rp_filter':
    value => '1',
  }
  
  # Setup SSH key-based authentication
  ssh_authorized_key { "${mediflow::app_user}_deploy":
    user => $mediflow::app_user,
    type => 'ssh-rsa',
    key => lookup('deploy_public_key', { 'default_value' => 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB...' }),
  }
  
  # Configure firewall rules (if using firewalld)
  if $::os['family'] == 'RedHat' {
    service { 'firewalld':
      ensure => running,
      enable => true,
    }
    
    firewall { '100 allow http':
      dport => 80,
      proto => 'tcp',
      action => 'accept',
    }
    
    firewall { '101 allow https':
      dport => 443,
      proto => 'tcp',
      action => 'accept',
    }
  }
  
  # Setup NTP for time synchronization
  class { '::ntp':
    servers => [
      '0.ubuntu.pool.ntp.org',
      '1.ubuntu.pool.ntp.org',
      '2.ubuntu.pool.ntp.org',
      '3.ubuntu.pool.ntp.org',
    ],
    autoupdate => true,
  }
  
  # Setup rsyslog for centralized logging
  class { '::rsyslog':
    ensure => present,
  }
  
  # Install security updates
  package { 'unattended-upgrades':
    ensure => present,
  }
  
  service { 'unattended-upgrades':
    ensure => running,
    enable => true,
    require => Package['unattended-upgrades'],
  }
}
