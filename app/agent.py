class MDPAgent:
    def __init__(self):
        pass  # No initialization needed for the basic agent

    def choose_action(self, board):
        available_moves = [i for i, x in enumerate(board) if x == ' ']

        best_move = None
        best_value = -float('inf')

        for move in available_moves:
            board[move] = 'O'  # Simulate the AI move
            move_value = self.minimax(board, 0, False)  # Evaluate the move
            board[move] = ' '  # Undo the move

            if move_value > best_value:
                best_value = move_value
                best_move = move

        return best_move

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == 'O':
            return 1  # AI wins
        elif winner == 'X':
            return -1  # Player wins
        elif ' ' not in board:
            return 0  # Draw

        if is_maximizing:
            best_value = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'  # AI move
                    value = self.minimax(board, depth + 1, False)
                    board[i] = ' '  # Undo move
                    best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'  # Player move
                    value = self.minimax(board, depth + 1, True)
                    board[i] = ' '  # Undo move
                    best_value = min(best_value, value)
            return best_value

    def check_winner(self, board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]               # Diagonal
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
                return board[combo[0]]  # Return the winner ('X' or 'O')
        return None  # No winner yet
