document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.getElementById("startButton");
    const selection = document.getElementById("selection");
    const coinToss = document.getElementById("coinToss");
    const board = document.getElementById("board");
    const newGameButton = document.getElementById("newGameButton");

    startButton.addEventListener("click", function() {
        startButton.style.display = "none";  // Hide start button
        selection.style.display = "block";   // Show symbol selection options
    });

    window.chooseSymbol = function(symbol) {
        fetch("/choose_symbol", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol: symbol })
        }).then(response => response.json()).then(data => {
            selection.style.display = "none"; // Hide symbol selection
            coinToss.style.display = "block"; // Show coin toss options
        });
    };

    window.coinToss = function(choice) {
        fetch("/coin_toss", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ choice: choice })
        }).then(response => response.json()).then(data => {
            coinToss.style.display = "none"; // Hide coin toss options
            board.style.display = "block";   // Show the game board

            // Display coin toss result
            alert(`Coin Toss Result: ${data.toss_result}. ${data.user_starts ? "You start!" : "AI starts!"}`);

            // If AI starts, make the first move
            if (!data.user_starts) {
                makeMove(agent.choose_action(game.board)); // Simulate the AI’s first move
            }

            initializeBoard(data.board);
        });
    };

    function initializeBoard(boardData) {
        const grid = document.querySelector(".grid");
        grid.innerHTML = ""; // Clear any previous board data

        // Create 9 cells for the Tic Tac Toe grid
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.addEventListener("click", () => makeMove(i));
            cell.textContent = boardData[i];
            grid.appendChild(cell);
        }
    }

    function makeMove(position) {
        fetch("/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ position: position })
        }).then(response => response.json()).then(data => {
            if (data.winner) {
                showGameResult(data.winner === "X" ? "You Win!" : "You Lose!", data.winner === "X");
            } else if (data.draw) {
                showGameResult("It's a Draw!", false);
            } else {
                updateBoard(data.board);  // Update the board with the new state
            }
        });
    }

    function updateBoard(boardData) {
        const cells = document.querySelectorAll(".cell");
        boardData.forEach((value, index) => {
            cells[index].textContent = value;
        });
    }

    function showGameResult(message, userWon) {
        board.style.display = "none";
        document.body.style.backgroundColor = userWon ? "green" : "red";
        alert(message);  // Or create a custom popup
        newGameButton.style.display = "block";  // Show "New Game" button
    }

    window.newGame = function() {
        fetch("/reset", { method: "POST" }).then(() => {
            document.body.style.backgroundColor = "";  // Reset background color
            board.style.display = "none";
            startButton.style.display = "block";  // Show start button again
            newGameButton.style.display = "none";  // Hide new game button
        });
    };
});
