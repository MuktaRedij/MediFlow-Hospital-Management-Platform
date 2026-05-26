# Jenkins Setup Guide
## Installation and Configuration for MediFlow

This guide covers Jenkins installation, configuration, and pipeline setup for MediFlow.

## Installation

### Prerequisites
- Linux server (Ubuntu 20.04+ or CentOS 7+)
- Java 11 or later
- Git
- 2GB+ RAM
- 20GB+ disk space

### Install Jenkins

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update
sudo apt-get install -y jenkins

# Start Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Access Jenkins

```
http://localhost:8080
```

Follow the setup wizard to complete initial configuration.

## Configure Jenkins for MediFlow

### 1. Install Required Plugins

Navigate to **Manage Jenkins** → **Manage Plugins** → **Available** and install:

- Pipeline
- Blue Ocean
- Git
- GitHub
- Email Extension
- Slack Notification
- Cobertura Plugin
- JUnit Plugin
- Python Plugin

### 2. Create Pipeline Job

1. Click **New Item**
2. Enter job name: `MediFlow`
3. Select **Pipeline**
4. Click **OK**

### 3. Configure Pipeline

**Pipeline section:**
- Definition: `Pipeline script from SCM`
- SCM: `Git`
- Repository URL: `https://github.com/your-org/mediflow.git`
- Script Path: `Jenkinsfile`
- Branch: `*/main`

### 4. Build Triggers

Enable:
- Poll SCM: `H/15 * * * *` (every 15 minutes)
- Or use GitHub webhook

### 5. Configure Credentials

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Create new credential:
   - Kind: `SSH Key` or `Username with password`
   - For GitHub access
3. Use in pipeline:

```groovy
withCredentials([usernamePassword(credentialsId: 'github-creds', 
                                   usernameVariable: 'GIT_USER', 
                                   passwordVariable: 'GIT_PASS')]) {
    // Use credentials
}
```

## Pipeline Stages Explained

### Checkout
- Clones source code from Git repository
- Fetches latest commits

### Environment Setup
- Creates Python virtual environment
- Prepares build environment

### Install Dependencies
- Installs Python packages
- Installs Selenium WebDriver
- Installs testing frameworks

### Code Quality Analysis
- Runs Flake8 for style checking
- Runs Pylint for code analysis
- Generates code quality reports

### Database Migration
- Applies pending migrations
- Verifies database schema

### Django Unit Tests
- Runs all Django application tests
- Generates test reports
- Fails build if tests fail

### Selenium Integration Tests
- Starts Django test server
- Runs browser automation tests
- Tests UI workflows
- Can be skipped with parameter

### Build Application
- Collects static files
- Creates deployment artifacts
- Archives build artifacts

### Deploy Simulation
- Creates deployment manifest
- Verifies all components ready
- Generates deployment report

### Documentation Generation
- Creates build report
- Documents test results
- Archives documentation

## Build Parameters

The Jenkinsfile supports parameters:

```groovy
DEPLOYMENT_ENV = 'dev' | 'staging' | 'production'
SKIP_SELENIUM = 'true' | 'false'
```

### Using Parameters

```bash
# Trigger with parameters
curl -X POST http://jenkins:8080/job/MediFlow/buildWithParameters \
  -d "token=YOUR_BUILD_TOKEN" \
  -d "DEPLOYMENT_ENV=staging" \
  -d "SKIP_SELENIUM=false"
```

## Monitoring Jenkins

### View Build Status

```
http://localhost:8080/job/MediFlow/
```

### Real-time Logs

```
http://localhost:8080/job/MediFlow/<BUILD_NUMBER>/console
```

### Blue Ocean UI

```
http://localhost:8080/blue/organizations/jenkins/MediFlow/
```

## Troubleshooting

### Jenkins Not Starting

```bash
# Check logs
sudo journalctl -u jenkins -n 50

# Check Java version
java -version

# Check disk space
df -h
```

### Build Failure

1. Check console output
2. Verify environment variables
3. Check credentials
4. Verify Git repository access
5. Check Python/pip installation

### Permission Issues

```bash
# Add user to Jenkins group
sudo usermod -aG jenkins ubuntu

# Fix directory permissions
sudo chown -R jenkins:jenkins /opt/mediflow
```

## Best Practices

1. **Keep Jenkins updated** - Regular security updates
2. **Backup Jenkins configuration** - Backup /var/lib/jenkins
3. **Monitor disk space** - Clean old builds
4. **Use credentials** - Never hardcode secrets
5. **Enable HTTPS** - Secure Jenkins with SSL
6. **Set resource limits** - Prevent resource hogging
7. **Archive artifacts** - Keep build artifacts
8. **Monitor build times** - Optimize slow stages

## Security

### Disable Anonymous Access

1. Go to **Manage Jenkins** → **Configure Global Security**
2. Uncheck "Allow anonymous read access"
3. Set default role to "authenticated users"

### Enable CSRF Protection

1. Check "Prevent Cross Site Request Forgery exploits"
2. Use HTTPS for all connections

### API Token

Generate API token for programmatic access:
1. Click your username (top right)
2. Click **Configure**
3. Click **Add new Token**
4. Use token for API calls:

```bash
curl -u username:token http://localhost:8080/api/json
```

## Integration

### Email Notifications

Configure email plugin for build notifications:

1. **Manage Jenkins** → **Configure System**
2. Scroll to **E-mail Notification**
3. Set SMTP server: `smtp.gmail.com`
4. Port: `587`
5. Enable TLS
6. Enter credentials

### Slack Integration

1. Install Slack Notification plugin
2. Generate Slack webhook URL
3. Configure in Jenkins:

```groovy
slackSend(
    color: 'good',
    message: "Build succeeded: ${env.BUILD_URL}"
)
```

### GitHub Integration

1. Install GitHub plugin
2. Create GitHub personal access token
3. Add token as Jenkins credential
4. Enable webhook in GitHub repository

---

**Next Steps:**
- Configure pipeline parameters
- Set up webhooks
- Configure notifications
- Run first build

---

For more information, see [Jenkinsfile](../Jenkinsfile)
