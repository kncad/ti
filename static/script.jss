// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startButton');
    const selectionDiv = document.getElementById('selection');
    const coinTossDiv = document.getElementById('coinToss');
    const boardElement = document.getElementById('board');
    const newGameButton = document.getElementById('newGameButton');
    const gridCells = document.querySelectorAll('.cell');

    // Start the game: show symbol selection
    window.startGame = () => {
        startButton.style.display = 'none';
        selectionDiv.style.display = 'block';
    };

    // Choose player symbol (X or O)
    window.chooseSymbol = async (symbol) => {
        await fetch('/set_symbol', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol })
        });
        selectionDiv.style.display = 'none';
        coinTossDiv.style.display = 'block';
    };

    // Perform coin toss to decide who starts
    window.coinToss = async (choice) => {
        const response = await fetch('/toss', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ choice })
        });
        const data = await response.json();

        coinTossDiv.style.display = 'none';
        boardElement.style.display = 'block';
        renderBoard(data.board);

        if (data.first_player === 'O') {
            aiMove(); // AI makes the first move if it won the toss
        }
    };

    // Render the board based on the state from the server
    function renderBoard(board) {
        gridCells.forEach((cell, index) => {
            cell.textContent = board[index];
            cell.classList.toggle('disabled', board[index] !== ' ');
        });
    }

    // Player makes a move by clicking a cell
    boardElement.addEventListener('click', async (event) => {
        const cell = event.target;
        if (!cell.classList.contains('cell') || cell.classList.contains('disabled')) return;

        const position = cell.dataset.index;

        // Send player's move to the server
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ position: parseInt(position) })
        });
        const data = await response.json();

        renderBoard(data.board); // Update board with latest state

        // Check for game end conditions
        if (data.winner) {
            endGame(data.winner === 'X' ? 'You win!' : 'You lose!', data.winner);
        } else if (data.draw) {
            endGame('It\'s a draw!');
        } else if (data.next_player === 'O') {
            aiMove(); // AI move if game isn't over
        }
    });

    // AI makes a move and updates the board
    async function aiMove() {
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ position: null })
        });
        const data = await response.json();
        
        renderBoard(data.board);

        // Check if AI won or if it's a draw
        if (data.winner) {
            endGame(data.winner === 'X' ? 'You win!' : 'You lose!', data.winner);
        } else if (data.draw) {
            endGame('It\'s a draw!');
        }
    }

    // Reset the game for a new round
    window.newGame = async () => {
        await fetch('/reset', { method: 'POST' });
        boardElement.style.display = 'none';
        newGameButton.style.display = 'none';
        startButton.style.display = 'block';
        renderBoard([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']); // Clear board
    };

    // Display end game message
    function endGame(message, winner = null) {
        alert(message); // Simple alert; replace with a custom UI if needed
        newGameButton.style.display = 'block';
    }
});
