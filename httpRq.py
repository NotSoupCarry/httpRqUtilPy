import requests
import time
from concurrent.futures import ThreadPoolExecutor
from config import BASE_URL, RQ_PATH, JWT_TOKEN, NUM_REQUESTS, MAX_WORKERS

url = f"{BASE_URL}{RQ_PATH}"

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}

def make_request(i):
    try:
        response = requests.get(url, headers=headers)
        if response.ok: 
            print(f"Request {i+1} OK - Status: {response.status_code}")
            return True
        else:
            print(f"Request {i+1} FAILED - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Request {i+1} FAILED WITH EXCEPTION: {e}")
        return False

start = time.time()

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    results = list(executor.map(make_request, range(NUM_REQUESTS)))

end = time.time()
duration = (end - start) * 1000

percntSuccess = (sum(results) / NUM_REQUESTS) * 100
print(f"\nCompleted {NUM_REQUESTS} requests in {duration:.2f}ms")
print(f"Average: {duration/NUM_REQUESTS:.2f}ms per request")
print(f"Success rate: {sum(results)}/{NUM_REQUESTS} ({percntSuccess:.2f}%)")