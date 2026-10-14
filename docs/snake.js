// Browser Snake game (docs/snake.js)
// Grid size matches the Python version: 30 columns x 20 rows

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const highScoreEl = document.getElementById('high');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const restartBtn = document.getElementById('restartBtn');

const COLS = 30;
const ROWS = 20;
const CELL_SIZE_X = canvas.width / COLS; // 600/30 = 20
const CELL_SIZE_Y = canvas.height / ROWS; // 400/20 = 20
const GAME_TICK_MS = 120;
const STORAGE_KEY = 'copilot-snake-highscore';

let snake = [];
let dir = { x: 1, y: 0 };
let nextDir = { x: 1, y: 0 };
let food = null;
let score = 0;
let highScore = 0;
let running = false;
let paused = false;
let tickInterval = null;

function loadHighScore() {
  const v = localStorage.getItem(STORAGE_KEY);
  return v ? Number(v) : 0;
}

function saveHighScore(v) {
  localStorage.setItem(STORAGE_KEY, String(v));
}

function resetState() {
  snake = [];
  const midX = Math.floor(COLS / 2);
  const midY = Math.floor(ROWS / 2);
  for (let i = 0; i < 4; i++) {
    snake.push({ x: midX - i, y: midY });
  }
  dir = { x: 1, y: 0 };
  nextDir = { x: 1, y: 0 };
  score = 0;
  scoreEl.textContent = String(score);
  running = true;
  paused = false;
  placeFood();
  updateButtons();
}

function startGame() {
  if (running && !paused) return;
  resetState();
  if (tickInterval) clearInterval(tickInterval);
  tickInterval = setInterval(gameTick, GAME_TICK_MS);
}

function togglePause() {
  if (!running) return;
  paused = !paused;
  updateButtons();
}

function updateButtons() {
  pauseBtn.disabled = !running;
  pauseBtn.textContent = paused ? 'Resume' : 'Pause';
}

function placeFood() {
  const available = [];
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (!snake.some(s => s.x === x && s.y === y)) available.push({ x, y });
    }
  }
  if (available.length === 0) {
    food = null;
    return;
  }
  food = available[Math.floor(Math.random() * available.length)];
}

function gameTick() {
  if (!running || paused) return;
  dir = nextDir; // commit direction
  const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

  // Wall collision
  if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS) {
    endGame();
    return;
  }

  // Self collision
  if (snake.some(s => s.x === head.x && s.y === head.y)) {
    endGame();
    return;
  }

  snake.unshift(head);

  // Food check
  if (food && head.x === food.x && head.y === food.y) {
    score += 1;
    scoreEl.textContent = String(score);
    if (score > highScore) {
      highScore = score;
      highScoreEl.textContent = String(highScore);
      saveHighScore(highScore);
    }
    placeFood();
  } else {
    snake.pop();
  }
}

function endGame() {
  running = false;
  paused = false;
  if (tickInterval) clearInterval(tickInterval);
  updateButtons();
  // show game over text
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 32px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2 - 10);
  ctx.fillStyle = '#7ef29a';
  ctx.font = '18px sans-serif';
  ctx.fillText(`Score: ${score}`, canvas.width / 2, canvas.height / 2 + 18);
}

function draw() {
  // background
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      ctx.fillStyle = (x + y) % 2 === 0 ? '#081018' : '#0d1623';
      ctx.fillRect(x * CELL_SIZE_X, y * CELL_SIZE_Y, CELL_SIZE_X, CELL_SIZE_Y);
    }
  }

  // snake
  for (let i = 0; i < snake.length; i++) {
    const s = snake[i];
    ctx.fillStyle = i === 0 ? '#7ef29a' : '#5ad1ff';
    ctx.fillRect(s.x * CELL_SIZE_X + 2, s.y * CELL_SIZE_Y + 2, CELL_SIZE_X - 4, CELL_SIZE_Y - 4);
  }

  // food
  if (food) {
    ctx.fillStyle = '#ff5d73';
    ctx.fillRect(food.x * CELL_SIZE_X + 4, food.y * CELL_SIZE_Y + 4, CELL_SIZE_X - 8, CELL_SIZE_Y - 8);
  }
}

function loop() {
  draw();
  requestAnimationFrame(loop);
}

function handleKey(e) {
  const key = e.key;
  if (key === 'ArrowUp') {
    if (!(dir.y === 1)) nextDir = { x: 0, y: -1 };
  } else if (key === 'ArrowDown') {
    if (!(dir.y === -1)) nextDir = { x: 0, y: 1 };
  } else if (key === 'ArrowLeft') {
    if (!(dir.x === 1)) nextDir = { x: -1, y: 0 };
  } else if (key === 'ArrowRight') {
    if (!(dir.x === -1)) nextDir = { x: 1, y: 0 };
  } else if (key === ' ') {
    // space pauses/resumes
    e.preventDefault();
    if (running) togglePause();
  }
}

// UI wiring
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', () => { togglePause(); });
restartBtn.addEventListener('click', startGame);

window.addEventListener('keydown', handleKey);

// init
highScore = loadHighScore();
highScoreEl.textContent = String(highScore);
resetState();
loop();
