import requests
import time
import json

# Base URL (change this to your Render URL when deployed)
BASE_URL = "http://127.0.0.1:5000"  # For local testing
# BASE_URL = "https://your-app.onrender.com"  # For Render

def print_response(title, response):
    """Print response nicely"""
    print(f"\n{title}:")
    print(json.dumps(response.json(), indent=2))

def test_bot():
    """Test all endpoints"""
    
    print("="*50)
    print("TESTING YOUTUBE BOT")
    print("="*50)
    
    # 1. Check status
    response = requests.get(f"{BASE_URL}/api/status")
    print_response("Initial Status", response)
    
    # 2. Start bot
    print("\nStarting bot...")
    response = requests.post(f"{BASE_URL}/api/start", json={
        'channel_url': 'https://youtube.com/@TestChannel',
        'target': 5
    })
    print_response("Start Response", response)
    
    # 3. Monitor progress
    for i in range(10):
        time.sleep(3)
        response = requests.get(f"{BASE_URL}/api/status")
        status = response.json()
        print(f"\nProgress: {status['current']}/{status['target']} ({status['percentage']}%)")
        
        if not status['running']:
            break
    
    # 4. Get logs
    response = requests.get(f"{BASE_URL}/api/logs")
    print_response("\nFinal Logs", response)
    
    # 5. Stop bot (if still running)
    response = requests.post(f"{BASE_URL}/api/stop")
    print_response("Stop Response", response)

if __name__ == '__main__':
    test_bot()