
import asyncio
import math
import pygame
import os
import copy


game = None


# Set up some constants
WIDTH, HEIGHT = 960, 640  # 1024, 768
ROOM_WIDTH, ROOM_HEIGHT = 30, 20  # how many tiles across and down in a room
TILE_SIZE = 32
TILE_COLOR = (19,69,139)
#PLAYER_RADIUS = TILE_SIZE // 2
#STARTING_ROOM_X, STARTING_ROOM_Y = 100,99
STARTING_ROOM_X, STARTING_ROOM_Y = 100,98
STARTING_X, STARTING_Y = 400, 200  # TILE_SIZE*2, TILE_SIZE*4
JUMP_VELOCITY = 7   #5.5
GRAVITY = .25
MAX_FALL_VELOCITY = 10
ACCELERATION = 0.2 # Horizontal acceleration
MAX_VELOCITY = 3.8
MAX_JUMP_VELOCITY = 2.5  # so that the player can't jump too far horizontally
AIRBORNE_ACCELERATION = 0.2  # New constant for airborne acceleration
HOVER_ACCELERATION = 0.22 
HOVER_ELEVATE_LIMIT = 58
HOVER_LIMIT = 68
DASH_VELOCITY = 10
player_walking_animation_speed = 5  # Change this value to adjust the speed of the walking animation
player_jumping_animation_speed = 6  # Change this value to adjust the speed of the jumping animation
player_landing_animation_speed = 6
player_death_animation_speed = 6
player_hit_animation_speed = 6
player_dash_animation_speed = 5
player_stomp_animation_speed = 5
player_hover_animation_speed = 13
transition_speed = 14 
EXPLOSION_COUNTER_LIMIT = 24
EXPLOSION_ANIMATION_SPEED = 2

item_font = pygame.font.Font(None, 36)



DASH_KEY = pygame.K_d
STOMP_KEY = pygame.K_s
HOVER_KEY = pygame.K_h
JUMP_KEY = pygame.K_SPACE
RESTART_KEY = pygame.K_r
DIE_KEY = pygame.K_F1


CHEATS_ON = False


# player states
STANDING = 0
WALKING = 1
JUMPING = 2
LANDING = 4
DEAD = 5
HIT = 6
DASH = 7
HOVER = 8
WALKING_UP = 9  # walking up a slope
WALKING_DOWN = 10 # walkiing down a slope



TILESET_FILE = "Tiles_32x32-purple.png"
#TILESET_FILE = "Tiles_32x32-alt.png"
HERO_FILE = "hero.png"
BACK_FILE = "back.jpg" #"BackgroundGradient.png"



def load_sprite(filename):
    path = os.path.join("sprites", filename)
    return pygame.image.load(path)
    
# Load background image
background_image = load_sprite(BACK_FILE)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))







def is_item(char):
    return char in ['A', 'D', 'S', 'H', 'R', 'K', 'E']  # Add more item IDs here
    
class Tile:
    def __init__(self, x, y, char='0'):
        self.x = x
        self.y = y
        try:
            self.id = int(char)
        except:
            #print('cant convert ' + char + ' to int')
            self.id = char
       
    def appear_solid(self):
        if self.id == 0 or is_item(self.id) or self.id=='P' or self.id=='G':
            return False  
           
        return True
        
    def solid(self):
        # empty space
        if self.id == 0:
            return False
        # most blocks are solid
        if self.id == 1 or self.id == 2 or self.id == 3 or self.id == 4 or self.id == 5 or self.id == 8:
            return True
        # diagonals
        if self.id == 6 or self.id == 7 or self.id == 8 or self.id == 9:
            return True
        # illusory block
        if self.id == 'Z':
            return False
        #if is_item(self.id):
        #    return False
        
            
        return False
     
    def breakable(self):
        return True if self.id == 3 else False
     
    def is_item(self):
        return is_item(self.id)
            


tilemap = []
previous_tilemap = []



# Load tileset
tileset_image = load_sprite(TILESET_FILE)
tileset_sprites = []
#print('w=' + str(tileset_image.get_width()) + ' h=' + str(tileset_image.get_height()))
for y in range(0, tileset_image.get_height(), 32):
    row = []
    for x in range(0, tileset_image.get_width(), 32):
        sprite = tileset_image.subsurface((x, y, 32, 32))
        row.append(sprite)
    tileset_sprites.append(row)

blocks = []
'''
blocks.append(tileset_sprites[0][1])
blocks.append(tileset_sprites[3][0]) # 1 common block
blocks.append(tileset_sprites[4][4]) # 2 common block with icing
blocks.append(tileset_sprites[0][2])
blocks.append(tileset_sprites[0][3])
blocks.append(tileset_sprites[0][4])
blocks.append(tileset_sprites[3][2]) # 6 slope up to right
blocks.append(tileset_sprites[3][3]) # 7 slope up to left
'''
blocks.append(tileset_sprites[0][0])
blocks.append(tileset_sprites[0][4]) # 1 common block
blocks.append(tileset_sprites[0][0]) # 2 common block with icing
blocks.append(tileset_sprites[0][6]) # 3 common blocky block
blocks.append(tileset_sprites[6][0]) # 4 block with pink splotch
blocks.append(tileset_sprites[6][1]) # 5 block with brown splotch
blocks.append(tileset_sprites[7][0]) # 6 slope up to right
blocks.append(tileset_sprites[2][4]) # 7 slope up to left
blocks.append(tileset_sprites[5][7]) # 8 block with alternate pink splotch
#blocks.append(tileset_sprites[3][2]) # 8 slope down to right
#blocks.append(tileset_sprites[3][3]) # 9 slope down to left

BLOCK_a = blocks[1]
BLOCK_b = copy.deepcopy(BLOCK_a)
BLOCK_b.fill((20, 20, 20, 20), special_flags=pygame.BLEND_ADD) # slightly lighter 
BLOCK_c = copy.deepcopy(BLOCK_a)
BLOCK_c.fill((12, 12, 12, 0), special_flags=pygame.BLEND_SUB) # slightly darker


# Load hero image
hero_image = load_sprite(HERO_FILE)
hero_sprites = []
for y in range(0, hero_image.get_height(), 64):
    row = []
    for x in range(0, hero_image.get_width(), 64):
        sprite = hero_image.subsurface((x, y, 64, 64))
        row.append(sprite)
    hero_sprites.append(row)

player_sprite = hero_sprites[8][0]  # Get the bottommost sprite on the left of the 9th row
PLAYER_WIDTH = player_sprite.get_width()
PLAYER_HEIGHT = player_sprite.get_height()
HALF_WIDTH = PLAYER_WIDTH/2
HALF_HEIGHT = PLAYER_HEIGHT/2

player_stationary_sprite = hero_sprites[8][0]  # Original sprite
player_walking_sprites = hero_sprites[4]  # 5th row of sprites
player_jumping_sprites = hero_sprites[5][2:]  # 6th row of sprites, excluding the first two
player_landing_sprites = [hero_sprites[5][1],hero_sprites[5][0]]  # 6th row of sprites, only the first two in reverse order
player_death_sprites = hero_sprites[2]  # 3rd row of sprites
player_hit_sprites = hero_sprites[3][:4]  # First four sprites of the 4th row
#player_dash_sprites = hero_sprites[1][:6] # all 8 sprites on the 2nd row
#player_dash_sprites = [hero_sprites[1][0], hero_sprites[1][1], hero_sprites[1][2], \
# hero_sprites[1][3], hero_sprites[1][5], hero_sprites[1][6], hero_sprites[1][7]]
player_dash_sprites = [hero_sprites[0][4], hero_sprites[0][5], hero_sprites[0][6], \
 hero_sprites[0][7], hero_sprites[1][5], hero_sprites[1][6], hero_sprites[1][7]]
player_stomp_sprites = [hero_sprites[7][3], hero_sprites[7][2], hero_sprites[7][0], hero_sprites[7][0], hero_sprites[7][0]]
player_hover_sprites = [hero_sprites[6][7], hero_sprites[6][4], hero_sprites[6][5], hero_sprites[6][6]]
player_walking_up_sprites = hero_sprites[6]
player_walking_down_sprites = hero_sprites[7]
     
     


class Game:
    def __init__(self):
        self.player_x, self.player_y = STARTING_X, STARTING_Y  
        self.player_vy, self.player_vx = 0, 0
        self.can_jump = False
        self.stomping = False
        self.hovering = False
        self.hover_counter = 0
        self.air_dash = False
        
        self.player_state = STANDING
        self.collected = set()  # Use a set for efficient lookups
        self.collected_items = {} #{'A': 0}  # number of each item that has been picked up
        
        self.player_facing = 1  # 1 for right, -1 for left
        
        self.player_animation_index = 0
        self.current_room_x, self.current_room_y = STARTING_ROOM_X, STARTING_ROOM_Y
        self.previous_room_x, self.previous_room_y = self.current_room_x, self.current_room_y
        self.transition_x, self.transition_y = 0, 0
        self.explosion_x, self.explosion_y = 0, 0
        self.exploding_tile = False
        self.explosion_counter = 0
        self.reverse_gravity = False
        
        self.gate_open = {}
        #self.gate_open[(12,11)] = False
        #self.gate_open[(103,99)] = False
        self.gate_open[(99,98)] = False
        self.gate_open[(103,96)] = False
        self.gate_open[(101,98)] = False
        self.animate_gate = False
        self.gate_y_offset = 0
        
        self.item_in_room = False
        self.animate_item_tile = None
        self.last_item_animation_time = 0
        
        self.fading_message = ""
        self.fading_message_counter = 850

        # if we need to cheat
        if CHEATS_ON:
            self.collected_items['D'] = 1
            self.collected_items['H'] = 1
            self.collected_items['S'] = 1
            self.collected_items['R'] = 1
            self.collected_items['K'] = 1
            self.collected_items['A'] = 1
        self.collected_items['D'] = 1
        self.collected_items['H'] = 1
        self.collected_items['S'] = 1
        self.collected_items['R'] = 1
        self.collected_items['A'] = 1

    def reset_some_stuff(self):
        self.player_x, self.player_y = STARTING_X, STARTING_Y  
        self.player_vy, self.player_vx = 0, 0
        self.can_jump = False
        self.stomping = False
        self.hovering = False
        self.hover_counter = 0
        self.air_dash = False
        self.player_state = STANDING
        self.current_room_x, self.current_room_y = STARTING_ROOM_X, STARTING_ROOM_Y
        self.previous_room_x, self.previous_room_y = self.current_room_x, self.current_room_y
        self.player_facing = 1  # 1 for right, -1 for left
        self.player_animation_index = 0
        

def in_map(x, y, tilemap):
    if x >= 0 and y >= 0 and x < len(tilemap[0]) and y < len(tilemap):
        return True
    return False


def item_title(id):
    if id=='A': return "Air Dash"
    if id=='D': return "Dash"
    if id=='H': return "Hover"
    if id=='S': return "Stomp"
    if id=='R': return "Reverse Gravity Tool"
    if id=='K': return "Gate Key"
    if id=='E': return "End of demo"
    return ""
    
def tutorial(id):
    if id=='1': return "Press LEFT and RIGHT to move"
    if id=='2': return "Hold SPACE to jump"
    if id=='3': return "Press F1 to die (in the case of getting stuck)"
    if id=='A': return "Press D to dash while airborne"
    if id=='D': return "Press D to dash"
    if id=='H': return "Hold H to hover"
    if id=='S': return "Press S while airborne to stomp"
    if id=='K': return ""
    if id=='E': return "This is as much as I've made! You can stop playing"
    return ""
    
    

