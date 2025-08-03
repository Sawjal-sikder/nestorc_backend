# Django CI/CD Pipeline Documentation

This repository includes a comprehensive GitHub Actions CI/CD pipeline for Django applications **without Docker**. The pipeline provides automated testing, security scanning, code quality checks, and deployment to various platforms.

## 🚀 Pipeline Overview

### Workflows Included

1. **`ci-cd.yml`** - Main CI/CD pipeline
2. **`deploy-vps.yml`** - VPS deployment via SSH
3. **`deploy-heroku.yml`** - Heroku deployment
4. **`deploy-aws.yml`** - AWS Elastic Beanstalk deployment

### Main Pipeline Jobs

#### 1. **Test Job** 🧪

- Runs on every push and pull request
- Sets up PostgreSQL and Redis services
- Installs Python dependencies
- **Handles Django allauth migration dependencies correctly**
- Runs Django tests, system checks, and security checks
- Collects static files

#### 2. **Lint Job** 📝

- **Flake8**: PEP 8 compliance checking
- **Black**: Code formatting validation
- **Isort**: Import statement sorting

#### 3. **Security Job** 🛡️

- **Bandit**: Python security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- Uploads security reports as artifacts

#### 4. **Deploy Staging** 🚀

- Deploys to staging on `develop` branch pushes
- Creates staging environment configuration
- Runs migrations and collects static files

#### 5. **Deploy Production** 🎯

- Deploys to production on `main` branch pushes
- Full production environment setup
- Comprehensive deployment preparation

## 🔧 Setup Instructions

### 1. Required GitHub Secrets

Add these secrets in your repository settings: `Settings → Secrets and variables → Actions`

#### Core Secrets (Required for all deployments)

```
# Staging Environment
STAGING_SECRET_KEY                 # Django secret key for staging
STAGING_ALLOWED_HOSTS             # Comma-separated allowed hosts
STAGING_DATABASE_ENGINE           # e.g., django.db.backends.postgresql
STAGING_DATABASE_NAME             # Staging database name
STAGING_DATABASE_USER             # Staging database username
STAGING_DATABASE_PASSWORD         # Staging database password
STAGING_DATABASE_HOST             # Staging database host
STAGING_DATABASE_PORT             # Staging database port
STAGING_EMAIL_HOST_USER           # Staging email username
STAGING_EMAIL_HOST_PASSWORD       # Staging email password

# Production Environment
PRODUCTION_SECRET_KEY             # Django secret key for production
PRODUCTION_ALLOWED_HOSTS          # Comma-separated allowed hosts
PRODUCTION_DATABASE_ENGINE        # Database engine
PRODUCTION_DATABASE_NAME          # Production database name
PRODUCTION_DATABASE_USER          # Production database username
PRODUCTION_DATABASE_PASSWORD      # Production database password
PRODUCTION_DATABASE_HOST          # Production database host
PRODUCTION_DATABASE_PORT          # Production database port
PRODUCTION_EMAIL_HOST_USER        # Production email username
PRODUCTION_EMAIL_HOST_PASSWORD    # Production email password
GOOGLE_CLIENT_ID                  # Google OAuth client ID
GOOGLE_CLIENT_SECRET              # Google OAuth client secret
```

#### VPS Deployment Secrets (Optional)

```
VPS_SSH_PRIVATE_KEY               # SSH private key for VPS access
VPS_HOST                          # VPS server hostname or IP address
VPS_USER                          # SSH username for VPS
VPS_APP_PATH                      # Full path to application on VPS
VPS_URL                           # VPS application URL for health checks
```

#### Heroku Deployment Secrets (Optional)

```
HEROKU_API_KEY                    # Heroku API key
HEROKU_APP_NAME                   # Heroku application name
HEROKU_EMAIL                      # Heroku account email
```

#### AWS Deployment Secrets (Optional)

```
AWS_ACCESS_KEY_ID                 # AWS access key ID
AWS_SECRET_ACCESS_KEY             # AWS secret access key
AWS_REGION                        # AWS region (e.g., us-east-1)
AWS_S3_BUCKET                     # S3 bucket for deployment packages
AWS_EB_APPLICATION                # Elastic Beanstalk application name
AWS_EB_ENVIRONMENT                # Elastic Beanstalk environment name
```

#### Notification Secrets (Optional)

```
SLACK_WEBHOOK_URL                 # Slack webhook for notifications
```

### 2. Django Migration Fix

The pipeline includes a **critical fix** for Django allauth migration dependencies:

```bash
# Migrations are run in this specific order:
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate accounts      # Custom user model
python manage.py migrate              # All remaining migrations
```

This prevents the `relation "accounts_customuser" does not exist` error.

### 3. Branch Configuration

- **`main` branch**: Triggers production deployment
- **`develop` branch**: Triggers staging deployment
- **Pull requests**: Run tests, linting, and security scans only

## 🚀 Deployment Options

### Option 1: VPS Deployment (Recommended)

Perfect for deploying to your own VPS/server.

**Requirements:**

- SSH access to your VPS
- Python virtual environment set up at `{VPS_APP_PATH}/venv/`
- Gunicorn and Nginx configured as systemd services
- Git repository cloned on the server

**Features:**

- Automatic backup before deployment
- Zero-downtime deployment
- Service restart (Gunicorn, Nginx, Celery)
- Deployment verification

### Option 2: Heroku Deployment

Easy deployment to Heroku with automatic migration handling.

**Features:**

- Uses official Heroku GitHub Action
- Runs migrations in correct order
- Collects static files
- Deployment verification

### Option 3: AWS Elastic Beanstalk

Enterprise-grade deployment to AWS.

**Features:**

- Creates deployment packages
- Uploads to S3
- Deploys to Elastic Beanstalk
- Handles application versioning

### Option 4: Custom Deployment

Customize the deployment sections in `ci-cd.yml` for your specific needs:

```yaml
- name: Deploy to production server
  run: |
    echo "🚀 Deploying to production environment..."
    # Add your custom deployment commands:
    # - rsync to server
    # - SCP files
    # - API calls
    # - Database updates
    # - Service restarts
```

## 📊 Pipeline Triggers

### Automatic Triggers

- **Push to `main`**: Full pipeline + production deployment
- **Push to `develop`**: Full pipeline + staging deployment
- **Pull requests**: Tests, linting, and security scans only

### Manual Triggers

- Navigate to `Actions` tab in GitHub
- Select workflow and click "Run workflow"

## 🔍 Code Quality Standards

### Flake8 Configuration

```bash
# Line length: 127 characters
# Max complexity: 10
# Excludes: migrations, venv, __pycache__
flake8 . --max-line-length=127 --max-complexity=10
```

### Black Configuration

```bash
# Line length: 88 characters (default)
# Automatic code formatting
black --check --diff .
```

### Isort Configuration

```bash
# Django-aware import sorting
# Alphabetical ordering
isort --check-only --diff .
```

## 🛡️ Security Features

### Bandit Security Scanning

- Scans for common Python security issues
- Generates detailed JSON reports
- Flags potential vulnerabilities

### Safety Dependency Scanning

- Checks dependencies against known vulnerability databases
- Identifies outdated packages with security issues
- Provides recommendations for updates

### Reports

- Security reports are uploaded as GitHub artifacts
- Available for 30 days after workflow completion
- Download from the Actions tab

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Migration Errors

```bash
# Problem: relation "accounts_customuser" does not exist
# Solution: Pipeline now handles this automatically with correct migration order
```

#### Static Files Warning

```bash
# Problem: STATICFILES_DIRS directory does not exist
# Solution: Pipeline creates static/ directory automatically
```

#### Test Failures

```bash
# Check the test job output in GitHub Actions
# Run tests locally: python manage.py test
```

#### Deployment Failures

```bash
# Check deployment job logs
# Verify all required secrets are configured
# Test SSH access manually for VPS deployments
```

### Local Development Setup

1. **Create static directory**:

   ```bash
   mkdir -p static
   ```

2. **Run migrations in correct order**:

   ```bash
   python manage.py migrate contenttypes
   python manage.py migrate auth
   python manage.py migrate accounts
   python manage.py migrate
   ```

3. **Test the application**:
   ```bash
   python manage.py test
   python manage.py check --deploy
   ```

## 📝 Customization

### Adding Custom Jobs

Add new jobs to `ci-cd.yml`:

```yaml
custom-job:
  runs-on: ubuntu-latest
  needs: [test]
  steps:
    - uses: actions/checkout@v4
    - name: Custom step
      run: echo "Add your custom logic here"
```

### Environment-Specific Workflows

Create separate workflow files for different environments:

- `.github/workflows/staging.yml`
- `.github/workflows/production.yml`

### Notification Integration

Add Slack notifications:

```yaml
- name: Notify deployment
  run: |
    curl -X POST -H 'Content-type: application/json' \
      --data '{"text":"🚀 Deployment successful!"}' \
      ${{ secrets.SLACK_WEBHOOK_URL }}
```

## 🔗 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
- [Django Custom User Model Best Practices](https://docs.djangoproject.com/en/stable/topics/auth/customizing/)

## 📊 Status Badges

Add to your README.md:

```markdown
![Django CI/CD](https://github.com/sparktechagency/nastoc-backend/workflows/Django%20CI/CD%20Pipeline/badge.svg)
```

---

## 🎯 Quick Start

1. **Configure secrets** in your GitHub repository
2. **Push to develop** to test staging deployment
3. **Create pull request** to main for production deployment
4. **Monitor workflows** in the Actions tab
5. **Customize deployment** commands for your infrastructure

The pipeline is designed to be **zero-configuration** for testing and easily customizable for your specific deployment needs!
