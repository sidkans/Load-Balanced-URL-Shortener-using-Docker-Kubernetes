from flask import Flask, request, jsonify, redirect
import redis
import shortuuid

app = Flask(__name__)

# Commented out Redis configuration for now
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Temporary in-memory key-value stores
# url_mappings = {}
# short_codes = {}

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get("long_url")

    if not long_url:
        return jsonify({"error": "Missing URL"}), 400

    # Check if the URL is already shortened
    existing_short_code = redis_client.hget("urls", long_url)
    # existing_short_code = url_mappings.get(long_url)
    if existing_short_code:
        short_url = f"http://localhost:5000/{existing_short_code}"
        return jsonify({"short_url": short_url, "short_code": existing_short_code})

    # Generate a new short code
    short_code = shortuuid.ShortUUID().random(length=6)

    # Store URL mapping in temporary dictionaries
    redis_client.hset("urls", long_url, short_code)
    redis_client.hset("short_codes", short_code, long_url)
    # url_mappings[long_url] = short_code
    # short_codes[short_code] = long_url

    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({"short_url": short_url, "short_code": short_code})

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    long_url = redis_client.hget("short_codes", short_code)
    # long_url = short_codes.get(short_code)

    if not long_url:
        return jsonify({"error": "Short URL not found"}), 404

    return redirect(long_url)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
