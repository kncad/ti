import random
from flask import Flask, jsonify, request, render_template
from tictactoe import TicTacToe
from agent import MDPAgent

app = Flask(__name__)
game = TicTacToe()
agent = MDPAgent()

@app.route("/")
def index():
    return render_template("index.html", board=game.board)

@app.route("/choose_symbol", methods=["POST"])
def choose_symbol():
    data = request.json
    game.current_player = data["symbol"]
    return jsonify(success=True)

@app.route("/coin_toss", methods=["POST"])
def coin_toss():
    data = request.json
    user_choice = data["choice"].lower()

    # Perform the coin toss
    toss_result = random.choice(["heads", "tails"])
    
    # Check if the user won the toss
    user_starts = user_choice == toss_result

    # Set who goes first based on the coin toss result
    if user_starts:
        game.current_player = 'X'  # User starts
    else:
        game.current_player = 'O'  # AI starts
    
    return jsonify({
        "toss_result": toss_result,
        "user_starts": user_starts,
        "board": game.board,
        "current_player": game.current_player
    })

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    position = data["position"]

    # Make the player's move
    if game.make_move(position):
        if game.current_player == 'O':
            ai_position = agent.choose_action(game.board)
            game.make_move(ai_position)

    winner = game.check_winner()
    is_draw = game.is_draw()

    return jsonify({
        'board': game.board,
        'winner': winner,
        'draw': is_draw,
        'next_player': game.current_player
    })

@app.route("/reset", methods=["POST"])
def reset():
    game.reset()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
