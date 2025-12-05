# Installation Guide

This guide provides detailed instructions for installing and setting up the MQTT Security Testing Tool.

## System Requirements

### Minimum Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Memory**: 512 MB RAM
- **Storage**: 100 MB free space
- **Network**: Internet connection for package installation

### Recommended Requirements
- **Python**: 3.10 or higher
- **Memory**: 2 GB RAM
- **Storage**: 1 GB free space

## Installation Methods

### Method 1: Standard Installation

#### Step 1: Prepare Environment
```bash
# Update system packages (Linux/macOS)
sudo apt update && sudo apt upgrade  # Ubuntu/Debian
brew update && brew upgrade          # macOS with Homebrew

# Install Python and pip if not already installed
sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian
brew install python3                                # macOS
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/your-username/mqtt-security-tester.git
cd mqtt-security-tester
```

#### Step 3: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 4: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

#### Step 5: Configure Django
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

#### Step 6: Test Installation
```bash
# Run development server
python manage.py runserver

# Open browser to http://127.0.0.1:8000
```

### Method 2: Docker Installation

#### Prerequisites
- Docker installed and running
- Docker Compose (optional)

#### Using Docker
```bash
# Build Docker image
docker build -t mqtt-security-tester .

# Run container
docker run -p 8000:8000 mqtt-security-tester
```

#### Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Method 3: Development Installation

For contributors and developers:

#### Step 1: Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/mqtt-security-tester.git
cd mqtt-security-tester

# Add upstream remote
git remote add upstream https://github.com/original-repo/mqtt-security-tester.git
```

#### Step 2: Install Development Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements-dev.txt
```

#### Step 3: Setup Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3

# MQTT Settings
DEFAULT_MQTT_PORT=1883
DEFAULT_SCAN_DURATION=30

# Security Settings
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
```

### Database Configuration

#### SQLite (Default)
No additional configuration required. Database file will be created automatically.

#### PostgreSQL
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update .env file
DATABASE_URL=postgresql://username:password@localhost:5432/mqtt_security_db
```

#### MySQL
```bash
# Install MySQL adapter
pip install mysqlclient

# Update .env file
DATABASE_URL=mysql://username:password@localhost:3306/mqtt_security_db
```

### Static Files Configuration

#### Development
Static files are served automatically by Django's development server.

#### Production
```bash
# Collect static files
python manage.py collectstatic

# Configure web server to serve static files
# Example for Nginx:
location /static/ {
    alias /path/to/your/project/staticfiles/;
}
```

## Verification

### Test Basic Functionality
```bash
# Run Django tests
python manage.py test

# Check if all URLs are working
python manage.py check

# Validate models
python manage.py validate
```

### Test MQTT Functionality
```bash
# Test MQTT scanner (requires MQTT broker)
python mqtt_security_tester.py localhost --time 10
```

### Performance Test
```bash
# Run with debug toolbar (development only)
pip install django-debug-toolbar

# Add to INSTALLED_APPS in settings.py
# Monitor performance at http://127.0.0.1:8000
```

## Troubleshooting

### Common Installation Issues

#### Python Version Issues
```bash
# Check Python version
python --version
python3 --version

# Use specific Python version
python3.10 -m venv venv
```

#### Permission Issues (Linux/macOS)
```bash
# Fix permission issues
sudo chown -R $USER:$USER /path/to/project
chmod +x manage.py
```

#### Virtual Environment Issues
```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

#### Static Files Issues
```bash
# Create static directory
mkdir -p static

# Update settings.py
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Platform-Specific Issues

#### Windows
```cmd
# Use Windows-style paths
venv\Scripts\activate

# Install Visual C++ Build Tools if needed for some packages
# Download from Microsoft website
```

#### macOS
```bash
# Install Xcode command line tools
xcode-select --install

# Use Homebrew for dependencies
brew install python3 postgresql
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt install python3-dev python3-pip python3-venv
sudo apt install build-essential libpq-dev  # For PostgreSQL
```

## Next Steps

After successful installation:

1. **Read the User Guide**: Check `docs/USER_GUIDE.md`
2. **Review Security Guidelines**: See `docs/SECURITY.md`
3. **Explore Examples**: Look at `examples/` directory
4. **Join Community**: Participate in discussions

## Getting Help

If you encounter issues:

1. **Check Documentation**: Review all files in `docs/`
2. **Search Issues**: Look for similar problems on GitHub
3. **Create Issue**: Report new bugs with detailed information
4. **Community Support**: Ask questions in discussions

## Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

---

**Note**: Always backup your data before updating in production environments.