from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import threading
from .models import ScanSession, DiscoveredTopic, InterceptedMessage, TestResult
from .mqtt_scanner import MQTTSecurityScanner

def index(request):
    recent_sessions = ScanSession.objects.order_by('-created_at')[:10]
    return render(request, 'mqtt_tester/index.html', {
        'recent_sessions': recent_sessions
    })

def start_scan(request):
    if request.method == 'POST':
        host = request.POST.get('host')
        port = int(request.POST.get('port', 1883))
        duration = int(request.POST.get('duration', 30))
        
        # Create scan session
        session = ScanSession.objects.create(
            host=host,
            port=port,
            duration=duration
        )
        
        # Start scan in background thread
        scanner = MQTTSecurityScanner(session)
        thread = threading.Thread(target=scanner.run_scan)
        thread.daemon = True
        thread.start()
        
        messages.success(request, f'Scan started for {host}:{port}')
        return redirect('mqtt_tester:session_detail', session_id=session.id)
    
    return render(request, 'mqtt_tester/start_scan.html')

def session_detail(request, session_id):
    session = get_object_or_404(ScanSession, id=session_id)
    topics = DiscoveredTopic.objects.filter(session=session)
    recent_messages = InterceptedMessage.objects.filter(session=session).order_by('-timestamp')[:20]
    
    return render(request, 'mqtt_tester/session_detail.html', {
        'session': session,
        'topics': topics,
        'recent_messages': recent_messages
    })

def session_results(request, session_id):
    session = get_object_or_404(ScanSession, id=session_id)
    test_results = TestResult.objects.filter(session=session).order_by('-timestamp')
    
    return render(request, 'mqtt_tester/session_results.html', {
        'session': session,
        'test_results': test_results
    })

@csrf_exempt
def inject_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        topic = data.get('topic')
        payload = data.get('payload')
        
        session = get_object_or_404(ScanSession, id=session_id)
        scanner = MQTTSecurityScanner(session)
        
        success = scanner.test_injection(topic, payload)
        
        TestResult.objects.create(
            session=session,
            test_type='injection',
            target_topic=topic,
            payload=payload,
            success=success,
            details=f"Injection test on {topic}"
        )
        
        return JsonResponse({'success': success})
    
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def flood_attack(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        topic = data.get('topic')
        count = int(data.get('count', 100))
        
        session = get_object_or_404(ScanSession, id=session_id)
        scanner = MQTTSecurityScanner(session)
        
        success = scanner.flood_attack(topic, count)
        
        TestResult.objects.create(
            session=session,
            test_type='flood',
            target_topic=topic,
            success=success,
            details=f"Flood attack with {count} messages"
        )
        
        return JsonResponse({'success': success})
    
    return JsonResponse({'error': 'Invalid request'})