const canvas = document.getElementById('game-board'); // from index.html
const context = canvas.getContext('2d');

const COLS = 10; // usual tetris width
const ROWS = 20; // usual tetris height
const BLOCK_SIZE = 30;

canvas.width = COLS * BLOCK_SIZE;
canvas.height = ROWS * BLOCK_SIZE;

context.fillStyle = 'black';
context.fillRect(0, 0, canvas.width, canvas.height);