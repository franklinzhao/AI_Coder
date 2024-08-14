const readline = require('readline');

// The game board
let board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];

// Function to display the board
function displayBoard() {
    console.log(` ${board[0]} | ${board[1]} | ${board[2]}`);
    console.log(`--+---+--`);
    console.log(` ${board[3]} | ${board[4]} | ${board[5]}`);
    console.log(`--+---+--`);
    console.log(` ${board[6]} | ${board[7]} | ${board[8]}`);
}

// Function to insert an element at a given position
function insertBoard(position, element) {
    if (board[position] === ' ') {
        board[position] = element;
        return true;
    }
    return false;
}

// Function to check if the board is full
function isBoardFull() {
    return !board.includes(' ');
}

// Function to check for a win
function isWinner(player) {
    const winConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  // Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  // Columns
        [0, 4, 8], [2, 4, 6]  // Diagonals
    ];

    for (let condition of winConditions) {
        if (board[condition[0]] === player &&
            board[condition[1]] === player &&
            board[condition[2]] === player) {
            return true;
        }
    }
    return false;
}

// Function to handle player move
function playerMove() {
    return new Promise(resolve => {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        rl.question("Enter your move (1-9): ", (move) => {
            const position = parseInt(move) - 1;

            if (position < 0 || position >= 9 || !insertBoard(position, 'X')) {
                console.log("Invalid move. Please enter a valid position.");
                rl.close();
                resolve(playerMove());
            } else {
                rl.close();
                resolve();
            }
        });
    });
}

// Minimax algorithm to choose the best move
function minimax(isMaximizing) {
    if (isWinner('O')) {
        return 1;
    } else if (isWinner('X')) {
        return -1;
    } else if (isBoardFull()) {
        return 0;
    }

    if (isMaximizing) {
        let bestScore = -Infinity;
        for (let i = 0; i < 9; i++) {
            if (board[i] === ' ') {
                board[i] = 'O';
                const score = minimax(false);
                board[i] = ' ';
                bestScore = Math.max(score, bestScore);
            }
        }
        return bestScore;
    } else {
        let bestScore = Infinity;
        for (let i = 0; i < 9; i++) {
            if (board[i] === ' ') {
                board[i] = 'X';
                const score = minimax(true);
                board[i] = ' ';
                bestScore = Math.min(score, bestScore);
            }
        }
        return bestScore;
    }
}

// Function to handle computer move with strategy
function computerMove() {
    let bestMove;
    let bestScore = -Infinity;

    for (let i = 0; i < 9; i++) {
        if (board[i] === ' ') {
            board[i] = 'O';
            const score = minimax(false);
            board[i] = ' ';
            if (score > bestScore) {
                bestScore = score;
                bestMove = i;
            }
        }
    }

    if (bestMove !== undefined) {
        insertBoard(bestMove, 'O');
    }
}

// Main game loop
async function main() {
    while (true) {
        displayBoard();

        // Player move
        await playerMove();

        // Check if player has won
        if (isWinner('X')) {
            displayBoard();
            console.log("You win!");
            break;
        }

        // Check if the board is full
        if (isBoardFull()) {
            displayBoard();
            console.log("It's a tie!");
            break;
        }

        // Computer move
        computerMove();

        // Check if computer has won
        if (isWinner('O')) {
            displayBoard();
            console.log("Computer wins!");
            break;
        }

        // Check if the board is full
        if (isBoardFull()) {
            displayBoard();
            console.log("It's a tie!");
            break;
        }
    }
}

// Run the game
main();
