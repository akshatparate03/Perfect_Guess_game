from flask import Flask, request, jsonify, session
from flask_cors import CORS
import random
import os

app = Flask(__name__)

# Production secret key
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')

# Session configuration for cross-origin
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# CORS configuration - Allow your Netlify domain
CORS(app, 
     resources={r"/*": {
         "origins": [
             "http://localhost:5500",
             "http://127.0.0.1:5500",
             "https://guessperfectnum.netlify.app",  # Your Netlify URL
             "https://*.netlify.app"  # All Netlify subdomains
         ],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type"],
         "max_age": 3600
     }})

@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'Number Guessing Game API is running!',
        'endpoints': {
            '/start': 'POST - Start new game',
            '/guess': 'POST - Submit a guess'
        }
    })

@app.route('/start', methods=['POST', 'OPTIONS'])
def start_game():
    """Start a new game"""
    if request.method == 'OPTIONS':
        return '', 204
    
    session['number'] = random.randint(1, 100)
    session['guesses'] = 0
    return jsonify({
        'status': 'success',
        'message': 'Game started! Guess a number between 1 and 100'
    })

@app.route('/guess', methods=['POST', 'OPTIONS'])
def guess():
    """Process a guess"""
    if request.method == 'OPTIONS':
        return '', 204
    
    if 'number' not in session:
        return jsonify({
            'status': 'error',
            'message': 'Please start a new game first!'
        })
    
    try:
        guess_num = int(request.json.get('guess'))
        session['guesses'] = session.get('guesses', 0) + 1
        target = session['number']
        
        if guess_num < 1 or guess_num > 100:
            return jsonify({
                'status': 'invalid',
                'message': 'Please enter a number between 1 and 100!'
            })
        
        if guess_num > target:
            return jsonify({
                'status': 'higher',
                'message': 'Lower number please!',
                'guesses': session['guesses']
            })
        elif guess_num < target:
            return jsonify({
                'status': 'lower',
                'message': 'Higher number please!',
                'guesses': session['guesses']
            })
        else:
            guesses = session['guesses']
            session.pop('number', None)
            session.pop('guesses', None)
            return jsonify({
                'status': 'correct',
                'message': f'🎉 Congratulations! You guessed the correct number {target}!',
                'guesses': guesses,
                'number': target
            })
    except (ValueError, TypeError):
        return jsonify({
            'status': 'error',
            'message': 'Please enter a valid number!'
        })

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)