from flask import Flask, request, jsonify, session
from flask_cors import CORS
import random
import os

app = Flask(__name__)

# Production secret key (use environment variable in production)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# CORS configuration for Netlify frontend
CORS(app, 
     origins=['http://localhost:5500', 'https://your-netlify-app.netlify.app'],  # Update with your Netlify URL
     supports_credentials=True,
     allow_headers=['Content-Type'],
     methods=['GET', 'POST', 'OPTIONS'])

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))