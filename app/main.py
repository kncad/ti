@app.route('/set_symbol', methods=['POST'])
def set_symbol():
    data = request.json
    game.current_player = data['symbol']
    return '', 204

@app.route('/toss', methods=['POST'])
def toss():
    import random
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
