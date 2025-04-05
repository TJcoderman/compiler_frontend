from django.urls import path
from django.http import JsonResponse
from . import views

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to the Code Compiler API',
        'endpoints': {
            'detect_language': '/api/detect-language/',
            'run_code': '/api/run-code/',
            'ai_debug': '/api/ai-debug/'
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),  # Add this line
    path('detect-language/', views.detect_language_view, name='detect_language'),
    path('run-code/', views.run_code_view, name='run_code'),
    path('ai-debug/', views.ai_debug_view, name='ai_debug'),
]
