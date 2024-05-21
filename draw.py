

import pygame
from random import randint


from globs import *


# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
BLUE = (100, 150, 255) 
RED = (250, 100, 100)



# Set up some constants
GATE_BLOCK_SIZE = 16
GATE_BLOCKS = 6




def draw_gate(tile, gate_y_offset):
    BORDER_WIDTH = 2
    GLIMMER_SIZE = 4
    GLIMMER_OFFSET = 2
    x, y = int(tile.x + TILE_SIZE/2 - 8), tile.y
    for i in range(GATE_BLOCKS):
        # Draw the block with a black border
        rect = pygame.Rect(x, max(y + i * GATE_BLOCK_SIZE - gate_y_offset, y), GATE_BLOCK_SIZE, GATE_BLOCK_SIZE)
        #pygame.draw.rect(screen, BLUE, rect)
        inner_rect = pygame.Rect(x + BORDER_WIDTH, max(y + i * GATE_BLOCK_SIZE - gate_y_offset + BORDER_WIDTH, y + BORDER_WIDTH), GATE_BLOCK_SIZE - BORDER_WIDTH * 2, GATE_BLOCK_SIZE - BORDER_WIDTH * 2)
        pygame.draw.rect(screen, GRAY, inner_rect)

        # Add a white patch of glimmer
        glimmer_rect = pygame.Rect(x + GATE_BLOCK_SIZE // 2 - GLIMMER_SIZE // 2 + GLIMMER_OFFSET, max(y + i * GATE_BLOCK_SIZE - gate_y_offset + GATE_BLOCK_SIZE // 2 - GLIMMER_SIZE // 2, y + GATE_BLOCK_SIZE // 2 - GLIMMER_SIZE // 2), GLIMMER_SIZE, GLIMMER_SIZE)
        pygame.draw.rect(screen, WHITE, glimmer_rect)

 
def draw_light_pillar(tile):
    origin_x, origin_y = tile.x, tile.y
    width, height = TILE_SIZE, TILE_SIZE
    for x in range(width):
        color = get_color_for_width(x, width)
        #pygame.draw.rect(screen, color, (x + origin_x, origin_y - height, 1, height))
        pygame.draw.rect(screen, color, (x + origin_x, origin_y, 1, height))

def get_color_for_width(x, pillar_width):
    time_sec = pygame.time.get_ticks() / 500  # convert to seconds
    hue = (math.sin(time_sec * 0.5) + 1) * 90  # Cycle hue within a narrower range 
    color = pygame.Color(0)

    # White stripe offset to the left of the center
    if x > (pillar_width // 4) and x < (pillar_width // 4) * 2:
        color = WHITE
    else:
        # Adjust the hue to get a strict range of blueish hues (between 180 to 240)
        hue = 180 + hue / 4
        color.hsla = (int(hue) % 360, 100, 50, 100)  # Full saturation, lightness at 50%

    return color
    
def draw_tile(tile, current_room_tuple = (0,0), tile_x = None, tile_y = None):
    x = tile_x if tile_x is not None else tile.x
    y = tile_y if tile_y is not None else tile.y
    #print(str(tile.x) + ',' + str(tile.y))
    
    #pygame.draw.rect(screen, (10,0,0), (x, y, TILE_SIZE, TILE_SIZE))  # Brown square
    #pygame.draw.rect(screen, TILE_COLOR, (x + 2, y + 2, TILE_SIZE -4, TILE_SIZE -4 ))  # Brown square
    

    # if tile_x, tile_y is provided then use that, otherwise use the tile's own x and y position
    tile_sprite = BLOCK_a
    
    if tile.id == 1:
        if (tile.x + tile.y + (current_room_tuple[0] // (current_room_tuple[1]+1) )) % 7 == 0 and \
         tile.x%2==0 and tile.y%3==0:
            tile_sprite = BLOCK_b
        elif (tile.x + tile.y + (current_room_tuple[0] // (current_room_tuple[1]+1) )) % 9 == 0 and \
         tile.y%2==0 and tile.x%3==0:
            tile_sprite = BLOCK_b
            
        elif (tile.x + tile.y + (current_room_tuple[1] // (current_room_tuple[0]+1) )) % 8 == 0 and \
         tile.y%2==0 and tile.x%3==0:
            tile_sprite = BLOCK_c
        elif (tile.x + tile.y + (current_room_tuple[1] // (current_room_tuple[0]+1) )) % 7 == 0 and \
         tile.x%2==0 and tile.y%3==0:
            tile_sprite = BLOCK_c
    
    elif tile.id == 2:
        tile_sprite = blocks[2]
    #if tile.id == 0 and in_map(x, y+TILE_SIZE, tilemap):
    #    tile_below = tilemap[y][tile_x] 
    #    if True or tile_below.appear_solid():
    #        tile_sprite = blocks[1]
    elif tile.id == 6:
        tile_sprite = blocks[6]
    elif tile.id == 7:
        tile_sprite = blocks[7]
        
    elif tile.id==3:
        tile_sprite = blocks[3]
        
    elif tile.id==4:
        tile_sprite = blocks[4]
    elif tile.id==5:
        tile_sprite = blocks[5]
    elif tile.id==8:
        tile_sprite = blocks[8]
    
    screen.blit(tile_sprite, (x, y))  # Draw tile
    

#def draw_item(tile):
#    font = pygame.font.Font(None, TILE_SIZE)  # Use a font with the same size as TILE_SIZE
#    text = font.render('H', True, (255, 255, 255))  # White letter 'H'
#    screen.blit(text, (tile.x, tile.y))
   
   

def draw_item(tile, last_item_animation_time = 0):
    #global last_item_animation_time
    x, y = tile.x, tile.y

    current_time = pygame.time.get_ticks()
    if current_time - last_item_animation_time >= 100:  # 100ms = 10 frames per second
        last_item_animation_time = current_time

        # Draw a hexagon
        points = [(x + 16, y), (x + 32, y + 8), (x + 32, y + 24), (x + 16, y + 32), (x, y + 24), (x, y + 8)]
        pygame.draw.polygon(screen, RED, points)
        pygame.draw.polygon(screen, WHITE, points, 2)

        # Draw a letter 'D'
        item_surf = item_font.render(tile.id, True, WHITE)
        item_rect = item_surf.get_rect()
        item_rect.center = (x + 16, y + 17)  # Adjusted the center to make it look more centered
        screen.blit(item_surf, item_rect)

        # Animate the border
        for i in range(6):
            pygame.draw.line(screen, (255,160,160), points[i], points[(i + 1) % 6], 2)
        i = (current_time // 100) % 6
        pygame.draw.line(screen, WHITE, points[i], points[(i + 1) % 6], 2)

        pygame.display.flip()

def draw_system_text(collected_items):
    font = pygame.font.Font(None, 32)
    #text = font.render(f"Hover: {collected_items['U']}", True, (255, 255, 255))
    #screen.blit(text, (WIDTH - 150, 10))
    
    #print(str(text.get_width()) + ',' + str(text.get_height()))

def redraw_room(tilemap, current_room_tuple, collected_items, gate_y_offset, item_in_room):
    #screen.blit(background_image, (0, 0))  # Draw background image
    #pygame.draw.rect(screen,(0,0,250),(0,0,WIDTH,HEIGHT))
    
    # Clear the screen
    #screen.fill((0, 0, 250))
    screen.blit(background_image, (0, 0))  # Draw background image
    
    for row in tilemap:
        for tile in row:
            if tile.appear_solid():
                draw_tile(tile, current_room_tuple)
            if tile.is_item() and item_in_room:
                draw_item(tile)
            if tile.id == 'P':
                draw_light_pillar(tile)
            if tile.id == 'G':
                draw_gate(tile, gate_y_offset)
                
    draw_system_text(collected_items)
                              
def redraw_room_rect(tilemap, current_room_tuple, rect, collected_items, gate_y_offset, item_in_room):
    #pygame.draw.rect(screen,(0,0,250),rect)
    #obstacle_rect = pygame.Rect(obstacle_x, height + obstacle_gap, obstacle_width, bottom_obstacle_height)
    #image_rect = obstacle_image.get_rect(center = obstacle_rect.center)
    #screen.blit(screen,(0,0)) # Redraw background image
    
    clipped_rect = rect.clamp(screen.get_rect())
    if background_image.get_rect().contains(clipped_rect):
        background_image_clipped = background_image.subsurface(clipped_rect)
        screen.blit(background_image_clipped, rect)  # Draw background image
    
    # Redraw tiles
    for row in tilemap:
        for tile in row:
            if tile.appear_solid() and rect.colliderect(pygame.Rect(tile.x, tile.y, TILE_SIZE, TILE_SIZE)):
                draw_tile(tile, current_room_tuple)
            if tile.is_item() and rect.colliderect(pygame.Rect(tile.x, tile.y, TILE_SIZE, TILE_SIZE)) and \
             item_in_room:
                    draw_item(tile) 
            if tile.id == 'P':
                draw_light_pillar(tile)
            if tile.id == 'G':
                draw_gate(tile, gate_y_offset)
    
    if rect.colliderect(pygame.Rect(WIDTH - 150, 10, 100, 30)):
        draw_system_text(collected_items)
   
    
def redraw_room_transitioning(tilemap, previous_tilemap, current_room_tuple, new_room_tuple, transition_x, transition_y, screen_offset_x, screen_offset_y):
    # Clear the screen
    #screen.fill((0, 0, 250))
    screen.blit(background_image, (0, 0))  # Draw background image
    
    # Draw the old room at its current position
    for row in previous_tilemap:
        for tile in row:
            if tile.appear_solid():
                x, y = tile.x + screen_offset_x + transition_x, tile.y + screen_offset_y + transition_y
                #if x >= 0 and y >= 0 and x < WIDTH - TILE_SIZE and y < HEIGHT - TILE_SIZE:
                draw_tile(tile, current_room_tuple, x, y)


    '''
    goobers = True
    while goobers:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                goobers = False
        
    
    pygame.display.update()
    print('finish first loop')
    '''
    
    # Draw the new room at its current position
    for row in tilemap:
        for tile in row:
            if tile.appear_solid():
                x, y = tile.x + transition_x, tile.y + transition_y
                #if x >= 0 and y >= 0 and x < WIDTH - TILE_SIZE and y < HEIGHT - TILE_SIZE:
                draw_tile(tile, new_room_tuple, x, y)  

    '''
    goobers = True
    while goobers:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                goobers = False
                
    pygame.display.update()
    print('finish second loop')
    '''        

NUM_DOTS_IN_EXPLOSION = 50
def redraw_explosion(explosion_x, explosion_y, explosion_counter):
    radius = explosion_counter//EXPLOSION_ANIMATION_SPEED * 3
    for _ in range(NUM_DOTS_IN_EXPLOSION):  # Number of dots in the explosion
        x = explosion_x + randint(-radius, radius)
        y = explosion_y + randint(-radius, radius)
        #pygame.draw.circle(screen, WHITE, (x, y), 2)
        pygame.draw.rect(screen, WHITE, (x-1,y-1,3,3))
  

    

def redraw_player(player_x, player_y, player_facing, player_state, player_animation_index, stomping, reverse_gravity):
    
    try:
        if player_state == JUMPING:
            if stomping:
                player_sprite = player_stomp_sprites[player_animation_index // player_stomp_animation_speed]
            else:
                player_sprite = player_jumping_sprites[player_animation_index // player_jumping_animation_speed]
            #else:
            #    player_sprite = player_jumping_sprites[-1]
        elif player_state == WALKING:
            player_sprite = player_walking_sprites[player_animation_index // player_walking_animation_speed]
        elif player_state == LANDING:
            player_sprite = player_landing_sprites[player_animation_index // player_landing_animation_speed]
            
        elif player_state == STANDING:
            player_sprite = player_stationary_sprite
        elif player_state == DEAD:
            player_sprite = player_death_sprites[player_animation_index // player_death_animation_speed]
        elif player_state == HIT:
            player_sprite = player_hit_sprites[player_animation_index // player_hit_animation_speed]
        elif player_state == DASH:
            player_sprite = player_dash_sprites[player_animation_index // player_dash_animation_speed]
        elif player_state == HOVER:
            player_sprite = player_hover_sprites[player_animation_index // player_hover_animation_speed]
        elif player_state == WALKING_UP:
            player_sprite = player_walking_up_sprites[player_animation_index // player_walking_animation_speed]
        elif player_state == WALKING_DOWN:
            player_sprite = player_walking_down_sprites[player_animation_index // player_walking_animation_speed]
    
    except:
        player_sprite = player_walking_sprites[0]
    
    
    if reverse_gravity:
        player_sprite = pygame.transform.flip(player_sprite, False, True) 

    
    player_sprite_flipped = pygame.transform.flip(player_sprite, player_facing == -1, False)
    screen.blit(player_sprite_flipped, (int(player_x - HALF_WIDTH), int(player_y - HALF_HEIGHT)))  # Draw player sprite



