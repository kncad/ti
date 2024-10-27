document.getElementById('startButton').addEventListener('click', startGame);

function startGame() {
    document.getElementById('selection').style.display = 'block';
    document.getElementById('startButton').style.display = 'none';
}

function chooseSymbol(symbol) {
    fetch('/set_symbol', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ symbol }) })
        .then(() => {
            document.getElementById('selection').style.display = 'none';
            document.getElementById('coinToss').style.display = 'block';
        });
}

function coinToss(choice) {
    fetch('/toss', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ choice }) })
        .then(response => response.json())
        .then(data => {
            document.getElementById('coinToss').style.display = 'none';
            document.getElementById('board').style.display = 'block';
            initializeBoard(data);
        });
}

function initializeBoard(data) {
    // Populate the board
}

// Handle new game logic, moves, and display transitions for win/lose
