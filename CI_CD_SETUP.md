# CI/CD Setup Documentation

This project includes a comprehensive GitHub Actions CI/CD pipeline for automated testing, security scanning, and deployment.

## 🚀 Pipeline Overview

The CI/CD pipeline consists of several jobs that run in parallel and sequence:

### 1. **Test Job**

- Runs on every push and pull request
- Sets up PostgreSQL and Redis services
- Installs dependencies and runs Django tests
- Performs Django system checks
- Runs security deployment checks
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
- Runs only after test, lint, and security jobs pass

### 5. **Deploy Production**

- Deploys to production on `main` branch pushes
- Runs only after all checks pass

### 6. **Docker Job**

- Builds and pushes Docker images to Docker Hub
- Tags images with `latest` and commit SHA
- Uses build caching for faster builds

## 🔧 Setup Instructions

### 1. GitHub Secrets Configuration

Add the following secrets to your GitHub repository:

```
Settings → Secrets and variables → Actions → New repository secret
```

**Required Secrets:**

- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_ACCESS_TOKEN`: Docker Hub access token

**Optional Secrets (for deployment):**

- `AWS_ACCESS_KEY_ID`: For AWS deployments
- `AWS_SECRET_ACCESS_KEY`: For AWS deployments
- `HEROKU_API_KEY`: For Heroku deployments
- `SLACK_WEBHOOK_URL`: For deployment notifications

### 2. Branch Configuration

The pipeline is configured for:

- **Main branch**: Production deployments
- **Develop branch**: Staging deployments

Make sure your repository has these branches or update the workflow file accordingly.

### 3. Environment Variables for CI

The pipeline automatically creates a `.env` file for testing with:

- PostgreSQL database configuration
- Redis configuration
- Console email backend
- Test-specific settings

## 🐳 Docker Setup

### Development Environment

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Environment

```bash
# Set environment variables
export DOCKER_HUB_USERNAME=your-username

# Deploy with production compose file
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 📋 Pipeline Triggers

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

## 📊 Monitoring and Notifications

### Artifacts

- Security reports are uploaded as artifacts
- Available for 90 days after workflow run

### Status Badges

Add to your README.md:

```markdown
![Django CI/CD](https://github.com/sparktechagency/nastoc-backend/workflows/Django%20CI/CD/badge.svg)
```

## 🚀 Deployment Strategies

### Current Setup

- **Staging**: Deploys on develop branch (placeholder)
- **Production**: Deploys on main branch (placeholder)

### Recommended Deployment Platforms

#### Heroku

```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.12.12
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: "your-app-name"
    heroku_email: "your-email@example.com"
```

#### AWS ECS

```yaml
- name: Deploy to AWS ECS
  run: |
    aws ecs update-service --cluster your-cluster --service your-service --force-new-deployment
```

#### DigitalOcean App Platform

```yaml
- name: Deploy to DigitalOcean
  uses: digitalocean/app_action@main
  with:
    app_name: your-app-name
    token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
```

## 🔧 Customization

### Adding New Jobs

Add new jobs to `.github/workflows/django.yml`:

```yaml
your-job:
  runs-on: ubuntu-latest
  needs: [test]
  steps:
    - uses: actions/checkout@v4
    - name: Your custom step
      run: echo "Custom logic here"
```

### Environment-Specific Settings

Create environment-specific workflow files:

- `.github/workflows/staging.yml`
- `.github/workflows/production.yml`

### Database Migrations in CI

For automated migrations in production:

```yaml
- name: Run migrations
  run: |
    python manage.py migrate --noinput
```

## 🐛 Troubleshooting

### Common Issues

1. **Test failures**: Check test output in the workflow logs
2. **Docker build fails**: Verify Dockerfile and dependencies
3. **Security scan failures**: Review bandit and safety reports
4. **Deployment failures**: Check deployment secrets and configuration

### Debug Commands

```bash
# Local testing with the same environment
docker run --rm -it python:3.12-slim bash

# Check Django configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell
```

## 📝 Best Practices

1. **Keep secrets secure**: Never commit secrets to code
2. **Test locally**: Run tests and linting locally before pushing
3. **Review changes**: Use pull requests for code review
4. **Monitor workflows**: Regularly check workflow runs for issues
5. **Update dependencies**: Keep GitHub Actions and dependencies updated

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
