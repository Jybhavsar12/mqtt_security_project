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