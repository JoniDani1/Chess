# ♟️ PyChess AI: A Multithreaded Chess Engine

A high-performance Chess AI written in pure Python. It features a custom Minimax engine with Alpha-Beta pruning, running on a separate thread to ensure a responsive 60 FPS user interface.

![Chess Gameplay](https://private-user-images.githubusercontent.com/100622677/545260667-b351dbee-855d-498e-95dc-1b64424c81fd.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzAyNDM4MzMsIm5iZiI6MTc3MDI0MzUzMywicGF0aCI6Ii8xMDA2MjI2NzcvNTQ1MjYwNjY3LWIzNTFkYmVlLTg1NWQtNDk4ZS05NWRjLTFiNjQ0MjRjODFmZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMjA0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDIwNFQyMjE4NTNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lMjZiNWRmZTdkNzUxMmJkMGMxZjA3NDNlODQ0OTFhMjI1MTA2N2U2YmNjNTViMDMxZTgwZGMzNzExODIwZDk0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.v55zAkfoS-aKOilPkz6hBKfz6S6i3eQTJuavwCVgPsM)



## 🚀 Key Features

### 🧠 The Intelligence (`ai.py`)
* **Minimax Algorithm:** Recursively evaluates future board states to find the optimal move.
* **Alpha-Beta Pruning:** Optimizes the search tree by ignoring "bad" branches, increasing efficiency by ~10x.
* **Move Ordering (MVV-LVA):** Prioritizes capturing high-value pieces with low-value pieces to find "killer moves" faster.
* **Dynamic Depth:** Automatically scales difficulty (Depth 4 in opening → Depth 5 in endgame) to balance speed and accuracy.
* **Positional Heuristics:** Uses Piece-Square Tables to understand that a Knight in the center is better than a Knight on the edge.

### ⚡ Engineering & Performance
* **Multithreading:** The AI runs in a background daemon thread using `threading` and `queue`. This prevents the UI from freezing/locking up during deep calculations.
* **State Management:** Implements `copy.deepcopy` to prevent "State Bleeding" (visual glitches) between the rendering thread and the calculation thread.
* **Type Safety:** Fully type-hinted codebase for robustness and maintainability.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/chess-ai.git](https://github.com/YOUR_USERNAME/chess-ai.git)
    cd chess-ai
    ```

2.  **Install Dependencies**
    This project requires `pygame`.
    ```bash
    pip install pygame
    ```

3.  **Run the Game**
    ```bash
    python main.py
    ```

## 🎮 Controls
* **Mouse:** Click and drag (or click-click) to move pieces.
* **Z Key:** Undo the last move.
* **Space Bar:** Reset the game (only when Game Over).

## 📂 Project Structure

* `main.py`: The entry point. Handles the Event Loop, Threading, and Rendering.
* `engine.py`: The "Model". Validates moves, handles castling/promotion logic, and stores the board state.
* `ai.py`: The "Brain". Contains the Minimax recursion and evaluation functions.
* `settings.py`: Configuration (Colors, Screen Size, FPS).
* `components.py`: Helper classes for UI (Buttons, Sound Manager).

## 🔮 Future Improvements
* **Transposition Tables:** Implement Zobrist Hashing to cache board states and speed up calculations.
* **WebAssembly Port:** Optimize the threading model to run in the browser using `pygbag`.
* **Opening Book:** Add a database of standard opening moves to play instantly in the early game.

---
*Built with Python 3 and Pygame.*
