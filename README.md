# MQTT Security Testing Tool

A comprehensive Django-based web application for testing MQTT broker security vulnerabilities. This tool is designed for educational purposes and authorized penetration testing.

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd mqtt_security_project
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Django**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

5. **Run the development server**
```bash
python manage.py runserver
```

6. **Access the application**
Open your browser and navigate to `http://127.0.0.1:8000`

## Project Structure

```
mqtt_security_project/
├── mqtt_security_project/     # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Main configuration
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── mqtt_tester/             # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── mqtt_tester/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── session_detail.html
│   │       └── session_results.html
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── urls.py             # App URL patterns
│   ├── views.py            # View functions
│   └── mqtt_scanner.py     # MQTT security scanner logic
├── static/                 # Static files (CSS, JS, images)
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # Project overview
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings Configuration
Key settings in `mqtt_security_project/settings.py`:

- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain/IP addresses
- `DATABASES`: Configure your database
- `STATIC_URL` and `STATICFILES_DIRS`: Static file configuration

## Features

### Core Functionality
- **MQTT Broker Discovery**: Scan and identify MQTT brokers
- **Anonymous Access Testing**: Check for unauthenticated access
- **Topic Discovery**: Find available MQTT topics using wildcards
- **Message Interception**: Monitor and log MQTT messages
- **Injection Testing**: Test message injection capabilities
- **Flood Attack Testing**: Perform DoS testing with message flooding
- **Results Export**: Export scan results in various formats

### Web Interface
- **Dashboard**: Overview of recent scans and quick actions
- **Session Management**: Track and manage scanning sessions
- **Real-time Updates**: Live monitoring of scan progress
- **Test Results**: Detailed vulnerability assessment reports

## Usage

### Starting a New Scan

1. Navigate to the dashboard
2. Click "Start New Scan"
3. Enter target MQTT broker details:
   - Host/IP address
   - Port (default: 1883)
   - Scan duration
4. Configure test parameters
5. Start the scan

### Viewing Results

1. Access active sessions from the dashboard
2. Monitor real-time progress
3. View discovered topics and intercepted messages
4. Run additional security tests
5. Export results for reporting

### Command Line Interface

The tool also includes a standalone CLI version:

```bash
# Basic scan
python mqtt_security_tester.py 192.168.1.100

# Extended scan with injection test
python mqtt_security_tester.py 192.168.1.100 --inject "home/lights/control" --payload "OFF"

# Flood attack test
python mqtt_security_tester.py 192.168.1.100 --flood "test/topic" --count 500
```

## Security Considerations

### Legal and Ethical Use
- **Authorization Required**: Only test systems you own or have explicit permission to test
- **Educational Purpose**: This tool is designed for learning and authorized security assessments
- **Responsible Disclosure**: Report vulnerabilities responsibly to system owners

### Production Deployment
- Change `SECRET_KEY` to a secure random value
- Set `DEBUG = False`
- Use a production database (PostgreSQL, MySQL)
- Configure proper logging
- Implement rate limiting
- Use HTTPS in production

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test mqtt_tester

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage
The project includes tests for:
- Model functionality
- View responses
- MQTT scanner logic
- Template rendering
- URL routing

## API Documentation

### Models

#### ScanSession
Represents an MQTT scanning session.

**Fields:**
- `host`: Target MQTT broker hostname/IP
- `port`: MQTT broker port (default: 1883)
- `created_at`: Session creation timestamp
- `status`: Current session status
- `duration`: Scan duration in seconds

#### DiscoveredTopic
Stores discovered MQTT topics.

**Fields:**
- `session`: Foreign key to ScanSession
- `topic`: MQTT topic string
- `discovered_at`: Discovery timestamp

#### InterceptedMessage
Logs intercepted MQTT messages.

**Fields:**
- `session`: Foreign key to ScanSession
- `topic`: Message topic
- `payload`: Message content
- `timestamp`: Message timestamp

#### TestResult
Records security test results.

**Fields:**
- `session`: Foreign key to ScanSession
- `test_type`: Type of security test
- `success`: Test success status
- `details`: Additional test details
- `timestamp`: Test execution timestamp

### Views

#### Dashboard (`/`)
- Displays recent scan sessions
- Provides quick start options
- Shows system status

#### Start Scan (`/scan/`)
- Form for initiating new scans
- Configuration options
- Validation and error handling

#### Session Detail (`/session/<id>/`)
- Real-time scan progress
- Discovered topics display
- Message interception logs
- Security test controls

#### Session Results (`/session/<id>/results/`)
- Comprehensive test results
- Vulnerability assessment
- Export options

## Troubleshooting

### Common Issues

#### Template Not Found
```
django.template.exceptions.TemplateDoesNotExist
```
**Solution**: Ensure template directories exist:
```bash
mkdir -p mqtt_tester/templates/mqtt_tester
```

#### WSGI Module Not Found
```
ModuleNotFoundError: No module named 'mqtt_security_project.wsgi'
```
**Solution**: Ensure `wsgi.py` exists in the project directory.

#### Static Files Not Loading
**Solution**: 
1. Create static directory: `mkdir -p static`
2. Run: `python manage.py collectstatic`

#### Database Migration Issues
```bash
python manage.py makemigrations mqtt_tester
python manage.py migrate
```

### Debug Mode
Enable detailed error messages by setting `DEBUG = True` in settings.py.

### Logging
Configure logging in settings.py for detailed troubleshooting:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'mqtt_tester': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Commit Messages
Use conventional commit format:
```
feat: add new security test
fix: resolve template loading issue
docs: update installation guide
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and authorized testing purposes only. Users are responsible for ensuring they have proper authorization before testing any systems. The developers are not responsible for any misuse of this tool.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the docs/ directory for detailed guides
- **Community**: Join discussions in the project forums

---

**Important**: Always use this tool responsibly and only on systems you own or have explicit permission to test.