import pygame
import random
import os
from pydub import AudioSegment
import simpleaudio as sa

NES_WIDTH, NES_HEIGHT = 256, 240
SCALE_FACTOR = 2.8
WINDOW_WIDTH, WINDOW_HEIGHT = NES_WIDTH * SCALE_FACTOR, NES_HEIGHT * SCALE_FACTOR

BOARD_X = 267
BOARD_Y = 120   
BOARD_WIDTH = 240
BOARD_HEIGHT = 500  

GRID_COLUMNS, GRID_ROWS = 10, 20
GRID_SIZE = BOARD_WIDTH // GRID_COLUMNS  

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

image_folder = os.path.join(os.path.dirname(__file__), "images")
background_path = os.path.join(image_folder, "background.png")
music_path = os.path.join(os.path.dirname(__file__), "music", "theme.mp3")

pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

block_textures = {
    'I': pygame.image.load(os.path.join(image_folder, "ZLI_BLUE.png")),
    'J': pygame.image.load(os.path.join(image_folder, "JS_BLUE.png")),
    'L': pygame.image.load(os.path.join(image_folder, "ZLI_BLUE.png")),
    'O': pygame.image.load(os.path.join(image_folder, "OT_BLUE.png")),
    'S': pygame.image.load(os.path.join(image_folder, "JS_BLUE.png")),
    'T': pygame.image.load(os.path.join(image_folder, "OT_BLUE.png")),
    'Z': pygame.image.load(os.path.join(image_folder, "ZLI_BLUE.png"))
}

for key in block_textures:
    block_textures[key] = pygame.transform.scale(block_textures[key], (GRID_SIZE, GRID_SIZE))

TETROMINOS = {
    'T': [[0, 1, 0], [1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'I': [[1, 1, 1, 1]]
}

grid = [[None for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]

soft_drop_active = False  

def show_game_over():
    font = pygame.font.Font(None, 50)  
    text = font.render("GAME OVER", True, (255, 0, 0))  
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  
    screen.blit(text, text_rect)  
    pygame.display.flip() 

    pygame.time.delay(3000)  
    pygame.quit()
    exit()

def check_game_over():
    for col in range(GRID_COLUMNS):
        if grid[0][col] is not None:  
            return True  
    return False 

total_lines = 0  

def clear_lines():
    global grid, total_lines, score  

    new_grid = [row for row in grid if any(cell is None for cell in row)]  
    lines_cleared = GRID_ROWS - len(new_grid)  

    if lines_cleared > 0:
        total_lines += lines_cleared  
        score += lines_cleared * 100 
    while len(new_grid) < GRID_ROWS:
        new_grid.insert(0, [None] * GRID_COLUMNS)

    grid = new_grid

def draw_lines():
    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")

    font = pygame.font.Font(font_path, 28) 
    lines_text = font.render(f"LINES-{total_lines:03}", True, (255, 255, 255)) 

    screen.blit(lines_text, (292, 43)) 



def draw_score():
    font_path = os.path.join(os.path.dirname(__file__), "Font", "Pixel-Emulator.otf")

    font = pygame.font.Font(font_path, 30)  
    score_font = pygame.font.Font(font_path, 30)  
    
    score_text = font.render("SCORE", True, (255, 255, 255))  
    formatted_score = f"{score:06d}" 
    number_text = score_font.render(formatted_score, True, (255, 255, 255))  

    screen.blit(score_text, (537, 135))  
    screen.blit(number_text, (537, 159))  

piece_count = {key: 0 for key in TETROMINOS.keys()}  

def draw_statistics():
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

    def rotate(self):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        max_x = BOARD_X + BOARD_WIDTH - len(rotated_shape[0]) * GRID_SIZE
        max_y = BOARD_Y + BOARD_HEIGHT - len(rotated_shape) * GRID_SIZE

        if BOARD_X <= self.x <= max_x and BOARD_Y <= self.y <= max_y:
            self.shape = rotated_shape

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
        global score, current_piece, next_piece  

        score += 10 

        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_y = (self.y - BOARD_Y) // GRID_SIZE + row_idx
                    grid_x = (self.x - BOARD_X) // GRID_SIZE + col_idx
                    if 0 <= grid_y < GRID_ROWS and 0 <= grid_x < GRID_COLUMNS:
                        grid[grid_y][grid_x] = self.shape_type  

        clear_lines()

        if check_game_over():
            show_game_over()
            return  

        current_piece = next_piece  
        next_piece = Piece(random.choice(list(TETROMINOS.keys())))  
        piece_count[current_piece.shape_type] += 1  

        

def draw_grid():
    for x in range(BOARD_X, BOARD_X + BOARD_WIDTH + 1, GRID_SIZE): 
        pygame.draw.line(screen, (100, 100, 100), (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT))

    for y in range(BOARD_Y, BOARD_Y + BOARD_HEIGHT + 1, GRID_SIZE):
        pygame.draw.line(screen, (100, 100, 100), (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y))

def draw_next_piece():
    font_path = os.path.join(os.path.dirname(__file__), "Font", "tetris-font.ttf")

    font = pygame.font.Font(font_path, 28)


    next_x = 548 
    next_y = 333 

    if next_piece.shape_type == 'O':
        next_x = 557 
    if next_piece.shape_type == 'I':
        next_x = 533 

    for row_idx, row in enumerate(next_piece.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                screen.blit(next_piece.texture, (next_x + col_idx * GRID_SIZE, next_y + row_idx * GRID_SIZE))




current_piece = Piece(random.choice(list(TETROMINOS.keys())))
next_piece = Piece(random.choice(list(TETROMINOS.keys()))) 



current_piece = Piece(random.choice(list(TETROMINOS.keys())))
piece_count[current_piece.shape_type] += 1  
next_piece = Piece(random.choice(list(TETROMINOS.keys())))

score = 0  
running = True
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
    
    draw_statistics()
    draw_lines() 
    draw_next_piece()
    draw_score()  
    pygame.display.flip() 