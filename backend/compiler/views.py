import json
import os
import subprocess
import tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import re

def detect_language(code):
    if re.search(r'import\s+java\.', code):
        return 'java'
    elif re.search(r'#include\s*<iostream>', code):
        return 'cpp'
    elif re.search(r'def\s+\w+|print\s*\(', code):
        return 'python'
    return 'undetected'

@csrf_exempt
@require_http_methods(["POST"])
def detect_language_view(request):
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = detect_language(code)
        return JsonResponse({'language': language})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def run_code_view(request):
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', '')
        
        if language == 'python':
            result = run_python(code)
        elif language == 'cpp':
            result = run_cpp(code)
        elif language == 'java':
            result = run_java(code)
        else:
            return JsonResponse({'error': 'Unsupported language'}, status=400)
        
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def ai_debug_view(request):
    return JsonResponse({'message': 'AI debugging feature coming soon'})

def run_python(code):
    try:
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return {'output': result.stdout}
        return {'error': result.stderr}
    except subprocess.TimeoutExpired:
        return {'error': 'Execution timed out'}
    except Exception as e:
        return {'error': str(e)}

def run_cpp(code):
    with tempfile.TemporaryDirectory() as tmp_dir:
        cpp_file = os.path.join(tmp_dir, 'temp.cpp')
        output_file = os.path.join(tmp_dir, 'output')
        
        with open(cpp_file, 'w') as f:
            f.write(code)
        
        try:
            # Compile
            compile_result = subprocess.run(
                ['g++', cpp_file, '-o', output_file],
                capture_output=True,
                text=True
            )
            if compile_result.returncode != 0:
                return {'error': f'Compilation error:\n{compile_result.stderr}'}
            
            # Run
            run_result = subprocess.run(
                [output_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            if run_result.returncode == 0:
                return {'output': run_result.stdout}
            return {'error': run_result.stderr}
        except subprocess.TimeoutExpired:
            return {'error': 'Execution timed out'}
        except Exception as e:
            return {'error': str(e)}

def run_java(code):
    with tempfile.TemporaryDirectory() as tmp_dir:
        java_file = os.path.join(tmp_dir, 'Main.java')
        
        with open(java_file, 'w') as f:
            f.write(code)
        
        try:
            # Compile
            compile_result = subprocess.run(
                ['javac', java_file],
                capture_output=True,
                text=True
            )
            if compile_result.returncode != 0:
                return {'error': f'Compilation error:\n{compile_result.stderr}'}
            
            # Run
            run_result = subprocess.run(
                ['java', '-cp', tmp_dir, 'Main'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if run_result.returncode == 0:
                return {'output': run_result.stdout}
            return {'error': run_result.stderr}
        except subprocess.TimeoutExpired:
            return {'error': 'Execution timed out'}
        except Exception as e:
            return {'error': str(e)}
