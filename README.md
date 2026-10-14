# Copilot_snakeGame

A simple Snake game implemented in Python (tkinter) and a browser-playable version.

Live demo (when GitHub Pages is enabled):

https://Demo-For-Test.github.io/Copilot_snakeGame/

---

## Play in the browser

This repository contains a web version of the game in the `docs/` folder. GitHub Pages can serve content from `docs/` on the default branch.

Files:
- docs/index.html — the web UI and canvas
- docs/style.css — styling
- docs/snake.js — game logic (JavaScript) with high score saved in localStorage

To run locally:

1. In the repository root run a simple HTTP server (Python 3):

```bash
python -m http.server 8000
```

2. Open your browser at:

```
http://localhost:8000/docs/
```

Controls:
- Arrow keys: move the snake
- Space: pause/resume
- Start / Pause / Restart buttons available on the page

Notes:
- The web version stores the high score in your browser's localStorage.
- The demo URL above will work once you enable GitHub Pages for this repository (Settings → Pages → Branch: `main` → Folder: `/docs`).

---

## Python (tkinter) version

There is also a native Python version using Tkinter:

- `snake_game.py` — plays locally using the Tkinter window

Run with:

```bash
python snake_game.py
```

Controls:
- Arrow keys: move the snake
- P: pause/resume
- Space: restart after game over
- Enter: start from title screen

The Python version saves a high score in `highscore.txt` in the repo directory (created on first run).

---

## Assets & License

This project is provided as-is. Feel free to use and modify it. If you'd like, I can add a license file (MIT/Apache/BSD) — tell me which license you prefer and I'll add it.
