######################
# DEFINING LIBRARIES #
######################

import pygame
import random
import os
from pydub import AudioSegment
import simpleaudio as sa
import sys

##########################
# INITIALIZING VARIABLES #
##########################

try: 
    # Inicializamos pygame
    pygame.init()

    # Obtener la resolución actual de la pantalla
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h  # Resolución de pantalla completa

    # Variables originales del juego
    NES_WIDTH, NES_HEIGHT = 256, 240
    SCALE_FACTOR = 2.8
    WINDOW_WIDTH, WINDOW_HEIGHT = NES_WIDTH * SCALE_FACTOR, NES_HEIGHT * SCALE_FACTOR

    BOARD_X = 267
    BOARD_Y = 120   
    BOARD_WIDTH = 240
    BOARD_HEIGHT = 500  

    GRID_COLUMNS, GRID_ROWS = 10, 20
    GRID_SIZE = BOARD_WIDTH // GRID_COLUMNS  

    # Asegúrate de que el WIDTH y HEIGHT son correctos para la pantalla completa
    WIDTH = screen_width  # Resolución de pantalla completa
    HEIGHT = screen_height  # Resolución de pantalla completa

    # Calculamos el tamaño de la ventana basado en el factor de escala
    window_width = int(NES_WIDTH * SCALE_FACTOR)
    window_height = int(NES_HEIGHT * SCALE_FACTOR)

    # Inicializamos pygame.mixer para los sonidos
    pygame.mixer.init()

    # Creamos la ventana de la pantalla completa (o ajustada si prefieres)
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    image_folder = os.path.join(os.path.dirname(__file__), "images\lvl0")
    images = os.path.join(os.path.dirname(__file__), "images")
    background_path = os.path.join(images, "background.png")
    music_path = os.path.join(os.path.dirname(__file__), "music", "music theme 1.ogg")

    # Ruta de la carpeta de sonidos
    sounds_folder = os.path.join(os.path.dirname(__file__), "music", "Sounds")

    # Cargar efectos de sonido
    sound_move = pygame.mixer.Sound(os.path.join(sounds_folder, "14sq1.wav"))  # Sonido de movimiento lateral
    sound_rotate = pygame.mixer.Sound(os.path.join(sounds_folder, "16sq1.wav"))  # Sonido de rotación
    sound_level_up = pygame.mixer.Sound(os.path.join(sounds_folder, "17sq1.wav"))  
    sound_displacement_menu= pygame.mixer.Sound(os.path.join(sounds_folder, "12sq1.wav")) # sonido de moverse entre las opciones
    sound_select_option_menu= pygame.mixer.Sound(os.path.join(sounds_folder, "13sq1.wav")) # sonido de elegir una opción del menú de música
    sound_set_piece= pygame.mixer.Sound(os.path.join(sounds_folder, "18sq1.wav")) # sonido de pieza al setearse
    sound_eliminating_rows= pygame.mixer.Sound(os.path.join(sounds_folder, "21sq1.wav")) # sonido cuando se elimina una, dos o tres filas de la grid
    sound_eliminating_4_rows= pygame.mixer.Sound(os.path.join(sounds_folder, "tetris-nes-four-line-101soundboards.mp3")) # sonido cuando se eliminan 4 filas de la grid
    sound_select_level= pygame.mixer.Sound(os.path.join(sounds_folder, "26sq1.wav")) # sonido de elegir un nivel para empezar
    sound_game_over= pygame.mixer.Sound(os.path.join(sounds_folder, "24noi.wav")) # sonido game over
    
    # Rutas de los archivos de música en la carpeta "music"
    music_files = [
        os.path.join(os.path.dirname(__file__), "music", "music theme 1.ogg"),
        os.path.join(os.path.dirname(__file__), "music", "music theme 2.ogg"),
        os.path.join(os.path.dirname(__file__), "music", "music theme 3.ogg"),
        None,
        os.path.join(os.path.dirname(__file__), "music", "08_-_Tetris_-_NES_-_Victory.ogg"),
        os.path.join(os.path.dirname(__file__), "music", "24noi.wav"),
        os.path.join(os.path.dirname(__file__), "music", "09_-_Tetris_-_NES_-_High_Score.ogg")  # Representa la opción OFF (sin música)
    ]


    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    block_textures = {
        'I': pygame.image.load(os.path.join(image_folder, "ZLI.png")),
        'J': pygame.image.load(os.path.join(image_folder, "JS.png")),
        'L': pygame.image.load(os.path.join(image_folder, "ZLI.png")),
        'O': pygame.image.load(os.path.join(image_folder, "OT.png")),
        'S': pygame.image.load(os.path.join(image_folder, "JS.png")),
        'T': pygame.image.load(os.path.join(image_folder, "OT.png")),
        'Z': pygame.image.load(os.path.join(image_folder, "ZLI.png"))
    }

    #Defining the geometrical shape of the tetraminos
    TETROMINOS = {
        'T': [[0, 1, 0], [1, 1, 1]],
        'J': [[1, 0, 0], [1, 1, 1]],
        'Z': [[1, 1, 0], [0, 1, 1]],
        'O': [[1, 1], [1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]],
        'L': [[0, 0, 1], [1, 1, 1]],
        'I': [[1, 1, 1, 1]]
    }

    credit_screen_path = os.path.join(images, "Credit_screen.png")
    title_screen_path = os.path.join(images, "Title_screen.png")
    grid = [[None for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
    soft_drop_active = False 
    level = 0
    lines_to_next_level = [10] * 29
    total_lines = 0  
    music_normal = os.path.join(os.path.dirname(__file__), "music", "music theme 1.ogg")
    music_fast = os.path.join(os.path.dirname(__file__), "music", "music theme 2 fast.ogg")
    current_music = None  
    piece_count = {key: 0 for key in TETROMINOS.keys()}  

except ValueError:  
    print("Error trying to initialize variables")

#######
# ROM #
#######

def get_lowest_score():
    # Leer el archivo de high_scores.txt y obtener el puntaje más bajo
    with open(os.path.join(os.path.join(os.path.dirname(__file__), "ROM"), "high_scores.txt"), "r") as file:
        lines = file.readlines()

    # Inicializar lowest_score con un valor alto
    lowest_score = float('inf')

    # Revisar específicamente Score3
    score3_line = lines[8].strip()  # La línea 8 tiene el valor de Score3

    if score3_line and score3_line.split(":")[1].strip():  # Si no está vacío
        try:
            lowest_score = int(score3_line.split(":")[1].strip())  # Convertir el puntaje de Score3 a entero
        except ValueError:
            lowest_score = 0  # En caso de error, asignar un puntaje de 0
    else:
        lowest_score = 0  # Si Score3 está vacío, asignamos 0

    print(lowest_score)
    return lowest_score

def save_high_score(player_name, score, level):
    # Leer el archivo de high_scores.txt y obtener los datos actuales
    with open(os.path.join(os.path.join(os.path.dirname(__file__), "ROM"), "high_scores.txt"), "r") as file:
        lines = file.readlines()

    # Evaluamos si el puntaje entra en el podio
    inserted = False
    for i in range(3):  # Asumiendo que hay 3 puestos en el podio
        score_line = f"Score{i+1}:"
        
        try:
            # Si el puntaje del jugador es mayor o igual que el puntaje actual
            current_score_line = lines[i * 3 + 2].strip()  # Obtener la línea con el puntaje
            if not current_score_line:  # Si la línea está vacía, saltar
                continue
            current_score = int(current_score_line.split(":")[1].strip())  # Obtener el puntaje de la línea
            
            # Verificamos si el puntaje del jugador es mayor
            if score > current_score:
                # Desplazar los puntajes hacia abajo
                # Empezamos desde el tercer puesto hacia abajo, para no sobrescribir
                for j in range(2, i-1, -1):  # Desplazamos de abajo hacia arriba
                    # Guardamos el jugador que está en la posición j
                    lines[j * 3 + 1] = lines[(j-1) * 3 + 1]  # Nombre
                    lines[j * 3 + 2] = lines[(j-1) * 3 + 2]  # Score
                    lines[j * 3 + 3] = lines[(j-1) * 3 + 3]  # Level
                
                # Insertamos el nuevo jugador en la posición correcta
                lines[i * 3 + 1] = f"Name{i+1}: {player_name}\n"
                lines[i * 3 + 2] = f"Score{i+1}: {score}\n"
                lines[i * 3 + 3] = f"Lvl{i+1}: {level}\n"
                inserted = True
                break  # Salir del bucle después de insertar

        except (IndexError, ValueError):  # Maneja el caso donde no hay datos o los datos son inválidos
            print("no data")
            # Si hay un lugar vacío en el podio, colocamos los datos directamente
            lines[i * 3 + 1] = f"Name{i+1}: {player_name}\n"
            lines[i * 3 + 2] = f"Score{i+1}: {score}\n"
            lines[i * 3 + 3] = f"Lvl{i+1}: {level}\n"
            inserted = True
            break  # Salimos del bucle después de insertar los datos

    # Si no se insertó nada (porque el puntaje no es mayor que ninguno), dejamos el archivo como estaba
    if not inserted:
        print("El puntaje no supera los puntajes existentes, no se insertaron cambios.")
    
    # Guardar los cambios en el archivo
    with open(os.path.join(os.path.join(os.path.dirname(__file__), "ROM"), "high_scores.txt"), "w") as file:
        file.writelines(lines)



#############################
# SOUND AND MUSIC FUNCTIONS #
#############################

def play_sound(effect): #play the sounds effects.
    effect.play()

def play_selected_music(selected_index): #Play the selected music and stops the previous one.
    """Reproduce la música seleccionada en el menú."""
    pygame.mixer.music.stop()  # Detener cualquier música en reproducción
    if music_files[selected_index]:  # Si no es OFF
        pygame.mixer.music.load(music_files[selected_index])
        pygame.mixer.music.set_volume(0.5)
        if selected_index == 5:
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()  # Repetir indefinidamente
        else:
            pygame.mixer.music.play(-1)

def start_game_music(selected_index): #Play the selected music for the first time.
    """Inicia la música cuando comienza la partida."""
    pygame.mixer.music.load(music_files[selected_index])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

###########################
# DRAW AND SHOW FUNCTIONS #
###########################

def show_credit_screen(image_path, duration=100, wait_for_input=False): #Displays a screen for a specified time
    """
    Muestra una imagen en pantalla. 
    - `duration`: Si se proporciona, la imagen se muestra por ese tiempo en milisegundos.
    - `wait_for_input`: Si es True, espera que el usuario presione ENTER antes de continuar.
    """
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    screen.blit(image, (0, 0))
    pygame.display.flip()

    if duration:
        pygame.time.delay(duration)  # Esperar el tiempo indicado
    
    if wait_for_input:
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    play_sound(sound_select_option_menu)
                    waiting = False  # Salir del bucle cuando el usuario presione ENTER

def draw_level(): #Shows the current level on the screen
    """Dibuja el nivel actual en pantalla"""
    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")

    font = pygame.font.Font(font_path, 30)  
    level_text = font.render("LEVEL", True, (255, 255, 255))  
    level_number = font.render(f"{level:02d}", True, (255, 255, 255))  

    screen.blit(level_text, (540, 447))  
    screen.blit(level_number, (569, 471))  

def show_game_over():  # Shows the GAME OVER at the end of the game. 
    global grid, piece_count, total_lines, score
    # Reproducir la música de fin de juego
    play_selected_music(4)  # Reproducir música de fin de juego
    
    # Mostrar la imagen de Game Over
    game_over_image = pygame.image.load(os.path.join(images, "Game_Over", "Game_over_screen.png"))
    game_over_image = pygame.transform.scale(game_over_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Ajustar tamaño
    screen.blit(game_over_image, (0, 0))  # Colocar la imagen en la pantalla

    # Mostrar el puntaje del jugador
    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")
    font = pygame.font.Font(font_path, 30)  
    score_text = font.render(f"Score {score}", True, (255, 255, 255))  # El puntaje en color blanco

    # Posición del puntaje en la pantalla (puedes ajustar la posición según necesites)
    score_x = (WINDOW_WIDTH - score_text.get_width()) // 2 - 100 # Centrar el puntaje en la pantalla
    score_y = WINDOW_HEIGHT // 2 - 273  # Ajustar la posición en el eje Y

    screen.blit(score_text, (score_x, score_y))  # Colocar el puntaje en la pantalla
    pygame.display.flip()  # Actualizar la pantalla

    # Esperar la entrada del usuario para continuar
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Si presionan ENTER
                    # Evaluar si el puntaje entra en el podio
                    if score >= get_lowest_score():  # Si el puntaje entra en el podio
                        high_score_menu()  # Llamar a high_score_menu si el puntaje entra en el podio
                    else:
                        start_game()  # Llamar a game_menu si no entra en el podio
                    waiting_for_input = False  # Salir del loop para continuar

def draw_lines(): #Only shows the Lines count in the screen
    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")

    font = pygame.font.Font(font_path, 28) 
    lines_text = font.render(f"LINES-{total_lines:03}", True, (255, 255, 255)) 

    screen.blit(lines_text, (292, 43)) 

def draw_score(): #Only shows the Score count in the screen
    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")

    font = pygame.font.Font(font_path, 30)  
    score_font = pygame.font.Font(font_path, 30)  
    
    score_text = font.render("SCORE", True, (255, 255, 255))  
    formatted_score = f"{score:06d}" 
    number_text = score_font.render(formatted_score, True, (255, 255, 255))  

    screen.blit(score_text, (537, 135))  
    screen.blit(number_text, (537, 159)) 

def draw_next_piece(): #Shows the next tetromino to play in the screen
    next_x = 548 
    next_y = 333 

    if next_piece.shape_type == 'O':
        next_x = 557 
    if next_piece.shape_type == 'I':
        next_x = 533 

    for row_idx, row in enumerate(next_piece.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                screen.blit(block_textures[next_piece.shape_type], 
                (next_x + col_idx * GRID_SIZE, next_y + row_idx * GRID_SIZE))

def draw_grid(): #Delimits the grid size in the screen.
    for y in range(GRID_ROWS):
        for x in range(GRID_COLUMNS):
            if grid[y][x] is not None:  
                screen.blit(block_textures[grid[y][x]], 
                            (BOARD_X + x * GRID_SIZE, BOARD_Y + y * GRID_SIZE))

    for x in range(BOARD_X, BOARD_X + BOARD_WIDTH + 1, GRID_SIZE):
        pygame.draw.line(screen, (100, 100, 100), (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT))

    for y in range(BOARD_Y, BOARD_Y + BOARD_HEIGHT + 1, GRID_SIZE):
        pygame.draw.line(screen, (100, 100, 100), (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y))

#####################################
# LOGIC AND FUNCTIONALITY FUNCTIONS #
#####################################

def update_level(): #Logic to increase the Level, Load the textures of any level, play sound effect of lvl up. (USES GLOBAL VARIABLES)
    global level, next_piece  
    if level < len(lines_to_next_level) and total_lines >= sum(lines_to_next_level[:level + 1]):
        level += 1
        load_textures_for_level(level) 
        if next_piece:
            next_piece.texture = block_textures[next_piece.shape_type]
        play_sound(sound_level_up)  
        draw_level()

def game_over_animation(level):  # Función para reproducir la animación del Game Over
    """Reproduce la secuencia de imágenes del Game Over según el nivel."""
    game_over_folder = os.path.join(images, "Game_Over", f"Lvl_{level}")  # Ruta de la carpeta del nivel
    image_files = [f"{i}.png" for i in range(1, 24)]  # Archivos de imagen 1.png, 2.png, ..., 23.png
    image_files = [os.path.join(game_over_folder, img) for img in image_files]  # Lista completa de imágenes

    # Cargar y mostrar las imágenes en secuencia
    for img_path in image_files:
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Ajustar tamaño si es necesario
        screen.blit(img, (0, 0))  # Mostrar la imagen en pantalla
        pygame.display.flip()  # Actualizar la pantalla
        pygame.time.delay(90)  # Esperar 0.1 segundos entre imágenes

def check_game_over():  # Lógica para determinar GAME OVER
    for col in range(GRID_COLUMNS):
        if grid[0][col] is not None:  # Si hay un bloque en la fila superior

            play_selected_music(5)  # Reproducir sonido de Game Over
            game_over_animation(level)  # Reproducir la animación de Game Over según el nivel
            pygame.time.delay(3000)
            return True  # Retorna True si el juego terminó
    return False  # Retorna False si el juego continúa

def check_and_update_music(selected_music_index): # Logic to accelerate and decelerate the selected music.
    """Verifies the block height in the grid and changes the music speed if necessary."""
    global current_music

    if selected_music_index == 3:  # If "OFF" is selected, stop the music
        pygame.mixer.music.stop()
        current_music = None
        return

    # Define paths for normal and fast versions of the selected music
    normal_music_path = os.path.join(os.path.dirname(__file__), "music", f"music theme {selected_music_index + 1}.ogg")
    fast_music_path = os.path.join(os.path.dirname(__file__), "music", f"music theme {selected_music_index + 1} fast.ogg")

    danger_zone = 6  
    highest_block = GRID_ROWS  

    # Check the highest occupied row in the grid
    for row_idx in range(GRID_ROWS):
        if any(grid[row_idx][col] is not None for col in range(GRID_COLUMNS)):
            highest_block = row_idx  
            break 

    # Choose between normal and fast music
    new_music = fast_music_path if highest_block < danger_zone else normal_music_path

    # Update music only if it has changed
    if new_music != current_music:
        pygame.mixer.music.load(new_music)
        pygame.mixer.music.play(-1)  
        current_music = new_music

def clear_lines(): #Checks and removes full rows, Increases the Score count, Increases the Lines count, checks to update level.
    global grid, total_lines, score  

    new_grid = [row for row in grid if any(cell is None for cell in row)]  
    lines_cleared = GRID_ROWS - len(new_grid)  

    if lines_cleared > 0 and lines_cleared < 4:
        total_lines += lines_cleared  
        score += lines_cleared * 100 
        play_sound(sound_eliminating_rows)
    elif lines_cleared == 4:
        total_lines += lines_cleared  
        score += lines_cleared * 100 
        sound_set_piece.set_volume(0.5)
        play_sound(sound_eliminating_4_rows)
    while len(new_grid) < GRID_ROWS:
        new_grid.insert(0, [None] * GRID_COLUMNS)

    update_level()

    grid = new_grid 

def draw_statistics(): #Shows and controls the logic of the statistics count in the screen
    font_path = os.path.join(os.path.dirname(__file__), "Font", "tetris-font.ttf")

    font = pygame.font.Font(font_path, 24)
    number_font = pygame.font.Font(font_path, 24)

    stats_x = 73  
    stats_y = 255  
    spacing_y = 49 

    scale_factor = 0.707 

    for idx, key in enumerate(TETROMINOS.keys()):
        tetromino_shape = TETROMINOS[key]  
        original_texture = block_textures[key]  
        
        scaled_texture = pygame.transform.scale(original_texture, 
                        (int(GRID_SIZE * scale_factor), int(GRID_SIZE * scale_factor)))

        piece_x = stats_x
        piece_y = stats_y + idx * spacing_y

        if key == 'O':  
            piece_x += 8  
        if key == 'I':  
            piece_x -= 6  

        for row_idx, row in enumerate(tetromino_shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    screen.blit(scaled_texture, (piece_x + col_idx * int(GRID_SIZE * scale_factor), 
                                                 piece_y + row_idx * int(GRID_SIZE * scale_factor)))

        count_text = number_font.render(f"{piece_count[key]:03d}", True, (255, 0, 0)) 
        screen.blit(count_text, (stats_x + 70, stats_y + idx * spacing_y))  

def game_menu():  # Fusión de selección de música y selección de tipo de juego
    """Displays the menu where the player can select game type and music."""
    global level
    play_selected_music(0)  # Start with the first music option

    menu_image_path = os.path.join(images, "Menu_screen.png")
    menu_image = pygame.image.load(menu_image_path)
    menu_image = pygame.transform.scale(menu_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    left_arrow = pygame.image.load(os.path.join(images, "flecha_izq.png"))
    right_arrow = pygame.image.load(os.path.join(images, "flecha_der.png"))

    # Redimensionar las flechas (cambiar 40, 40 por el tamaño deseado)
    left_arrow = pygame.transform.scale(left_arrow, (22, 22))  # Cambia el tamaño de la flecha izquierda
    right_arrow = pygame.transform.scale(right_arrow, (23, 23))  # Cambia el tamaño de la flecha derecha

    selected_music = 0  # Start with "Music - 1"
    selected_game_type = 0  # 0 = Type A, 1 = Type B
    
    # Variable para el parpadeo
    show_arrows = True  # Controla si las flechas se deben mostrar
    arrow_timer = 0  # Temporizador para el parpadeo (en frames)

    while True:
        screen.blit(menu_image, (0, 0))  
        font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")
        font = pygame.font.Font(font_path, 30)

        # **Opciones de música**
        music_options = ["MUSIC - 1", "MUSIC - 2", "MUSIC - 3", "OFF"]
        for i, option in enumerate(music_options):
            text_x = 350  
            text_y = 405 + (i * 48)  

            if i == selected_music:  # Mostrar flechas en la opción seleccionada
                if show_arrows:
                    screen.blit(left_arrow, (text_x - 62, text_y))
                    screen.blit(right_arrow, (text_x + 148, text_y))

        # **Opciones de tipo de juego**
        game_type_y = 167  # Posición de los botones
        game_types = ["A-TYPE", "B-TYPE"]

        for i, option in enumerate(game_types):
            x_offset = 164 if i == 0 else 388  # Posición de los textos A-TYPE y B-TYPE

            if i == selected_game_type:
                if selected_game_type == 0:  # Tipo A
                    if show_arrows:
                        screen.blit(left_arrow, (x_offset + 10, game_type_y))
                        screen.blit(right_arrow, (x_offset + 173, game_type_y))
                else:  # Tipo B
                    if show_arrows:
                        screen.blit(left_arrow, (x_offset + 56, game_type_y))
                        screen.blit(right_arrow, (x_offset + 219, game_type_y))

        pygame.display.flip()

        # **Manejo de eventos**
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_music = (selected_music + 1) % len(music_options)
                    play_selected_music(selected_music)
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_UP:
                    selected_music = (selected_music - 1) % len(music_options)
                    play_selected_music(selected_music)
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_LEFT:
                    selected_game_type = 0  # Selecciona Type A
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_RIGHT:
                    selected_game_type = 1  # Selecciona Type B
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_RETURN:
                    play_sound(sound_select_option_menu)
                    return selected_music, selected_game_type  # Devuelve selección

        # Actualiza el temporizador y el estado de las flechas
        arrow_timer += 1
        if arrow_timer >= 4:  # Cambia el valor de 30 para ajustar la velocidad de parpadeo
            arrow_timer = 0
            show_arrows = not show_arrows  # Alterna la visibilidad de las flechas


def high_score_menu():
    """Muestra el menú de High Scores para ingresar el nombre del jugador en el podio"""
    # Reproducir la música del high score
    play_selected_music(6)  # Asegúrate de que el índice de la música esté correcto
    
    # Cargar la imagen del menú de high score
    high_score_image = pygame.image.load(os.path.join(images, "New_High_Score_Menu.png"))
    high_score_image = pygame.transform.scale(high_score_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(high_score_image, (0, 0))  # Mostrar la imagen de fondo

    # El alfabeto que el jugador puede seleccionar
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    current_letter_idx = 0  # Índice para la letra seleccionada actualmente
    name = ["_"] * 6  # Nombre del jugador, con 6 espacios

    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")
    font = pygame.font.Font(font_path, 30)

    # Mostrar el puntaje y el nivel en la pantalla
    score_text = f"{score}"  # Mostrar el puntaje
    level_text = f"{level}"  # Mostrar el nivel

    score_surface = font.render(score_text, True, (255, 255, 255))  # Color blanco
    level_surface = font.render(level_text, True, (255, 255, 255))  # Color blanco

    # Posiciones para el puntaje y nivel
    score_x = (WINDOW_WIDTH - score_surface.get_width()) // 2 + 28
    score_y = WINDOW_HEIGHT // 2 + 111  # Ajustar la posición para que no se superponga con el nombre

    level_x = (WINDOW_WIDTH - level_surface.get_width()) // 2 + 170
    level_y = WINDOW_HEIGHT // 2 + 111  # Colocar el nivel debajo del puntaje

    while True:
        screen.blit(high_score_image, (0, 0))  # Mostrar la imagen de fondo de high score

        # Mostrar el nombre actual
        name_text = ''.join(name)  # Unir las letras para formar el nombre
        name_surface = font.render(name_text, True, (255, 255, 255))  # Blanco
        name_x = (WINDOW_WIDTH - name_surface.get_width()) // 2 - 86 # Centrar nombre en la pantalla
        name_y = WINDOW_HEIGHT // 2 + 111  # Ajustar posición Y
        screen.blit(name_surface, (name_x, name_y))

        # Mostrar el puntaje y nivel en todo momento
        screen.blit(score_surface, (score_x, score_y))  # Mostrar puntaje
        screen.blit(level_surface, (level_x, level_y))  # Mostrar nivel

        # Mostrar la letra seleccionada
        letter_surface = font.render(alphabet[current_letter_idx], True, (255, 255, 255))  # Blanco
        letter_x = (WINDOW_WIDTH // 2) - 150  # X de la letra seleccionada
        letter_y = 250  # Y de la letra seleccionada
        screen.blit(letter_surface, (letter_x, letter_y))

        pygame.display.flip()  # Actualizar la pantalla

        # Manejar la entrada del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    play_sound(sound_displacement_menu)
                    current_letter_idx = (current_letter_idx + 1) % len(alphabet)  # Mover hacia abajo en el alfabeto
                elif event.key == pygame.K_UP:
                    play_sound(sound_displacement_menu)
                    current_letter_idx = (current_letter_idx - 1) % len(alphabet)  # Mover hacia arriba en el alfabeto
                elif event.key == pygame.K_RETURN:
                    # Añadir la letra seleccionada al nombre
                    play_sound(sound_displacement_menu)
                    for i in range(6):
                        if name[i] == "_":
                            name[i] = alphabet[current_letter_idx]
                            break  # Una vez que se llena el espacio, detener la selección

                    # Si el nombre está completo, guardar en el archivo y volver al menú de juego
                    if "_" not in name:
                        play_sound(sound_select_option_menu)
                        save_high_score(name,score,level)  # Guardar el nuevo score
                        start_game()

def level_selection_menu():  # Handles level selection after choosing Type A
    """Displays the level selection screen and allows the user to pick a starting level (0-9)."""
    global level, selected_music, selected_game_type
    level_screen_path = os.path.join(images, "Level_screen.png")  # Load Level Screen
    level_screen = pygame.image.load(level_screen_path)
    level_screen = pygame.transform.scale(level_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
    play_selected_music(3)

    # Load the Level Screen Selector PNG
    level_selector_path = os.path.join(images, "Level_screen_selector.png")  # Load the Level screen selector
    level_selector = pygame.image.load(level_selector_path)
    level_selector = pygame.transform.scale(level_selector, (39, 44))  # Adjust the size of the selector image

    # Define grid for level selection (2 rows, 5 columns)
    level_grid = [[0, 1, 2, 3, 4], 
                  [5, 6, 7, 8, 9]]

    row, col = 0, 0  # Initial selection position

    # Variable to adjust position and size
    level_x = 157  # Starting X position for levels
    level_y = 229  # Starting Y position for levels
    level_size = 32  # Font size for level numbers

    # Define the reddish color for the level numbers (RGB values)
    reddish_color = (255, 60, 30)  # You can adjust the color if needed

    # Variables for controlling the blinking effect
    show_selector = True  # Control if the level selector image should blink
    selector_timer = 0  # Timer to control blinking effect
    blinking_delay = 3  # Frames delay for the blinking effect (make it faster or slower)
    blinking_active = False  # To control when blinking should start (only after pressing Enter)
    blink_duration = 2000  # Duration for blinking effect in milliseconds
    start_time = None  # Variable to store the time when Enter was pressed

    while True:
        screen.blit(level_screen, (0, 0))  # Display level selection screen

        # Calculate the position of the selector image based on the selected level
        selector_x = 3 + level_x + (col * 45) - (level_selector.get_width() // 3.3)
        selector_y = 21 + level_y + (row * 48) - (level_selector.get_height() // 2)

        # If blinking is active, toggle visibility of the selector image
        if blinking_active:
            if start_time is None:
                start_time = pygame.time.get_ticks()  # Record the time when Enter is pressed
            
            # Check how much time has passed since Enter was pressed
            elapsed_time = pygame.time.get_ticks() - start_time

            # Toggle the visibility of the selector based on elapsed time
            if elapsed_time < blink_duration:
                selector_timer += 1
                if selector_timer >= blinking_delay:
                    selector_timer = 0
                    show_selector = not show_selector  # Toggle visibility every blinking_delay frames
            else:
                # Once the time has passed, stop blinking and return the selected level
                blinking_active = False
                return level_grid[row][col]

        # Display the level selector image (this is now drawn first, so it's behind the numbers)
        if show_selector:
            # Place the level selector image in the background (centered)
            screen.blit(level_selector, (selector_x, selector_y))

        font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")
        font = pygame.font.Font(font_path, level_size)

        for r in range(2):  # Iterate over rows
            for c in range(5):  # Iterate over columns
                # Render the level number with the reddish color
                level_text = font.render(f"{level_grid[r][c]}", True, reddish_color)  # Use the reddish color
                text_x = level_x + (c * 45)  # Adjust X spacing between levels (more spacing)
                text_y = level_y + (r * 48)  # Adjust Y spacing between levels (more spacing)
                screen.blit(level_text, (text_x, text_y))

        pygame.display.flip()

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    col = (col + 1) % 5  # Move right in grid
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_LEFT:
                    col = (col - 1) % 5  # Move left in grid
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_DOWN:
                    row = (row + 1) % 2  # Move down in grid
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_UP:
                    row = (row - 1) % 2  # Move up in grid
                    play_sound(sound_displacement_menu)
                elif event.key == pygame.K_RETURN:
                    play_sound(sound_select_option_menu)
                    # Start the blinking effect after pressing Enter (2-second delay)
                    blinking_active = True  # Activate blinking
                    start_time = None  # Reset start time for a new delay cycle
                    pygame.time.delay(100)  # Small delay to allow input to register
                elif event.key == pygame.K_z:  # If the user presses 'Z', go to the game menu
                    selected_music, selected_game_type = game_menu()  # Call the game menu to go back to the main menu
                    play_selected_music(3)

            
######################
# TEXTURES FUNCTIONS #
######################

def load_textures_for_level(level): #Load the textures of the tetrominos depending of the level.
    global block_textures, current_piece

    adjusted_level = level % 10  


    level_folder = os.path.join(images, f"lvl{adjusted_level}")  

    block_textures = {
        'I': pygame.image.load(os.path.join(level_folder, "ZLI.png")),
        'J': pygame.image.load(os.path.join(level_folder, "JS.png")),
        'L': pygame.image.load(os.path.join(level_folder, "ZLI.png")),
        'O': pygame.image.load(os.path.join(level_folder, "OT.png")),
        'S': pygame.image.load(os.path.join(level_folder, "JS.png")),
        'T': pygame.image.load(os.path.join(level_folder, "OT.png")),
        'Z': pygame.image.load(os.path.join(level_folder, "ZLI.png"))
    }

    for key in block_textures:
        block_textures[key] = pygame.transform.scale(block_textures[key], (GRID_SIZE, GRID_SIZE))

    if current_piece:
        current_piece.texture = block_textures[current_piece.shape_type]

#######################
# GAME TYPE FUNCTIONS #
#######################

def Type_A():
    """Function to start Type A game mode."""
    global running, piece_count, total_lines, score, level
    
    for k in range(20):  # Recorre las filasS
        for h in range(10):  # Recorre las columnas
            grid[k][h] = None
    piece_count = {key: 0 for key in TETROMINOS.keys()} 
    total_lines = 0  
    score = 0

    while running:
        delta_time = clock.tick(60)  
        screen.blit(background, (0, 0)) 
        #draw_grid()  

        for y in range(GRID_ROWS):
            for x in range(GRID_COLUMNS):
                if grid[y][x] is not None:
                    texture = block_textures[grid[y][x]]
                    screen.blit(texture, (BOARD_X + x * GRID_SIZE, BOARD_Y + y * GRID_SIZE))

        current_piece.draw(screen)
        current_piece.update(delta_time)  

        keys = pygame.key.get_pressed()
        soft_drop_active = keys[pygame.K_DOWN]  
        current_piece.fast_drop = soft_drop_active  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
        
        draw_level()
        draw_statistics()
        draw_lines() 
        draw_next_piece()
        draw_score()  
        check_and_update_music(selected_music)  
        load_textures_for_level(level) 
        
        pygame.display.flip() 

def Type_B():
    """Function to start Type B game mode."""
    print("Starting Type B Mode...")
    a = 1  # Placeholder para evitar errores

def start_game():
    global selected_game_type, level
    if selected_game_type == 0:
        level = level_selection_menu()
        Type_A()
    else:
        Type_B()

######################################################
# INITIALIZE PIECE MOVILITY FUNTION IN CLASS "PIECE" #
######################################################
class Piece:
    
    def __init__(self, shape):
        self.shape = TETROMINOS[shape]
        self.x = BOARD_X + (GRID_COLUMNS // 2 - len(self.shape[0]) // 2) * GRID_SIZE
        self.y = BOARD_Y
        self.shape_type = shape  
        self.texture = block_textures[shape]  
        self.fall_time = 0  
        self.fall_speed = 500  
        self.fast_drop = soft_drop_active 

    def draw(self, screen):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    screen.blit(
                        self.texture,
                        (self.x + col_idx * GRID_SIZE, self.y + row_idx * GRID_SIZE)
                    )

    def update(self, delta_time):
        self.fall_time += delta_time

        speed = 50 if self.fast_drop else self.fall_speed  

        if self.fall_time >= speed:
            if not self.check_collision(0, 1):
                self.move(0, 1)
            else:
                self.set_piece()
            self.fall_time = 0  

    def move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE

        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:  
                    block_new_x = (new_x - BOARD_X) // GRID_SIZE + col_idx
                    block_new_y = (new_y - BOARD_Y) // GRID_SIZE + row_idx

                    if block_new_x < 0 or block_new_x >= GRID_COLUMNS:  
                        return 
                    if block_new_y >= GRID_ROWS: 
                        return  
                    
                    if 0 <= block_new_y < GRID_ROWS and 0 <= block_new_x < GRID_COLUMNS:
                        if grid[block_new_y][block_new_x] is not None: 
                            return 
        self.x = new_x
        self.y = new_y

        if dx != 0:
            play_sound(sound_move)

    def rotate(self):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        max_x = BOARD_X + BOARD_WIDTH - len(rotated_shape[0]) * GRID_SIZE
        max_y = BOARD_Y + BOARD_HEIGHT - len(rotated_shape) * GRID_SIZE

        if BOARD_X <= self.x <= max_x and BOARD_Y <= self.y <= max_y:
            self.shape = rotated_shape

            play_sound(sound_rotate)

    def check_collision(self, dx, dy):
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = (self.x - BOARD_X) // GRID_SIZE + col_idx + dx
                    new_y = (self.y - BOARD_Y) // GRID_SIZE + row_idx + dy

                    if new_y >= GRID_ROWS or (0 <= new_x < GRID_COLUMNS and grid[new_y][new_x] is not None):
                        return True
        return False

    def set_piece(self):
        """Fija la pieza en la grid y genera la siguiente pieza con las texturas correctas."""
        global score, current_piece, next_piece, selected_music

        score += 10  

        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    sound_set_piece.set_volume(0.5)
                    play_sound(sound_set_piece)
                    grid_y = (self.y - BOARD_Y) // GRID_SIZE + row_idx
                    grid_x = (self.x - BOARD_X) // GRID_SIZE + col_idx
                    if 0 <= grid_y < GRID_ROWS and 0 <= grid_x < GRID_COLUMNS:
                        grid[grid_y][grid_x] = self.shape_type  

        clear_lines()
        check_and_update_music(selected_music)  

        if check_game_over():
            show_game_over()
            return  

        current_piece = next_piece  
        next_piece = Piece(random.choice(list(TETROMINOS.keys())))  

        current_piece.texture = block_textures[current_piece.shape_type]
        next_piece.texture = block_textures[next_piece.shape_type]

        piece_count[current_piece.shape_type] += 1  

###############################
# INITIALIZATION OF VARIABLES #
###############################

current_piece = Piece(random.choice(list(TETROMINOS.keys()))) #Selects randomly the tetromino that falls
piece_count[current_piece.shape_type] += 1 #Counts the pieces that falls
next_piece = Piece(random.choice(list(TETROMINOS.keys()))) #Selects randomly the tetromino that is next
show_credit_screen(credit_screen_path, duration=5000)
load_textures_for_level(level) #Load the textures of the selected level
show_credit_screen(title_screen_path, wait_for_input=True)
selected_music, selected_game_type = game_menu() # Selected music is 0, 1 or 2.
score = 0 #Initialize the starting score to 0
running = True #Determines when to stop the code
for key in block_textures:
    block_textures[key] = pygame.transform.scale(block_textures[key], (GRID_SIZE, GRID_SIZE))
start_game_music(selected_music) #Start the selected Game Music    
start_game()

