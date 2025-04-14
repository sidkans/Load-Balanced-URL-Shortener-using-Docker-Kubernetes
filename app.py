from flask import Flask, request, jsonify, redirect
import redis
import shortuuid
import os
import logging
import time
import validators
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get configuration from environment variables with defaults
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
MAX_RETRIES = int(os.environ.get('REDIS_MAX_RETRIES', 5))
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
SHORT_CODE_LENGTH = int(os.environ.get('SHORT_CODE_LENGTH', 6))

# Redis connection with retry logic
def get_redis_connection():
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            redis_client = redis.StrictRedis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
            # Test the connection
            redis_client.ping()
            logger.info(f"Successfully connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return redis_client
        except redis.ConnectionError as e:
            retry_count += 1
            wait_time = 2 ** retry_count  # Exponential backoff
            logger.warning(f"Redis connection attempt {retry_count} failed. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    logger.error(f"Failed to connect to Redis after {MAX_RETRIES} attempts")
    return None

# Initialize Redis client
redis_client = get_redis_connection()

# Fallback to in-memory storage if Redis is not available
url_mappings = {}
short_codes = {}

def is_redis_available():
    if redis_client is None:
        return False
    try:
        redis_client.ping()
        return True
    except:
        return False

def validate_url(url):
    """Validate if the provided string is a valid URL"""
    if not url:
        return False
    
    # Basic validation using validators library
    if not validators.url(url):
        return False
    
    # Additional checks
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

@app.route('/')
def index():
    return ("The service is working. To use the URL shortener use /shorten along with <BASE_URL>")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes"""
    health_status = {
        "status": "healthy",
        "redis_connected": is_redis_available()
    }
    return jsonify(health_status)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        
        long_url = data.get("long_url")
        
        if not long_url:
            return jsonify({"error": "Missing URL parameter"}), 400
        
        if not validate_url(long_url):
            return jsonify({"error": "Invalid URL format"}), 400
        
        # Check if Redis is available
        redis_available = is_redis_available()
        
        # Check if the URL is already shortened
        if redis_available:
            existing_short_code = redis_client.hget("urls", long_url)
        else:
            existing_short_code = url_mappings.get(long_url)
            
        if existing_short_code:
            short_url = f"{BASE_URL}/{existing_short_code}"
            return jsonify({
                "short_url": short_url, 
                "short_code": existing_short_code,
                "original_url": long_url
            })
        
        # Generate a new short code
        short_code = shortuuid.ShortUUID().random(length=SHORT_CODE_LENGTH)
        
        # Store URL mapping
        if redis_available:
            redis_client.hset("urls", long_url, short_code)
            redis_client.hset("short_codes", short_code, long_url)
            logger.info(f"Stored URL mapping in Redis: {short_code} -> {long_url}")
        else:
            url_mappings[long_url] = short_code
            short_codes[short_code] = long_url
            logger.info(f"Stored URL mapping in memory: {short_code} -> {long_url}")
        
        short_url = f"{BASE_URL}/{short_code}"
        return jsonify({
            "short_url": short_url, 
            "short_code": short_code,
            "original_url": long_url
        })
    except Exception as e:
        logger.error(f"Error in shorten_url: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    try:
        # Check if Redis is available
        redis_available = is_redis_available()
        
        # Get the long URL
        if redis_available:
            long_url = redis_client.hget("short_codes", short_code)
        else:
            long_url = short_codes.get(short_code)
        
        if not long_url:
            return jsonify({"error": "Short URL not found"}), 404
        
        logger.info(f"Redirecting {short_code} to {long_url}")
        return redirect(long_url)
    except Exception as e:
        logger.error(f"Error in redirect_url: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true')


