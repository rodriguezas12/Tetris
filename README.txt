TETRIS NES - README

============================
INSTALLATION INSTRUCTIONS
============================

To run this Tetris NES project successfully, you need to install the required Python libraries. Follow these steps to set up your environment:

1. **Ensure you have Python installed**
   - This project requires **Python 3.x**.
   - You can download it from: https://www.python.org/downloads/

2. **Install the required libraries**
   Open a terminal or command prompt and run the following command:
   ```
   pip install pygame pydub simpleaudio
   ```

   - `pygame`: Used for rendering graphics and handling game logic.
   - `pydub`: Required for manipulating and adjusting the music playback speed.
   - `simpleaudio`: Used to play back the modified audio in real-time.

3. **Ensure you have FFmpeg installed**
   - `pydub` requires **FFmpeg** to process audio files.
   - Download and install FFmpeg from: https://ffmpeg.org/download.html
   - After installation, ensure FFmpeg is added to your system path.

============================
RUNNING THE GAME
============================

1. **Navigate to the project folder**
   - Open a terminal/command prompt and go to the folder where `Tetris.py` is located.
   Example:
   ```
   cd path/to/tetris-project
   ```

2. **Run the game**
   - Execute the following command:
   ```
   python Tetris.py
   ```

   If all dependencies are installed correctly, the game should launch without issues.

============================
TROUBLESHOOTING
============================

- **ModuleNotFoundError**: If you encounter an error stating that a module is missing, ensure you installed all the required libraries using `pip install pygame pydub simpleaudio`.

- **Music issues**: If audio does not play correctly, confirm that FFmpeg is installed and added to the system path.

- **File not found errors**: Ensure all required assets (images, fonts, and music files) are located within the correct directories.

============================
CREDITS
============================

Developed by: Sergio Rodriguez
Game inspired by: Tetris NES 1981
Python Version: 3.x

