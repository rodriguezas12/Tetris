import pygame
import os
import subprocess

# Inicializar pygame
pygame.init()

# Obtener resolución de pantalla
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Crear ventana sin bordes y con tamaño completo
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Game System")

# Cargamos las imágenes de los juegos (sin redimensionar)
games_images = [
    pygame.image.load(os.path.join(os.path.join(os.path.dirname(__file__), "images"), "DK.png")),
    pygame.image.load(os.path.join(os.path.join(os.path.dirname(__file__), "images"), "Tetris.png")),
    pygame.image.load(os.path.join(os.path.join(os.path.dirname(__file__), "images"), "smash_bros.png")),
    pygame.image.load(os.path.join(os.path.join(os.path.dirname(__file__), "images"), "idk.png"))
]

# Definimos las rutas de los juegos .py correspondientes
games_scripts = [
    os.path.join(os.path.dirname(__file__), "Games", "DK", "DK.py"),      # Ruta para el script de DK
    os.path.join(os.path.dirname(__file__), "Games", "Tetris", "Tetris.py"),   # Ruta para el script de Tetris
    os.path.join(os.path.dirname(__file__), "Games", "smash_bros", "smash_bros.py"), # Ruta para el script de Smash Bros.
    os.path.join(os.path.dirname(__file__), "Games", "game_4", "idk.py")       # Ruta para el script de idk
]

# Sonidos
sounds_folder = os.path.join(os.path.dirname(__file__), "music")
sound_displacement_menu = pygame.mixer.Sound(os.path.join(sounds_folder, "12sq1.wav")) # sonido de moverse entre las opciones
sound_select_option_menu = pygame.mixer.Sound(os.path.join(sounds_folder, "13sq1.wav")) # sonido de elegir una opción del menú de música

# Variable para la imagen actual
current_image_index = 0  # Empezamos con la primera imagen (Tetris)

# Cargamos la música
pygame.mixer.music.load(os.path.join(os.path.join(os.path.dirname(__file__), "music"), "SNES_Classic_Edition_Menu_Song.mp3"))
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en loop

# Funciones de texto
font = pygame.font.Font(os.path.join(os.path.join(os.path.dirname(__file__), "Font"), "Pixel_NES.otf"), 36)
WHITE = (255, 255, 255)

def play_sound(effect):  # Play the sound effects
    effect.play()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Función para ejecutar el script de juego
def run_game_script(script_path):
    try:
        # Ejecutamos el script .py y guardamos el subproceso
        return subprocess.Popen(["python", script_path])  # Ejecuta el script y retorna el proceso
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")

# Función principal del menú
def menu():
    global current_image_index  # Para actualizar el índice de la imagen actual
    running = True
    game_process = None  # Al principio no hay ningún juego en ejecución

    while running:
        screen.fill((0, 0, 0))  # Fondo negro (ya no usamos background.png)

        # Obtenemos el tamaño de la imagen actual
        current_image = games_images[current_image_index]
        img_width, img_height = current_image.get_size()

        # Calculamos la posición para centrar la imagen
        x_pos = (WIDTH - img_width) // 2
        y_pos = (HEIGHT - img_height) // 2

        # Dibujamos la imagen del juego actual en su tamaño original
        screen.blit(current_image, (x_pos, y_pos))

        # Actualizamos la pantalla
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_process:
                        game_process.terminate()  # Termina el subproceso del juego actual
                    running = False  # Para salir del menú si presionas ESC
                elif event.key == pygame.K_RIGHT:
                    # Mover a la siguiente imagen
                    current_image_index = (current_image_index + 1) % len(games_images)
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_LEFT:
                    # Mover a la imagen anterior
                    current_image_index = (current_image_index - 1) % len(games_images)
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_RETURN:
                    # Detener la música del menú
                    pygame.mixer.music.stop()
                    # Ejecutar el juego correspondiente
                    selected_game_script = games_scripts[current_image_index]
                    game_process = run_game_script(selected_game_script)  # Ejecutar el script del juego
                    play_sound(sound_select_option_menu)  # Sonido de selección

    pygame.quit()

# Ejecutamos el menú
menu()
