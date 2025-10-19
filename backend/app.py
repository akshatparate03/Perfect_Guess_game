from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
CORS(app, supports_credentials=True)  # Enable CORS for cross-origin requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game"""
    session['number'] = random.randint(1, 100)
    session['guesses'] = 0
    return jsonify({'status': 'success', 'message': 'Game started! Guess a number between 1 and 100'})

@app.route('/guess', methods=['POST'])
def guess():
    """Process a guess"""
    if 'number' not in session:
        return jsonify({'status': 'error', 'message': 'Please start a new game first!'})
    
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
    app.run(debug=True)