


import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import copy


# Initialize Pygame
pygame.init()

# Set up some constants
TILESET_FILE = "Tiles_32x32-purple.png" 
#TILESET_FILE = "Tiles_32x32.png"
WIDTH, HEIGHT = 1285, 680
TILE_SIZE = 32
MAP_X = 300
ROWS, COLUMNS = 20, 30

class Tile:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

def load_map(filename):
    if not os.path.exists(filename):
        # Handle the case where the file does not exist
        print(f"Error: {filename} does not exist")
        return

    map = []
    with open(filename, 'r') as f:
        for y, line in enumerate(f.readlines()):
            row = []
            for x, char in enumerate(line.strip()):
                row.append(Tile(x * TILE_SIZE, y * TILE_SIZE, char))
            map.append(row)
    return map

def select_file():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    return filename

def save_map(map, filename):
    with open(filename, 'w') as f:
        for row in map:
            line = ''.join(tile.char for tile in row) + '\n'
            f.write(line)
            
    global map_filename
    map_filename = filename
    redraw_screen()

def map_char_to_sprite(char):
    char_to_sprite = {
        
        "1": (0, 4),
        "2": (0, 0),
        "3": (6, 0),
        "4": (0, 6),
        "5": (1, 6),
        "6": (0, 7),
        "7": (4, 2),
        "8": (7, 5),
        #"8": (2, 3),
        #"9": (3, 3),
    }
    return char_to_sprite.get(char)
    
def map_sprite_to_char(sprite):
    sprite_to_char = {
        (0, 4): "1",
        (0, 0): "2",
        (6, 0): "3",
        (0, 6): "4",
        (1, 6): "5",
        (0, 7): "6",
        (4, 2): "7",
        (7, 5): "8",
        #(2, 3): "8",
        #(3, 3): "9",
    }
    return sprite_to_char.get(sprite)

# Load tileset
tileset_image = pygame.image.load(TILESET_FILE)
tileset_sprites = []
for y in range(0, tileset_image.get_height(), TILE_SIZE):
    row = []
    for x in range(0, tileset_image.get_width(), TILE_SIZE):
        sprite = tileset_image.subsurface((x, y, TILE_SIZE, TILE_SIZE))
        row.append(sprite)
    tileset_sprites.append(row)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Set up the selected tile
selected_tile = None

# Set up the map
#map = None
map_filename = ''
map = [[Tile(x * TILE_SIZE, y * TILE_SIZE, '0') for x in range(COLUMNS)] for y in range(ROWS)]
            

show_grid = True

def draw_text(screen, font, text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

def draw_grid(screen):
    if not show_grid:
        return
    for x in range(0, (COLUMNS+1) * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (MAP_X + x, 0), (MAP_X + x, ROWS * TILE_SIZE))
    for y in range(0, (ROWS+1) * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (MAP_X, y), (MAP_X + COLUMNS * TILE_SIZE, y))

def draw_button(screen, font, text, x, y):
    pygame.draw.rect(screen, (100, 100, 100), (x, y, 70, 30))
    draw_text(screen, font, text, x + 10, y + 5)

def draw_map(screen, map):
    if map is not None:
        for row in map:
            for tile in row:
                if tile.char != "0":
                    sprite_coords = map_char_to_sprite(tile.char)
                    if sprite_coords is not None:
                        sprite = tileset_sprites[sprite_coords[1]][sprite_coords[0]]
                        screen.blit(sprite, (tile.x + MAP_X, tile.y))
                    elif len(tile.char)==1:
                        draw_text(screen, font, tile.char, tile.x + MAP_X, tile.y)

def draw_tileset(screen):
    screen.fill((0, 0, 0))
    for y, row in enumerate(tileset_sprites):
        for x, sprite in enumerate(row):
            screen.blit(sprite, (x * TILE_SIZE, y * TILE_SIZE))
            if (x, y) == selected_tile:  # Highlight the selected tile
                pygame.draw.rect(screen, (255, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # Add an empty tile to the right of the tileset on the last row
    pygame.draw.rect(screen, (100, 100, 100), (len(tileset_sprites[0]) * TILE_SIZE, (len(tileset_sprites) - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    if selected_tile == (len(tileset_sprites[0]), len(tileset_sprites) - 1):  # Highlight the empty tile if it is selected
        pygame.draw.rect(screen, (255, 0, 0), (len(tileset_sprites[0]) * TILE_SIZE, (len(tileset_sprites) - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def redraw_screen():
    screen.fill((0, 0, 0))
    draw_tileset(screen)
    draw_button(screen, font, "Load", 10, len(tileset_sprites) * TILE_SIZE + 20)
    draw_button(screen, font, "New", 90, len(tileset_sprites) * TILE_SIZE + 20)
    draw_button(screen, font, "Save", 170, len(tileset_sprites) * TILE_SIZE + 20)
    draw_button(screen, font, "Grid", 170, len(tileset_sprites) * TILE_SIZE + 20 + 50)
    draw_button(screen, font, "Undo", 90, len(tileset_sprites) * TILE_SIZE + 70)
    if map_filename:
        filename = os.path.basename(map_filename)  # Only display the file name
        draw_text(screen, small_font, filename, 10, len(tileset_sprites) * TILE_SIZE + 120)
    draw_map(screen, map)
    draw_grid(screen)
    pygame.display.flip()



action_history = []


redraw_screen()

mouse_down = False



# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
           
        
            # Get the tile that was clicked
            x, y = event.pos
            
            if x < len(tileset_sprites[0]) * TILE_SIZE + TILE_SIZE and y < len(tileset_sprites) * TILE_SIZE:  # Check if the click was on the tileset
                tile_x = x // TILE_SIZE
                tile_y = y // TILE_SIZE
                if (0 <= tile_y < len(tileset_sprites) and 
                    0 <= tile_x < len(tileset_sprites[0])):
                    selected_tile = (tile_x, tile_y)
                elif (tile_x == len(tileset_sprites[0]) and 
                      tile_y == len(tileset_sprites) - 1):  # Check if the empty tile was clicked
                    selected_tile = (tile_x, tile_y)
                print(f"Selected tile at ({tile_x}, {tile_y})")
                redraw_screen()  # Redraw the screen to show the selected tile
            
            # load
            elif 10 < x < 80 and len(tileset_sprites) * TILE_SIZE + 20 < y < len(tileset_sprites) * TILE_SIZE + 50:  # Check if the click was on the "Load" button
                filename = select_file()
                if filename:
                    map = load_map(filename)
                    map_filename = filename
                    redraw_screen()
            
            # new
            elif 90 < x < 160 and len(tileset_sprites) * TILE_SIZE + 20 < y < len(tileset_sprites) * TILE_SIZE + 50:  # Check if the click was on the "New" button
                layers = simpledialog.askinteger("New Map", "Enter the number of layers around the map:")
                if layers is not None:
                
                    fill_char = '1'
                    if selected_tile is not None:
                        x, y = selected_tile[1], selected_tile[0]
                        tup = (y,x)
                        char = map_sprite_to_char(tup)
                        if char in [str(i) for i in range(1, 10)]:
                            fill_char = char
                        
                        
                    map = [[Tile(x * TILE_SIZE, y * TILE_SIZE, '0' if x >= layers and x < COLUMNS - layers and y >= layers and y < ROWS - layers else fill_char) for x in range(COLUMNS)] for y in range(ROWS)]
                    map_filename = ''
                    redraw_screen()
            
            # save
            elif 170 < x < 240 and len(tileset_sprites) * TILE_SIZE + 20 < y < len(tileset_sprites) * TILE_SIZE + 50:  # Check if the click was on the "Save" button
                if map is not None:
                    filename = filedialog.asksaveasfilename(initialfile = map_filename)
                    #filename = filedialog.asksaveasfile(initialfile = map_filename)
                    if filename:
                        save_map(map, filename)
              
            # grid
            elif 170 < x < 240 and len(tileset_sprites) * TILE_SIZE + 20 + 50 < y < len(tileset_sprites) * TILE_SIZE + 50 + 50:  # Check if the click was on the "Grid" button
                show_grid = not show_grid
                redraw_screen()
                
            # undo
            elif 90 < x < 160 and len(tileset_sprites) * TILE_SIZE + 70 < y < len(tileset_sprites) * TILE_SIZE + 100:  # Check if the click was on the "Undo" button
                if len(action_history) > 0:
                    map = action_history.pop()
                    redraw_screen()
            
            elif MAP_X <= x < MAP_X + COLUMNS * TILE_SIZE and 0 <= y < ROWS * TILE_SIZE:  # Check if the click was on the map
                mouse_down = True
                action_history.append(copy.deepcopy(map))  # Add the current state to the history
            else:
                mouse_down = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        
        if mouse_down:
            x, y = pygame.mouse.get_pos()
            
            
            if MAP_X <= x < MAP_X + COLUMNS * TILE_SIZE and 0 <= y < ROWS * TILE_SIZE:  # Check if the click was on the map
                if selected_tile is not None:
                    map_x = (x - MAP_X) // TILE_SIZE
                    map_y = y // TILE_SIZE
                    
                    print('map_x=' + str(map_x) + ' map_y=' + str(map_y))
                    
                    if selected_tile == (len(tileset_sprites[0]), len(tileset_sprites) - 1):  # If the empty tile was selected
                        
                        
                        if len(action_history) > 10:  # Limit the number of undo actions
                            action_history.pop(0)
                        
                        map[map_y][map_x].char = '0'
                        
                  
                        
                    else:
                        x, y = selected_tile[1], selected_tile[0]
                        tup = (y,x)
                        print(str(tup))
                        char = map_sprite_to_char(tup)
                        
                        if char in [str(i) for i in range(1, 10)]:
                            
                            
                            if len(action_history) > 10:  # Limit the number of undo actions
                                action_history.pop(0)
                            
                            #char = str(selected_tile[1] * len(tileset_sprites[0]) + selected_tile[0] + 1)
                            map[map_y][map_x].char = char
    
                            

                    
                redraw_screen()  # Redraw the screen to show the updated map          
                
  
        
            
    