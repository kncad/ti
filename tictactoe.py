class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Empty board
        self.current_player = 'X'  # X starts the game

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]               # Diagonal
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]  # Return the winner ('X' or 'O')
        return None  # No winner yet

    def is_draw(self):
        return ' ' not in self.board and self.check_winner() is None
