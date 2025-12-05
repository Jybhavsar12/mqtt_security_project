#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import threading
import time
import argparse
import json
from datetime import datetime

class MQTTSecurityTester:
    def __init__(self, host, port=1883):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        self.discovered_topics = set()
        self.messages = []
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[+] Connected to {self.host}:{self.port}")
        else:
            print(f"[-] Connection failed: {rc}")
    
    def on_message(self, client, userdata, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        topic = msg.topic
        payload = msg.payload.decode('utf-8', errors='ignore')
        
        self.discovered_topics.add(topic)
        self.messages.append({
            'timestamp': timestamp,
            'topic': topic,
            'payload': payload
        })
        
        print(f"[{timestamp}] {topic}: {payload}")
    
    def test_anonymous_access(self):
        """Test if broker allows anonymous connections"""
        print("\n[*] Testing anonymous access...")
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[-] Anonymous access failed: {e}")
            return False
    
    def discover_topics(self, duration=30):
        """Discover topics using wildcard subscriptions"""
        print(f"\n[*] Discovering topics for {duration} seconds...")
        self.client.on_message = self.on_message
        
        # Subscribe to all topics
        wildcards = ['#', '+/+', '+/+/+', '$SYS/#']
        for wildcard in wildcards:
            self.client.subscribe(wildcard)
            print(f"[+] Subscribed to: {wildcard}")
        
        time.sleep(duration)
        print(f"\n[+] Discovered {len(self.discovered_topics)} unique topics")
        return list(self.discovered_topics)
    
    def test_injection(self, target_topic, payload):
        """Test message injection to specific topic"""
        print(f"\n[*] Testing injection on topic: {target_topic}")
        try:
            self.client.publish(target_topic, payload)
            print(f"[+] Payload sent: {payload}")
        except Exception as e:
            print(f"[-] Injection failed: {e}")
    
    def flood_attack(self, topic, count=100):
        """Perform message flooding attack"""
        print(f"\n[*] Flooding topic '{topic}' with {count} messages...")
        for i in range(count):
            payload = f"flood_message_{i}_{time.time()}"
            self.client.publish(topic, payload)
            time.sleep(0.01)  # Small delay to avoid overwhelming
        print(f"[+] Sent {count} flood messages")
    
    def brute_force_topics(self, wordlist):
        """Brute force common topic names"""
        print(f"\n[*] Brute forcing topics...")
        common_topics = [
            'admin', 'config', 'status', 'control', 'command',
            'sensor', 'device', 'home', 'temperature', 'light',
            'door', 'camera', 'alarm', 'system', 'debug'
        ]
        
        for topic in common_topics:
            test_topics = [
                topic,
                f"{topic}/status",
                f"{topic}/config",
                f"home/{topic}",
                f"device/{topic}",
                f"{topic}/command"
            ]
            
            for test_topic in test_topics:
                self.client.subscribe(test_topic)
                time.sleep(0.1)
    
    def save_results(self, filename="mqtt_scan_results.json"):
        """Save discovered data to file"""
        results = {
            'target': f"{self.host}:{self.port}",
            'timestamp': datetime.now().isoformat(),
            'topics': list(self.discovered_topics),
            'messages': self.messages[-50:]  # Last 50 messages
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="MQTT Security Testing Tool")
    parser.add_argument("host", help="Target MQTT broker IP/hostname")
    parser.add_argument("-p", "--port", type=int, default=1883, help="MQTT port (default: 1883)")
    parser.add_argument("-t", "--time", type=int, default=30, help="Discovery time in seconds")
    parser.add_argument("--inject", help="Topic for injection testing")
    parser.add_argument("--payload", default="SECURITY_TEST", help="Injection payload")
    parser.add_argument("--flood", help="Topic to flood")
    parser.add_argument("--count", type=int, default=100, help="Flood message count")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("MQTT Security Testing Tool")
    print("For Educational Purposes Only")
    print("=" * 50)
    
    tester = MQTTSecurityTester(args.host, args.port)
    
    # Test anonymous access
    if not tester.test_anonymous_access():
        print("[-] Cannot proceed without connection")
        return
    
    # Discover topics
    topics = tester.discover_topics(args.time)
    
    # Brute force common topics
    tester.brute_force_topics([])
    
    # Injection test if specified
    if args.inject:
        tester.test_injection(args.inject, args.payload)
    
    # Flood test if specified
    if args.flood:
        tester.flood_attack(args.flood, args.count)
    
    # Save results
    tester.save_results()
    
    print("\n[*] Testing completed")

if __name__ == "__main__":
    main()