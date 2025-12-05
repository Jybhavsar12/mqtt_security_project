# API Reference

Complete reference for the MQTT Security Testing Tool's models, views, and functions.

## Models

### ScanSession

Represents an MQTT security scanning session.

```python
class ScanSession(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=1883)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='running')
    duration = models.IntegerField(default=30)
```

**Fields:**
- `host` (CharField): Target MQTT broker hostname or IP address
- `port` (IntegerField): MQTT broker port number (default: 1883)
- `created_at` (DateTimeField): Session creation timestamp
- `status` (CharField): Current session status ('running', 'completed', 'failed')
- `duration` (IntegerField): Scan duration in seconds

**Methods:**
- `__str__()`: Returns string representation of session
- `get_absolute_url()`: Returns URL for session detail view

**Usage Example:**
```python
from mqtt_tester.models import ScanSession

# Create new session
session = ScanSession.objects.create(
    host='192.168.1.100',
    port=1883,
    duration=60
)

# Query sessions
recent_sessions = ScanSession.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=7)
)
```

### DiscoveredTopic

Stores MQTT topics discovered during scanning.

```python
class DiscoveredTopic(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    discovered_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['session', 'topic']
```

**Fields:**
- `session` (ForeignKey): Reference to parent ScanSession
- `topic` (CharField): MQTT topic string
- `discovered_at` (DateTimeField): Discovery timestamp

**Constraints:**
- Unique together: session and topic (prevents duplicates)

**Usage Example:**
```python
from mqtt_tester.models import DiscoveredTopic

# Add discovered topic
topic = DiscoveredTopic.objects.create(
    session=session,
    topic='home/sensors/temperature'
)

# Get topics for session
topics = DiscoveredTopic.objects.filter(session=session)
```

### InterceptedMessage

Logs MQTT messages intercepted during scanning.

```python
class InterceptedMessage(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    payload = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    qos = models.IntegerField(default=0)
```

**Fields:**
- `session` (ForeignKey): Reference to parent ScanSession
- `topic` (CharField): MQTT topic of intercepted message
- `payload` (TextField): Message payload content
- `timestamp` (DateTimeField): Message interception timestamp
- `qos` (IntegerField): Quality of Service level

**Usage Example:**
```python
from mqtt_tester.models import InterceptedMessage

# Log intercepted message
message = InterceptedMessage.objects.create(
    session=session,
    topic='sensor/data',
    payload='{"temperature": 23.5, "humidity": 45}',
    qos=1
)

# Get recent messages
recent_messages = InterceptedMessage.objects.filter(
    session=session
).order_by('-timestamp')[:10]
```

### TestResult

Records results of security tests performed.

```python
class TestResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=50)
    target_topic = models.CharField(max_length=500, blank=True)
    success = models.BooleanField()
    details = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
```

**Fields:**
- `session` (ForeignKey): Reference to parent ScanSession
- `test_type` (CharField): Type of test performed
- `target_topic` (CharField): Target topic for test (optional)
- `success` (BooleanField): Whether test was successful
- `details` (TextField): Detailed test results
- `timestamp` (DateTimeField): Test execution timestamp

**Test Types:**
- `'anonymous_access'`: Anonymous connection test
- `'topic_discovery'`: Topic enumeration test
- `'message_injection'`: Message injection test
- `'flood_attack'`: DoS flood test

**Usage Example:**
```python
from mqtt_tester.models import TestResult

# Record test result
result = TestResult.objects.create(
    session=session,
    test_type='message_injection',
    target_topic='home/lights/control',
    success=True,
    details='Successfully injected test message'
)
```

## Views

### index(request)

Dashboard view displaying recent sessions and quick start options.

**URL Pattern:** `/`
**Template:** `mqtt_tester/index.html`
**Context Variables:**
- `recent_sessions`: QuerySet of recent ScanSession objects

**Usage:**
```python
def index(request):
    recent_sessions = ScanSession.objects.order_by('-created_at')[:10]
    return render(request, 'mqtt_tester/index.html', {
        'recent_sessions': recent_sessions
    })
```

### start_scan(request)

Handles scan initiation form and creates new scanning sessions.

**URL Pattern:** `/scan/`
**Methods:** GET, POST
**Template:** `mqtt_tester/start_scan.html`

**GET Request:**
- Displays scan configuration form

**POST Request:**
- Validates form data
- Creates new ScanSession
- Initiates background scanning
- Redirects to session detail

**Form Fields:**
- `host`: Target hostname/IP (required)
- `port`: MQTT port (default: 1883)
- `duration`: Scan duration in seconds (default: 30)

**Usage:**
```python
def start_scan(request):
    if request.method == 'POST':
        # Process form data
        host = request.POST.get('host')
        port = int(request.POST.get('port', 1883))
        duration = int(request.POST.get('duration', 30))
        
        # Create session
        session = ScanSession.objects.create(
            host=host,
            port=port,
            duration=duration
        )
        
        # Start background scan
        start_mqtt_scan(session)
        
        return redirect('mqtt_tester:session_detail', session_id=session.id)
    
    return render(request, 'mqtt_tester/start_scan.html')
```

### session_detail(request, session_id)

Displays detailed information about a scanning session.

**URL Pattern:** `/session/<int:session_id>/`
**Template:** `mqtt_tester/session_detail.html`
**Context Variables:**
- `session`: ScanSession object
- `topics`: QuerySet of DiscoveredTopic objects
- `recent_messages`: QuerySet of recent InterceptedMessage objects

**Features:**
- Real-time scan progress
- Discovered topics display
- Message interception logs
- Security test controls

### session_results(request, session_id)

Shows comprehensive test results for a session.

**URL Pattern:** `/session/<int:session_id>/results/`
**Template:** `mqtt_tester/session_results.html`
**Context Variables:**
- `session`: ScanSession object
- `test_results`: QuerySet of TestResult objects

### inject_message(request)

API endpoint for message injection testing.

**URL Pattern:** `/inject/`
**Method:** POST
**Content-Type:** application/json
**CSRF:** Exempt

**Request Body:**
```json
{
    "session_id": 1,
    "topic": "home/lights/control",
    "payload": "OFF"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Injection test completed"
}
```

### flood_attack(request)

API endpoint for flood attack testing.

**URL Pattern:** `/flood/`
**Method:** POST
**Content-Type:** application/json
**CSRF:** Exempt

**Request Body:**
```json
{
    "session_id": 1,
    "topic": "test/flood",
    "count": 100
}
```

**Response:**
```json
{
    "success": true,
    "message": "Flood attack completed",
    "messages_sent": 100
}
```

## MQTT Scanner Module

### MQTTSecurityScanner

Core class for MQTT security testing functionality.

```python
class MQTTSecurityScanner:
    def __init__(self, host, port=1883, timeout=30):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = mqtt.Client()
```

**Methods:**

#### test_anonymous_access()
Tests if broker allows anonymous connections.

**Returns:** `bool` - True if anonymous access is allowed

```python
scanner = MQTTSecurityScanner('192.168.1.100')
if scanner.test_anonymous_access():
    print("Vulnerability: Anonymous access allowed")
```

#### discover_topics(duration=30)
Discovers active MQTT topics using wildcard subscriptions.

**Parameters:**
- `duration` (int): Discovery time in seconds

**Returns:** `list` - List of discovered topic strings

```python
topics = scanner.discover_topics(duration=60)
for topic in topics:
    print(f"Discovered: {topic}")
```

#### intercept_messages(topics, duration=30)
Intercepts messages on specified topics.

**Parameters:**
- `topics` (list): List of topics to monitor
- `duration` (int): Monitoring time in seconds

**Returns:** `list` - List of intercepted message dictionaries

```python
messages = scanner.intercept_messages(['home/+/+'], duration=30)
for msg in messages:
    print(f"{msg['topic']}: {msg['payload']}")
```

#### inject_message(topic, payload)
Attempts to inject a message into specified topic.

**Parameters:**
- `topic` (str): Target topic
- `payload` (str): Message payload

**Returns:** `bool` - True if injection successful

```python
success = scanner.inject_message('home/lights/control', 'OFF')
if success:
    print("Message injection successful")
```

#### flood_attack(topic, count=100)
Performs flood attack on specified topic.

**Parameters:**
- `topic` (str): Target topic
- `count` (int): Number of messages to send

**Returns:** `dict` - Attack results with success count

```python
result = scanner.flood_attack('test/flood', count=500)
print(f"Sent {result['sent']} of {result['total']} messages")
```

## URL Patterns

### App URLs (mqtt_tester/urls.py)

```python
from django.urls import path
from . import views

app_name = 'mqtt_tester'

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/', views.start_scan, name='start_scan'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('session/<int:session_id>/results/', views.session_results, name='session_results'),
    path('inject/', views.inject_message, name='inject_message'),
    path('flood/', views.flood_attack, name='flood_attack'),
]
```

### Root URLs (mqtt_security_project/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mqtt_tester.urls')),
]
```

## Template Tags and Filters

### Custom Template Tags

#### scan_status
Displays formatted scan status with appropriate styling.

**Usage:**
```html
{% load mqtt_tags %}
{% scan_status session.status %}
```

#### vulnerability_badge
Shows vulnerability severity badge.

**Usage:**
```html
{% vulnerability_badge result.severity %}
```

### Custom Template Filters

#### truncate_payload
Truncates long message payloads for display.

**Usage:**
```html
{{ message.payload|truncate_payload:50 }}
```

## JavaScript API

### Frontend JavaScript Functions

#### testInjection()
Performs AJAX request for message injection testing.

```javascript
function testInjection() {
    const topic = document.getElementById('inject-topic').value;
    const payload = document.getElementById('inject-payload').value;
    
    fetch('/inject/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_id: sessionId,
            topic: topic,
            payload: payload
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Injection test completed successfully');
        }
    });
}
```

#### testFlood()
Performs AJAX request for flood attack testing.

```javascript
function testFlood() {
    const topic = document.getElementById('flood-topic').value;
    const count = document.getElementById('flood-count').value;
    
    fetch('/flood/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_id: sessionId,
            topic: topic,
            count: parseInt(count)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Flood attack completed: ${data.messages_sent} messages sent`);
        }
    });
}
```

## Error Handling

### Common Exceptions

#### MQTTConnectionError
Raised when unable to connect to MQTT broker.

```python
try:
    scanner = MQTTSecurityScanner('192.168.1.100')
    scanner.test_anonymous_access()
except MQTTConnectionError as e:
    print(f"Connection failed: {e}")
```

#### InvalidTopicError
Raised when topic format is invalid.

```python
try:
    scanner.inject_message('invalid/topic/+', 'test')
except InvalidTopicError as e:
    print(f"Invalid topic: {e}")
```

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Session or resource not found
- `500 Internal Server Error`: Server error during processing

---

This API reference provides comprehensive documentation for developers working with the MQTT Security Testing Tool. For additional examples and use cases, see the `examples/` directory in the project repository.