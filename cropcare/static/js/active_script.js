const boardSize = 10;
const player1Pos = document.getElementById('player1Pos');
const player2Pos = document.getElementById('player2Pos');
const currentTurn = document.getElementById('currentTurn');
const diceResult = document.getElementById('diceResult');

let currentPlayer = 1;
let positions = [1, 1];

const snakes = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78,
};

const ladders = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100,
};

document.getElementById('rollDice').addEventListener('click', () => {
    const diceRoll = Math.floor(Math.random() * 6) + 1;
    diceResult.textContent = diceRoll;
    movePlayer(diceRoll);
    checkWin();
    switchTurn();
});

function movePlayer(diceRoll) {
    let currentPosition = positions[currentPlayer - 1];
    currentPosition += diceRoll;

    if (currentPosition > 100) {
        currentPosition = 100;
    }

    if (snakes[currentPosition]) {
        currentPosition = snakes[currentPosition];
    } else if (ladders[currentPosition]) {
        currentPosition = ladders[currentPosition];
    }

    positions[currentPlayer - 1] = currentPosition;

    if (currentPlayer === 1) {
        player1Pos.textContent = currentPosition;
    } else {
        player2Pos.textContent = currentPosition;
    }

    updateBoard();
}

function updateBoard() {
    document.querySelectorAll('.player1').forEach(el => el.remove());
    document.querySelectorAll('.player2').forEach(el => el.remove());

    const player1Cell = document.querySelector(`#cell-${positions[0]}`);
    const player1Symbol = document.createElement('div');
    player1Symbol.classList.add('player1');
    player1Symbol.textContent = '🦜';
    player1Cell.appendChild(player1Symbol);

    const player2Cell = document.querySelector(`#cell-${positions[1]}`);
    const player2Symbol = document.createElement('div');
    player2Symbol.classList.add('player2');
    player2Symbol.textContent = '🕊️';
    player2Cell.appendChild(player2Symbol);
}

function checkWin() {
    if (positions[currentPlayer - 1] >= 100) {
        alert(`Player ${currentPlayer} wins! 😁🎇🎆🎁🎀💫`);
        resetGame();
    }
}

function switchTurn() {
    currentPlayer = currentPlayer === 1 ? 2 : 1;
    currentTurn.textContent = `Player ${currentPlayer}`;
}

function resetGame() {
    positions = [1, 1];
    player1Pos.textContent = 1;
    player2Pos.textContent = 1;
    currentPlayer = 1;
    currentTurn.textContent = 'Player 1';
    diceResult.textContent = 0;
    updateBoard();
}

const gameBoard = document.getElementById('gameBoard');
for (let i = 100; i > 0; i--) {
    const cell = document.createElement('div');
    cell.id = `cell-${i}`;
    cell.textContent = i;

    if (snakes[i]) {
        cell.classList.add('snake');
        const snakeSymbol = document.createElement('p');
        snakeSymbol.classList.add('symbol');
        snakeSymbol.textContent = '🐍';
        cell.appendChild(snakeSymbol);
    } else if (ladders[i]) {
        cell.classList.add('ladder');
        const ladderSymbol = document.createElement('p');
        ladderSymbol.classList.add('symbol');
        ladderSymbol.textContent = '🪜';
        cell.appendChild(ladderSymbol);
    }

    gameBoard.appendChild(cell);
}
updateBoard();
