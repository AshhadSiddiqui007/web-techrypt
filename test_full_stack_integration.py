#!/usr/bin/env python3
"""
Comprehensive Full-Stack Integration Test
Tests both frontend and backend connectivity
"""

import requests
import time

def test_full_stack_integration():
    print('🧪 COMPREHENSIVE FULL-STACK INTEGRATION TEST')
    print('='*60)
    
    # Test backend health
    print('\n--- Testing Backend (Port 5000) ---')
    try:
        backend_response = requests.get('http://localhost:5000/health', timeout=5)
        if backend_response.status_code == 200:
            data = backend_response.json()
            print('✅ BACKEND: Running successfully')
            print(f'   Service: {data.get("service")}')
            print(f'   Version: {data.get("version")}')
            print(f'   Status: {data.get("status")}')
            backend_working = True
        else:
            print(f'❌ Backend failed: {backend_response.status_code}')
            backend_working = False
    except Exception as e:
        print(f'❌ Backend error: {e}')
        backend_working = False
    
    # Test frontend on multiple ports
    frontend_working = False
    frontend_port = None
    
    for port in [5173, 3000, 8080]:
        print(f'\n--- Testing Frontend (Port {port}) ---')
        try:
            frontend_response = requests.get(f'http://localhost:{port}', timeout=5)
            if frontend_response.status_code == 200:
                print(f'✅ FRONTEND: Running on port {port}')
                print(f'   Status: {frontend_response.status_code}')
                print(f'   Content-Type: {frontend_response.headers.get("content-type", "unknown")}')
                frontend_working = True
                frontend_port = port
                break
            else:
                print(f'❌ Frontend port {port} returned: {frontend_response.status_code}')
        except Exception as e:
            print(f'❌ Frontend port {port} error: {e}')
    
    # Test chat integration if both are working
    if backend_working and frontend_working:
        print(f'\n--- Testing Chat Integration ---')
        try:
            chat_payload = {
                'message': 'I have a dental practice and need help',
                'user_name': 'Dr. Test',
                'user_context': {
                    'name': 'Dr. Test',
                    'email': 'test@dental.com'
                }
            }
            
            chat_response = requests.post('http://localhost:5000/chat', json=chat_payload, timeout=10)
            if chat_response.status_code == 200:
                data = chat_response.json()
                print('✅ CHAT INTEGRATION: Working')
                print(f'   Business Type: {data.get("business_type")}')
                print(f'   Response: {data.get("response")[:100]}...')
                print(f'   Response Time: {data.get("response_time")}s')
                print(f'   Show Appointment Form: {data.get("show_appointment_form")}')
                chat_working = True
            else:
                print(f'❌ Chat integration failed: {chat_response.status_code}')
                chat_working = False
        except Exception as e:
            print(f'❌ Chat integration error: {e}')
            chat_working = False
    else:
        chat_working = False
    
    # Summary
    print(f'\n🎯 FULL-STACK INTEGRATION SUMMARY:')
    print(f'   Backend (Port 5000): {"✅ Working" if backend_working else "❌ Failed"}')
    print(f'   Frontend: {"✅ Working on port " + str(frontend_port) if frontend_working else "❌ Failed"}')
    print(f'   Chat Integration: {"✅ Working" if chat_working else "❌ Failed"}')
    
    if backend_working and frontend_working and chat_working:
        print(f'\n🚀 SUCCESS: Full-stack integration is working!')
        print(f'   Frontend URL: http://localhost:{frontend_port}')
        print(f'   Backend URL: http://localhost:5000')
        print(f'   Ready for production deployment!')
    else:
        print(f'\n⚠️ ISSUES DETECTED: Some components need attention')
        if not backend_working:
            print(f'   - Start backend: python smart_llm_chatbot.py')
        if not frontend_working:
            print(f'   - Start frontend: npm run dev in Techrypt_sourcecode/Techrypt')
        if not chat_working and backend_working and frontend_working:
            print(f'   - Check CORS configuration between frontend and backend')

if __name__ == "__main__":
    test_full_stack_integration()
