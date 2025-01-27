from flask import Flask, request, jsonify
import requests
import ssl
import urllib3
import json

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create Flask app
app = Flask(__name__)

# Create a custom SSL context that doesn't verify certificates
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

TARGET_URL = 'https://157.245.100.93:3001/send-otp'

@app.route('/forward-otp', methods=['POST'])
def forward_otp():
    try:
        # Print the raw request data for debugging
        print("Received request data:", request.get_data())
        
        # Explicitly parse JSON data
        if not request.is_json:
            print("Request is not JSON")
            return jsonify({
                'error': 'Request must be JSON'
            }), 400
            
        data = request.get_json()
        print("Parsed JSON data:", data)
        
        # Validate required fields
        if not data or 'phoneNumber' not in data or 'otp' not in data:
            return jsonify({
                'error': 'Missing required fields. Please provide phoneNumber and otp.'
            }), 400

        # Forward the request to the target URL
        response = requests.post(
            TARGET_URL,
            json=data,
            verify=False,
            headers={'Content-Type': 'application/json'}
        )
        
        print("Target response:", response.text)
        return response.json()

    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))
        return jsonify({
            'error': f'Invalid JSON format: {str(e)}'
        }), 400
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)