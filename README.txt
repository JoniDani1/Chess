PROJECT: Pygame Chess Implementation
STUDENT: JONI DANI
MODULE: Programming


=============================================================================
1. PROJECT DESCRIPTION
=============================================================================
This is a comprehensive 2-Player Chess game developed in Python using the Pygame 
library. It implements standard chess rules including piece movement, capturing, 
check detection, and special moves like Pawn Promotion. 

Unlike a basic board display, this project includes a complete game loop with 
menus, timers, sound effects, and visual move validation.

=============================================================================
2. HOW TO RUN THE GAME
=============================================================================
Requirements:
- Python 3.x
- Pygame library (Install via: pip install pygame)

Installation & Execution:
1. Unzip the submission folder.
2. Ensure the following structure exists:
   /ProjectFolder
      |-- main.py
      |-- /images          (Contains .png files for all pieces)
      |-- move.wav
      |-- capture.wav
      |-- notify.wav
3. Open a terminal/command prompt in this folder.
4. Run the command:
   python main.py

=============================================================================
3. IMPLEMENTED FEATURES & CUSTOM CLASSES
=============================================================================
Per the assignment requirements, I have implemented several custom classes to 
handle game complexity and state management:

A. Class SoundManager (New Functionality)
   - Handles the loading and playback of audio cues (move, capture, check notification).
   - Includes error handling: If a .wav file is missing, the game generates 
     a silent buffer to prevent crashing.

B. Class Timer (New Functionality)
   - Implements a Blitz-style countdown timer (10 minutes per player).
   - Handles time-delta calculations and updates the game state to "Game Over" 
     if a player's clock hits 00:00.

C. Class ChessPiece
   - Encapsulates piece data (color, type, movement status).
   - Manages sprite loading with a fallback system: if an image fails to load, 
     it generates a placeholder graphic so the game remains playable.

D. Class Button
   - Created for the Main Menu interface.
   - Handles collision detection for mouse clicks and hover effects 
     (changing color when the mouse is over the button).

=============================================================================
4. GAMEPLAY CONTROLS
=============================================================================
- MOUSE: Left-click to select a piece. Valid moves will be highlighted in green.
         Click a highlighted square to move.
- PROMOTION: When a pawn reaches the opposite side, a clickable menu appears 
             to select the promotion piece (Queen, Rook, Knight, Bishop).
- SPACEBAR: Resets the game after a Checkmate, Stalemate, or Timeout.

=============================================================================
5. ASSETS & CREDITS
=============================================================================
- Logic: Implemented using standard Chess rules and Pygame event handling.
- Images: Chess piece sprites located in the /images directory.
- Audio: Custom sound effects for user feedback.
