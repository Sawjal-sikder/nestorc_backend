# CI/CD Setup Documentation (Without Docker)

This project includes a comprehensive GitHub Actions CI/CD pipeline for automated testing, security scanning, and direct deployment without Docker.

## 🚀 Pipeline Overview

The CI/CD pipeline consists of several jobs that run in parallel and sequence:

### 1. **Test Job**

- Runs on every push and pull request
- Sets up PostgreSQL and Redis services
- Installs dependencies and runs Django tests
- **Migration Fix**: Runs migrations in correct order to handle custom user model dependencies
- Performs Django system checks and security deployment checks
- Collects static files

### 2. **Lint Job**

- Code quality checks using flake8
- Code formatting checks using black
- Import sorting checks using isort

### 3. **Security Job**

- Security vulnerability scanning with bandit
- Dependency vulnerability checks with safety
- Generates security reports as artifacts

### 4. **Deploy Staging**

- Deploys to staging environment on `develop` branch pushes
- Sets up environment variables from GitHub secrets
- Runs migrations and collects static files
- Ready for customization with your deployment commands

### 5. **Deploy Production**

- Deploys to production on `main` branch pushes
- Full environment setup with production secrets
- Database migrations and static file collection
- Production-ready deployment workflow

## 🔧 Setup Instructions

### 1. GitHub Secrets Configuration

Add the following secrets to your GitHub repository:

```
Settings → Secrets and variables → Actions → New repository secret
```

**Required Secrets for Staging:**

- `STAGING_SECRET_KEY`: Django secret key for staging
- `STAGING_ALLOWED_HOSTS`: Comma-separated allowed hosts for staging
- `STAGING_DATABASE_ENGINE`: Database engine (e.g., `django.db.backends.postgresql`)
- `STAGING_DATABASE_NAME`: Staging database name
- `STAGING_DATABASE_USER`: Staging database username
- `STAGING_DATABASE_PASSWORD`: Staging database password
- `STAGING_DATABASE_HOST`: Staging database host
- `STAGING_DATABASE_PORT`: Staging database port

**Required Secrets for Production:**

- `PRODUCTION_SECRET_KEY`: Django secret key for production
- `PRODUCTION_ALLOWED_HOSTS`: Comma-separated allowed hosts for production
- `PRODUCTION_DATABASE_ENGINE`: Database engine
- `PRODUCTION_DATABASE_NAME`: Production database name
- `PRODUCTION_DATABASE_USER`: Production database username
- `PRODUCTION_DATABASE_PASSWORD`: Production database password
- `PRODUCTION_DATABASE_HOST`: Production database host
- `PRODUCTION_DATABASE_PORT`: Production database port
- `PRODUCTION_EMAIL_HOST_USER`: Production email username
- `PRODUCTION_EMAIL_HOST_PASSWORD`: Production email password

**Optional Secrets for VPS Deployment:**

- `VPS_SSH_PRIVATE_KEY`: SSH private key for VPS access
- `VPS_HOST`: VPS server hostname or IP
- `VPS_USER`: SSH username for VPS
- `VPS_PATH`: Path to application on VPS

**Optional Secrets for Heroku Deployment:**

- `HEROKU_API_KEY`: Heroku API key
- `HEROKU_APP_NAME`: Heroku application name
- `HEROKU_EMAIL`: Heroku account email

**Optional Secrets for Notifications:**

- `SLACK_WEBHOOK_URL`: Slack webhook for deployment notifications

### 2. Migration Fix

The pipeline includes a critical fix for Django allauth migration dependencies:

```yaml
# Run migrations in correct order
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate accounts
python manage.py migrate
```

This ensures that the custom user model is created before allauth tries to reference it.

### 3. Branch Configuration

The pipeline is configured for:

- **Main branch**: Production deployments
- **Develop branch**: Staging deployments

## 🚀 Deployment Options

### Option 1: VPS Deployment (Recommended)

Use the `vps-deploy.yml` workflow for deploying to your own VPS:

1. Set up VPS secrets in GitHub
2. Ensure your VPS has:
   - Python virtual environment at `venv/`
   - Gunicorn service configured
   - Nginx service configured
   - Proper file permissions

### Option 2: Heroku Deployment

Use the `heroku-deploy.yml` workflow for Heroku:

1. Set up Heroku secrets in GitHub
2. Configure your Heroku app
3. The workflow will automatically deploy and run migrations

### Option 3: Custom Deployment

Modify the deployment sections in `django.yml`:

```yaml
- name: Deploy to production
  run: |
    echo "Deploying to production environment..."
    # Add your custom deployment commands here
    # Examples:
    # - AWS S3 sync for static files
    # - EC2 deployment via SSH
    # - FTP upload
    # - Custom scripts
```

## 📊 Pipeline Triggers

### Automatic Triggers

- **Push to main**: Runs all jobs + production deployment
- **Push to develop**: Runs all jobs + staging deployment
- **Pull requests**: Runs test, lint, and security jobs only

### Manual Triggers

You can manually trigger workflows from the GitHub Actions tab.

## 🔍 Code Quality Standards

The pipeline enforces:

### Flake8 (PEP 8 Compliance)

- Line length: 127 characters
- Complexity: Maximum 10
- Excludes: migrations, venv, **pycache**

### Black (Code Formatting)

- Automatic code formatting
- Line length: 88 characters (Black default)

### Isort (Import Sorting)

- Alphabetical import sorting
- Django-aware import grouping

## 🛡️ Security Scanning

### Bandit

- Scans for common security issues in Python code
- Generates JSON report as artifact

### Safety

- Checks dependencies for known vulnerabilities
- Generates JSON report as artifact

## 🐛 Troubleshooting

### Common Issues

1. **Migration errors**: The pipeline now handles custom user model dependencies correctly
2. **Static files warnings**: Create `static/` directory in your project root
3. **Test failures**: Check test output in the workflow logs
4. **Security scan failures**: Review bandit and safety reports
5. **Deployment failures**: Check deployment secrets and configuration

### Debug Commands

```bash
# Test migration order locally
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate accounts
python manage.py migrate

# Check Django configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell
```

## 📝 Environment Setup for Local Development

1. **Copy environment file**:

   ```bash
   cp .env.example .env
   ```

2. **Update your .env file** with local development values

3. **Create static directory**:

   ```bash
   mkdir -p static
   ```

4. **Run migrations in order**:
   ```bash
   python manage.py migrate contenttypes
   python manage.py migrate auth
   python manage.py migrate accounts
   python manage.py migrate
   ```

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Custom User Model](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
