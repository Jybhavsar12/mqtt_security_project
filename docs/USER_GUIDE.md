# User Guide

Complete guide for using the MQTT Security Testing Tool effectively and safely.

## Getting Started

### First Launch

1. **Start the Application**
```bash
python manage.py runserver
```

2. **Access the Dashboard**
Open your browser and navigate to `http://127.0.0.1:8000`

3. **Familiarize with Interface**
- Dashboard: Overview of recent scans
- Navigation: Easy access to all features
- Legal Notice: Important usage guidelines

### Understanding the Interface

#### Dashboard Components
- **Quick Start**: Begin new security scans
- **Recent Sessions**: View past scanning activities
- **System Status**: Monitor application health
- **Legal Notice**: Reminder of responsible use

## Core Features

### 1. MQTT Broker Discovery

#### Starting a Basic Scan
1. Click "Start New Scan" from dashboard
2. Enter target information:
   - **Host**: IP address or hostname (e.g., `192.168.1.100`)
   - **Port**: MQTT port (default: `1883`)
   - **Duration**: Scan time in seconds (default: `30`)
3. Click "Start Scan"

#### Scan Parameters
- **Host**: Target MQTT broker
  - IP addresses: `192.168.1.100`, `10.0.0.50`
  - Hostnames: `mqtt.example.com`, `iot-broker.local`
- **Port**: Common MQTT ports
  - `1883`: Standard MQTT
  - `8883`: MQTT over SSL/TLS
  - `8080`: MQTT over WebSocket
- **Duration**: Recommended ranges
  - Quick scan: `10-30` seconds
  - Thorough scan: `60-300` seconds

### 2. Anonymous Access Testing

The tool automatically tests for:
- **Unauthenticated connections**
- **Default credentials**
- **Weak authentication**

#### Results Interpretation
- ✅ **Success**: Anonymous access possible (vulnerability)
- ❌ **Failed**: Authentication required (secure)
- ⚠️ **Partial**: Limited access detected

### 3. Topic Discovery

#### How It Works
- Uses MQTT wildcards (`#`, `+`)
- Subscribes to common topic patterns
- Monitors for active topics

#### Common Topic Patterns
```
home/+/+          # Home automation
device/+/status   # Device status
sensor/+/data     # Sensor data
$SYS/#           # System topics
```

#### Viewing Discovered Topics
1. Navigate to active scan session
2. View "Discovered Topics" section
3. Topics appear in real-time during scan

### 4. Message Interception

#### Real-time Monitoring
- Automatically captures messages on discovered topics
- Displays message content and metadata
- Logs timestamps for analysis

#### Message Information
- **Topic**: MQTT topic path
- **Payload**: Message content
- **Timestamp**: When message was received
- **QoS**: Quality of Service level

### 5. Security Testing

#### Injection Testing
Test ability to publish malicious messages:

1. **Navigate to Session Detail**
2. **Use Injection Test Panel**:
   - Enter target topic
   - Specify test payload
   - Click "Test Injection"

**Example Scenarios**:
```
Topic: home/lights/control
Payload: {"state": "off", "brightness": 0}

Topic: device/update
Payload: {"firmware": "malicious.bin"}
```

#### Flood Attack Testing
Test broker resilience against DoS attacks:

1. **Configure Flood Parameters**:
   - Target topic
   - Message count (start with 100)
2. **Monitor Broker Response**
3. **Analyze Results**

**Caution**: Start with low message counts to avoid overwhelming the broker.

### 6. Results Analysis

#### Session Results Page
Access comprehensive test results:
- **Test Summary**: Overview of all tests performed
- **Vulnerability Assessment**: Security findings
- **Recommendations**: Suggested improvements

#### Result Categories
- **Critical**: Immediate security risks
- **High**: Significant vulnerabilities
- **Medium**: Moderate security concerns
- **Low**: Minor issues or recommendations
- **Info**: Informational findings

## Advanced Usage

### Custom Test Scenarios

#### IoT Device Testing
```
Target: 192.168.1.50:1883
Topics to test:
- device/+/command
- sensor/+/config
- system/update
```

#### Home Automation Testing
```
Target: home-assistant.local:1883
Topics to test:
- homeassistant/+/+
- home/+/set
- zigbee2mqtt/+
```

### Batch Testing
Test multiple brokers systematically:

1. Create list of targets
2. Run sequential scans
3. Compare results across brokers
4. Generate consolidated report

### Integration with Other Tools

#### Export Results
- JSON format for programmatic analysis
- CSV for spreadsheet analysis
- PDF reports for documentation

#### API Integration
Use Django's REST framework for automation:
```python
import requests

# Start scan via API
response = requests.post('http://localhost:8000/api/scan/', {
    'host': '192.168.1.100',
    'port': 1883,
    'duration': 60
})
```

## Best Practices

### Pre-Testing Checklist
- [ ] Verify authorization to test target
- [ ] Document test scope and objectives
- [ ] Prepare incident response plan
- [ ] Set up monitoring for test impact

### During Testing
- **Start Small**: Begin with short scans
- **Monitor Impact**: Watch for service disruption
- **Document Findings**: Record all observations
- **Respect Limits**: Don't overwhelm target systems

### Post-Testing
- **Analyze Results**: Review all findings thoroughly
- **Verify Vulnerabilities**: Confirm findings are accurate
- **Report Responsibly**: Follow disclosure guidelines
- **Clean Up**: Remove any test data created

## Safety Guidelines

### Authorized Testing Only
- **Own Systems**: Test only systems you own
- **Written Permission**: Get explicit authorization
- **Scope Definition**: Clearly define test boundaries
- **Legal Compliance**: Follow local laws and regulations

### Technical Precautions
- **Network Isolation**: Use isolated test networks when possible
- **Backup Systems**: Ensure target systems are backed up
- **Monitoring**: Monitor system health during tests
- **Rollback Plan**: Have procedures to undo changes

### Ethical Considerations
- **Responsible Disclosure**: Report vulnerabilities appropriately
- **Minimize Impact**: Avoid disrupting production systems
- **Data Protection**: Handle discovered data responsibly
- **Professional Conduct**: Maintain ethical standards

## Troubleshooting

### Common Issues

#### Connection Failures
**Symptoms**: Cannot connect to MQTT broker
**Solutions**:
- Verify host and port are correct
- Check network connectivity
- Confirm broker is running
- Test with MQTT client tools

#### No Topics Discovered
**Symptoms**: Scan completes but finds no topics
**Solutions**:
- Increase scan duration
- Try different topic patterns
- Check if broker requires authentication
- Verify broker has active publishers

#### Slow Performance
**Symptoms**: Scans take longer than expected
**Solutions**:
- Reduce scan duration
- Limit concurrent connections
- Check network latency
- Monitor system resources

### Error Messages

#### "Permission Denied"
- Check user permissions
- Verify network access
- Confirm firewall settings

#### "Template Not Found"
- Ensure template files exist
- Check Django configuration
- Verify app installation

#### "Database Error"
- Run database migrations
- Check database permissions
- Verify database configuration

## Getting Help

### Documentation Resources
- **Installation Guide**: Setup instructions
- **API Reference**: Technical documentation
- **Security Guide**: Safety guidelines
- **FAQ**: Common questions and answers

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Wiki**: Community-contributed guides
- **Examples**: Sample configurations and use cases

### Professional Support
For enterprise users:
- **Training**: Comprehensive security testing training
- **Consulting**: Custom implementation assistance
- **Support**: Priority technical support
- **Compliance**: Regulatory compliance guidance

---

**Remember**: This tool is powerful and should be used responsibly. Always ensure you have proper authorization before testing any systems.