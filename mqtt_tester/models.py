from django.db import models
from django.utils import timezone

class ScanSession(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=1883)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='running')
    duration = models.IntegerField(default=30)
    
    def __str__(self):
        return f"{self.host}:{self.port} - {self.created_at}"

class DiscoveredTopic(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    discovered_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['session', 'topic']

class InterceptedMessage(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    payload = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.topic}: {self.payload[:50]}"

class TestResult(models.Model):
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=50)
    target_topic = models.CharField(max_length=500, blank=True)
    payload = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)