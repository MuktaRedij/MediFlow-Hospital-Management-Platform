# Database Configuration
# Configures PostgreSQL database server

class mediflow::database {
  
  require mediflow::base
  
  # Install PostgreSQL
  class { '::postgresql::server':
    postgres_password => lookup('postgres_password', { 'default_value' => 'postgres' }),
    package_version => '14',
    manage_postgresql_contrib => true,
    manage_postgresql_contrib_package => true,
  }
  
  # Create MediFlow database user
  postgresql::server::role { $mediflow::db_user:
    password_hash => postgresql::postgresql_password(
      $mediflow::db_user,
      $mediflow::db_password
    ),
    createdb => true,
    createrole => false,
  }
  
  # Create MediFlow database
  postgresql::server::db { $mediflow::db_name:
    user => $mediflow::db_user,
    password => $mediflow::db_password,
    owner => $mediflow::db_user,
    encoding => 'UTF8',
    locale => 'en_US.UTF-8',
  }
  
  # Install PostgreSQL extensions
  postgresql::server::extension { 'uuid-ossp':
    database => $mediflow::db_name,
    require => Postgresql::Server::Db[$mediflow::db_name],
  }
  
  postgresql::server::extension { 'pgcrypto':
    database => $mediflow::db_name,
    require => Postgresql::Server::Db[$mediflow::db_name],
  }
  
  postgresql::server::extension { 'pg_trgm':
    database => $mediflow::db_name,
    require => Postgresql::Server::Db[$mediflow::db_name],
  }
  
  # Configure PostgreSQL for performance
  postgresql::server::config_entry { 'shared_buffers':
    value => '256MB',
    require => Class['::postgresql::server'],
  }
  
  postgresql::server::config_entry { 'effective_cache_size':
    value => '1GB',
  }
  
  postgresql::server::config_entry { 'work_mem':
    value => '16MB',
  }
  
  postgresql::server::config_entry { 'log_statement':
    value => 'all',
  }
  
  # Setup database backup
  file { '/usr/local/bin/backup_mediflow_db.sh':
    ensure => file,
    content => epp('mediflow/db_backup.sh.epp', {
      db_name => $mediflow::db_name,
      db_user => $mediflow::db_user,
    }),
    mode => '0755',
    owner => 'postgres',
    group => 'postgres',
  }
  
  # Schedule daily backups
  cron { 'mediflow_db_backup':
    command => '/usr/local/bin/backup_mediflow_db.sh',
    user => 'postgres',
    hour => 2,
    minute => 0,
  }
  
  # Create monitoring user
  postgresql::server::role { 'monitoring':
    password_hash => postgresql::postgresql_password(
      'monitoring',
      lookup('monitoring_password', { 'default_value' => 'monitoring123' })
    ),
    createdb => false,
    createrole => false,
  }
  
  # Grant monitoring user privileges
  postgresql::server::grant { 'monitoring_connect':
    role => 'monitoring',
    privilege => 'CONNECT',
    object_type => 'DATABASE',
    object_name => $mediflow::db_name,
    require => [
      Postgresql::Server::Role['monitoring'],
      Postgresql::Server::Db[$mediflow::db_name],
    ],
  }
}
