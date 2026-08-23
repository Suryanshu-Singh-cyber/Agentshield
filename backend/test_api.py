# backend/test_api.py
import requests
import sys

BASE_URL = 'http://127.0.0.1:8000'

def test_health():
    try:
        resp = requests.get(f'{BASE_URL}/health', timeout=5)
        if resp.status_code == 200:
            print('✅ Health check passed')
            return True
        else:
            print(f'❌ Health check failed: {resp.status_code}')
            return False
    except Exception as e:
        print(f'❌ Health check error: {e}')
        return False

def test_generate():
    try:
        resp = requests.post(f'{BASE_URL}/generate-tests', json={'count': 5}, timeout=10)
        if resp.status_code == 200:
            print('✅ Generate tests passed')
            return True
        else:
            print(f'❌ Generate tests failed: {resp.status_code}')
            return False
    except Exception as e:
        print(f'❌ Generate tests error: {e}')
        return False

def test_run():
    try:
        resp = requests.post(f'{BASE_URL}/run-tests', timeout=30)
        if resp.status_code == 200:
            print('✅ Run tests passed')
            return True
        else:
            print(f'❌ Run tests failed: {resp.status_code}')
            return False
    except Exception as e:
        print(f'❌ Run tests error: {e}')
        return False

if __name__ == '__main__':
    print('🚀 Running AgentShield API tests...')
    print('=' * 40)
    
    passed = True
    passed &= test_health()
    passed &= test_generate()
    passed &= test_run()
    
    print('=' * 40)
    if passed:
        print('✅ All tests passed!')
        sys.exit(0)
    else:
        print('❌ Some tests failed')
        sys.exit(1)
