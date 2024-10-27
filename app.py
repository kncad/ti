# app/app.py
from flask import Flask, jsonify, request, render_template
from app.tictactoe import TicTacToe  # Importing TicTacToe class
from app.agentimport MDPAgent       # Importing MDPAgent class
import random

app = Flask(__name__)

# Initialize the game and the AI agent
game = TicTacToe()
agent = MDPAgent()

@app.route('/')
def index():
    return render_template('index.html', board=game.board, current_player=game.current_player)

@app.route('/set_symbol', methods=['POST'])
def set_symbol():
    """Sets the symbol for the player and AI."""
    data = request.json
    game.current_player = data['symbol']  # Set player's chosen symbol as the starting player
    return '', 204

@app.route('/toss', methods=['POST'])
def toss():
    """Simulates a coin toss to decide who plays first."""
    data = request.json
    user_choice = data['choice']
    toss_result = random.choice(['heads', 'tails'])
    first_player = game.current_player if user_choice == toss_result else 'O'
    game.current_player = first_player
    return jsonify({
        'toss_result': toss_result,
        'first_player': first_player,
        'board': game.board
    })

@app.route('/move', methods=['POST'])
def move():
    """Handles a player's move, followed by the AI's response if it's the AI's turn."""
    data = request.json
    position = data['position']

    # Make the move for the human player
    if game.make_move(position):
        # AI's turn if the game isn't over
        if game.current_player == 'O':
            ai_move = agent.choose_action(game.board)
            game.make_move(ai_move)

    # Check the game status
    winner = game.check_winner()
    is_draw = game.is_draw()

    return jsonify({
        'board': game.board,
        'winner': winner,
        'draw': is_draw,
        'next_player': game.current_player  # Send the next player
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Resets the game to start a new round."""
    game.reset()
    return jsonify({
        'board': game.board
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
