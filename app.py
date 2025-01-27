from flask import Flask, request, jsonify
import requests
import ssl
import urllib3
import os

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
        # Get JSON data from the incoming request
        data = request.get_json()
        
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

        # Return the response from the target server
        return response.json()

    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Get port from environment variable (Render will provide this)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Requirements for requirements.txt:
# flask==2.0.1
# requests==2.26.0
# urllib3==1.26.7