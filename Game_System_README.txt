# Game System

This is a game selection system that allows users to navigate through different game options. Upon selecting a game, the corresponding Python script is executed. This system runs in fullscreen mode and allows seamless transition between the menu and game scripts.

################
# Requirements #
################

Before you can run the Game System, make sure you have the following dependencies installed:

1. Python 3.x  
   This game system is developed using Python. Make sure Python 3.x is installed on your system. You can download it from here: https://www.python.org/downloads/

2. Pygame  
   The Pygame library is used for handling graphics, sound, and user input. You can install it using pip:
   ```bash
   pip install pygame
   ```

3. Subprocess (Standard Python Library)  
   The subprocess module is used to run external Python scripts when a game is selected. It is already included in Python, so no additional installation is needed.

#########
# Setup #
#########

1. Download the Game System Files  
   Clone or download the repository containing the Game System and place it in a folder on your machine.

2. Game Scripts  
   Inside the `Games` folder, you will find individual folders for each game (DK, Tetris, Smash Bros, idk). Each game folder contains a Python script (`.py` file) for that game. These scripts will be executed when you select a game from the menu.

3. Images and Music  
   - Place the game cover images (e.g., DK.png, Tetris.png, etc.) inside the `images` folder.
   - Put the music files and sound effects (e.g., `SNES_Classic_Edition_Menu_Song.mp3`, `12sq1.wav`, `13sq1.wav`) inside the `music` folder.
   - The font used for the menu is `Pixel_NES.otf` and should be placed in the `Font` folder.

4. Adjust the Game Scripts Paths  
   Ensure that the paths to the `.py` scripts are correct and point to the actual locations of your game scripts in the `Games` folder.

##############
# How to Use #
##############

1. Launch the Game System  
   Run the main Python file for the Game System. The menu will display the game options as images on the screen.

2. Navigate the Menu  
   - Use the **left and right arrow keys** to move between the game options.
   - When you hover over the game you wish to select, press **Enter** to start the game.
   - If you wish to exit the menu at any time, press **Escape**.

3. Playing the Game  
   - Once a game is selected, the system will stop the background menu music and run the corresponding Python script for the game in a new window.
   - After the game is over, the user can return to the menu by closing the game window, and the menu will be displayed again.

4. Exit the Game System  
   - Press **Escape** in the menu or close the game window to exit the game system entirely.

####################
# Folder Structure #
#################### 

Here’s how your project folder should be structured:

```
GameSystem/
│
├── images/                  # Contains images of the games (DK.png, Tetris.png, etc.)
├── music/                   # Contains music and sound files (MP3, WAV)
├── Font/                    # Contains the Pixel_NES.otf font file
│
├── Games/                   # Contains game folders (DK, Tetris, Smash Bros, idk)
│   ├── DK/
│   │   └── DK.py            # Python script for DK game
│   ├── Tetris/
│   │   └── Tetris.py        # Python script for Tetris game
│   ├── smash_bros/
│   │   └── smash_bros.py    # Python script for Smash Bros game
│   └── idk/
│       └── idk.py           # Python script for the idk game
│
└── main_game_system.py      # Main Python script for the Game System
```

##################
# Libraries Used #
##################

1. **Pygame**  
   Pygame is used for rendering the game window, handling events, playing sounds, and loading images.

2. **Subprocess**  
   Used for running external Python scripts (i.e., launching games as separate processes).

3. **os**  
   The **os** library is used to manage file paths, making the game system flexible and compatible across different platforms.


