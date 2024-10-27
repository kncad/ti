class MDP:
    def __init__(self):
        self.states = [i for i in range(9)]  # Representing the 9 board positions
        self.actions = [i for i in range(9)]  # Possible actions are placing in any of the 9 positions

    def is_terminal(self, board):
        # Check if the board has a winner or is full (draw)
        return self.check_winner(board) is not None or ' ' not in board

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
