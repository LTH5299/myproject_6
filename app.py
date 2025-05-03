from flask import Flask
import logging
import prometheus_client
from prometheus_client import Counter, Histogram
import time
import random

app = Flask(__name__)

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Khởi tạo metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

@app.route('/metrics')
def metrics():
    return prometheus_client.generate_latest()

@app.route('/')
def home():
    logger.info('Home page accessed')
    REQUEST_COUNT.inc()
    
    start_time = time.time()
    time.sleep(random.uniform(0.1, 0.3))
    REQUEST_LATENCY.observe(time.time() - start_time)
    
    return 'Hello Monitoring!'

@app.route('/error')
def error():
    logger.error('Simulated error occurred')
    return 'Error Page', 500

if __name__ == '__main__':
    prometheus_client.start_http_server(8000)
    app.run(host='0.0.0.0', port=5000)
