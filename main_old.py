
import asyncio
import pygame
import os


# Initialize Pygame
pygame.init()


from globs import *
from gui import *
from draw import *





def collision_check(new_player_x, new_player_y): #, allow_dash_bonus = True):
    global player_x, player_y, player_vx, player_vy, player_animation_index, player_state, can_jump, \
     collected, collected_items, hovering, hover_counter
    # Check for collisions with adjacent tiles
    collided_x = False
    collided_y = False
    tile_x = int(player_x // TILE_SIZE)
    tile_y = int(player_y // TILE_SIZE)
    
    #dash_bonus = TILE_SIZE if (allow_dash_bonus and player_state == DASH) else 0  # go under tiles when dashing
    
    dash_bonus = TILE_SIZE if player_state == DASH and (player_animation_index > 5 or air_dash) else 0  # go under and slightly above tiles when dashing
    hover_bonus = TILE_SIZE/2 if player_state == HOVER else 0  # go slightly above tiles when hovering
    
    for x in range(tile_x - 2, tile_x + 3):
        for y in range(tile_y - 3, tile_y + 3):
            if x >= 0 and y >= 0 and x < len(tilemap[0]) and y < len(tilemap):
                tile = tilemap[y][x]
                if tile.solid():
               
                    # Check for collision on the left
                    if not collided_x and player_vx < 0:
                        if new_player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/4 > tile.x  and player_y + HALF_HEIGHT - dash_bonus/2 - hover_bonus/2 > tile.y and player_y - HALF_HEIGHT + dash_bonus < tile.y: 
                            if True: #allow_dash_bonus:  # dont alter if only testing check for dash retain under tiles
                                player_x = tile.x + TILE_SIZE + HALF_WIDTH/4
                                player_vx = 0
                            
                                if player_state == DASH:
                                    player_animation_index = 6
                                    # check two other tiles below it to see if the dash animation should end
                                    if y+1 < len(tilemap):
                                        tile2 = tilemap[y+1][x]
                                        if tile2.solid() and new_player_y + HALF_HEIGHT > tile2.y and new_player_y - HALF_HEIGHT < tile2.y:
                                            player_state = JUMPING
                                        elif y+2 < len(tilemap):
                                            tile3 = tilemap[y+2][x]
                                            if tile3.solid() and new_player_y + HALF_HEIGHT > tile3.y and new_player_y - HALF_HEIGHT < tile3.y:
                                                player_state = JUMPING 
                            collided_x = True
                    
                    # Check for collision on the right
                    elif not collided_x and player_vx > 0:
                        if new_player_x + HALF_WIDTH/4 > tile.x and new_player_x + HALF_WIDTH/4 < tile.x + TILE_SIZE and player_y + HALF_HEIGHT - dash_bonus/2 - hover_bonus/2 > tile.y and new_player_y - HALF_HEIGHT + dash_bonus < tile.y:
                            if True: #allow_dash_bonus:  # dont alter if only testing check for dash retain under tiles
                                player_x = tile.x - HALF_WIDTH/4
                                player_vx = 0
                            
                                if player_state == DASH:
                                    player_animation_index = 6
                                    # check two other tiles below it to see if the dash animation should end
                                    if y+1 < len(tilemap):
                                        tile2 = tilemap[y+1][x]
                                        if tile2.solid() and new_player_y + HALF_HEIGHT > tile2.y and new_player_y - HALF_HEIGHT < tile2.y:
                                            player_state = JUMPING
                                        elif y+2 < len(tilemap):
                                            tile3 = tilemap[y+2][x]
                                            if tile3.solid() and new_player_y + HALF_HEIGHT > tile3.y and new_player_y - HALF_HEIGHT < tile3.y:
                                                player_state = JUMPING 
                            collided_x = True
                    
                    # Check for collision on the top
                    if not collided_y and player_vy < 0:
                        if new_player_y - HALF_HEIGHT < tile.y + TILE_SIZE and new_player_y - HALF_HEIGHT > tile.y and player_x + HALF_WIDTH/4 > tile.x and player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:
                            player_y = tile.y + TILE_SIZE + HALF_HEIGHT
                            player_vy = 0
                            collided_y = True
                    
                    # Check for collision on the bottom
                    elif not collided_y and player_vy > 0:
                        if new_player_y + HALF_HEIGHT > tile.y and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE and player_x + HALF_WIDTH/4 > tile.x and player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:
                            player_y = tile.y - HALF_HEIGHT
                            player_vy = 0
                            collided_y = True
                            can_jump = True
                            if player_state == JUMPING:
                                player_state = LANDING
                                player_animation_index = 0
                                player_vx = player_vx / 2
                                print('switch to landing')
                            if player_state == HOVER:
                                player_state = STANDING
                            hovering = False
                            hover_counter = 0
                            
                            
    
    # Check for collisions with items
    for x in range(tile_x - 2, tile_x + 3):
        for y in range(tile_y - 3, tile_y + 3):
            if x >= 0 and y >= 0 and x < len(tilemap[0]) and y < len(tilemap):
                tile = tilemap[y][x]
                if tile.is_item():
                    # Check if the player is touching the item
                    if (new_player_x - HALF_WIDTH//3 < tile.x + TILE_SIZE and
                        new_player_x + HALF_WIDTH//3 > tile.x and
                        new_player_y - HALF_HEIGHT < tile.y + TILE_SIZE and
                        new_player_y + HALF_HEIGHT > tile.y):
                        # Erase item from screen
                        collected.add((current_room_x, current_room_y, x, y))  # Add the item's coordinates to the collected set
                        print('added ' + str(current_room_x) + ',' + str(current_room_y) + ',' + str(x) + ',' + str(y))
                        collected_items[tile.id] += 1  # Increment the number of H-items collected
                        tile.id = 0
                        redraw_room(tilemap, collected_items)
    
    return collided_x, collided_y
    
    
def dash_collision_check(new_player_x, new_player_y):
    tile_x = int(new_player_x // TILE_SIZE)
    tile_y = int(new_player_y // TILE_SIZE)
    
    for x in range(tile_x - 2, tile_x + 3):
        for y in range(tile_y - 3, tile_y + 3):
            if x >= 0 and y >= 0 and x < len(tilemap[0]) and y < len(tilemap):
                tile = tilemap[y][x]
                if tile.solid():
               
                    # Check for collision on the left
                    if new_player_x - HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/3 > tile.x  and player_y + HALF_HEIGHT > tile.y and player_y - HALF_HEIGHT < tile.y and \
                     not (new_player_x - HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/3 > tile.x  and player_y + HALF_HEIGHT > tile.y and player_y - HALF_HEIGHT < tile.y - TILE_SIZE): 
                        return True
                    
                    # Check for collision on the right
                    if new_player_x + HALF_WIDTH/3 > tile.x and new_player_x + HALF_WIDTH/3 < tile.x + TILE_SIZE and player_y + HALF_HEIGHT > tile.y and player_y - HALF_HEIGHT < tile.y and \
                     not (new_player_x + HALF_WIDTH/3 > tile.x and new_player_x + HALF_WIDTH/3 < tile.x + TILE_SIZE and player_y + HALF_HEIGHT > tile.y and player_y - HALF_HEIGHT < tile.y - TILE_SIZE):
                        return True
            



def load_tilemap(room_x, room_y):
    global tilemap, previous_tilemap #, previous_room_x, previous_room_y
    filename = f"{room_x}-{room_y}.txt"
    if not os.path.exists(filename):
        # Handle the case where the file does not exist
        print(f"Error: {filename} does not exist")
        return

    previous_tilemap = tilemap
    #previous_room_x = current_room_x
    #previous_room_y = current_room_y

    tilemap = []
    with open(filename, 'r') as f:
        for y, line in enumerate(f.readlines()):
            row = []
            for x, char in enumerate(line.strip()):
                #if is_item(char):
                #    print('item at ' + str(x) + ',' + str(y))
                if is_item(char) and (room_x, room_y, x, y) in collected:
                    row.append(Tile(x * TILE_SIZE, y * TILE_SIZE, '0'))
                else:
                    row.append(Tile(x * TILE_SIZE, y * TILE_SIZE, char))
            tilemap.append(row)


def cancel():
    redraw_room(tilemap, collected_items)


def initialize_game():
    global player_x, player_y, player_vy, player_vx, can_jump, player_state, player_facing, \
     current_room_x, current_room_y, transition_x, transition_y, player_animation_index, \
     stomping, collected, collected_items, hovering, hover_counter, air_dash, exploding_tile, \
     explosion_x, explosion_y, explosion_counter

    player_x, player_y = TILE_SIZE*2, TILE_SIZE*4
    player_vy = 0
    player_vx = 0
    can_jump = False
    stomping = False
    hovering = False
    hover_counter = 0
    player_state = STANDING
    player_facing = 1
    player_animation_index = 0
    current_room_x, current_room_y = 12, 11
    transition_x, transition_y = 0, 0
    collected = set()  # Use a set for efficient lookups
    collected_items = {'A': 0}  # number of each item that has been picked up
    exploding_tile = False
    explosion_x, explosion_y = 0, 0
    explosion_counter = 0

    load_tilemap(current_room_x, current_room_y)
    redraw_room(tilemap, collected_items)
    

async def main():
    global player_x, player_y, player_vy, player_vx, player_state, can_jump, player_facing, \
     current_room_x, current_room_y, transition_x, transition_y, player_animation_index, \
     stomping, previous_tilemap, hovering, hover_counter, air_dash, exploding_tile, \
     explosion_x, explosion_y, explosion_counter
     
    
    initialize_game()
    
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    await create_dialog_box(screen, "Restart game?", initialize_game, cancel)
                    
                elif player_state != DEAD and player_state != HIT and player_state != DASH:
                    
                    if event.key == pygame.K_d:  
                        player_state = DEAD
                        player_animation_index = 0
                    elif event.key == pygame.K_h:
                        player_state = HIT
                        player_animation_index = 0
                    elif event.key == pygame.K_g:
                        exploding_tile = True
                        explosion_x, explosion_y = 50,50
                        explosion_counter = 0
                        print('explosion_x=' + str(explosion_x) + ' explosion_y=' + str(explosion_y))
                        
                    # dash
                    elif event.key == pygame.K_a:
                        air_dash = True if player_state == JUMPING else False
                        player_state = DASH
                        player_vx = player_facing * DASH_VELOCITY
                        player_vy = 0
                        player_animation_index = 0
                    
                    # stomp
                    elif event.key == pygame.K_t and player_state == JUMPING and not stomping:
                        stomping = True
                        player_animation_index = 0
                        print('stomp')
                        player_vy = MAX_FALL_VELOCITY  # fall fast when stomping
                    
                      
                        
                    
                        
                        
                elif event.key == pygame.K_RETURN:
                    # Implement something here, e.g. restart the game
                    initialize_game()
                    
                


        # Move the player with Left and Right keys
        if player_state != LANDING and player_state != DEAD and \
         player_state != HIT:  # if not landing and not dead
            keys = pygame.key.get_pressed()
            
            # hover
            if keys[pygame.K_e]:
                # initiate hover_counter
                if not hovering and player_vy == 0 and player_state != JUMPING and hover_counter == 0:
                    print('initiate hover')
                    hovering = True
                    player_vy = -2
                    player_state = HOVER
                # sustain hover
                elif hovering:
                    hover_counter += 1
                    # if hover hasn't run out
                    if hover_counter >= HOVER_LIMIT:
                        player_vy = 0
                        hovering = False
                    # if hover elevation has reached max
                    elif hover_counter >= HOVER_ELEVATE_LIMIT:
                        player_vy = 0
                    # otherwise keep elevating
                    else:
                        player_vy = -.5
                    # stop hover
                    #if hover_counter == MAX_HOVER_COUNTER:
                    #   hovering = False
                    #    player_state = JUMPING
  
                else:
                    pass
                print('hovering=' + str(hovering) + ' player_vy=' + str(player_vy) + ' hover_counter=' + str(hover_counter))
            else:
                hovering = False

            
            # jump
            if keys[pygame.K_SPACE] and player_state != DASH:
                # initiate jump
                if can_jump:
                    player_vy = -JUMP_VELOCITY
                    can_jump = False
                    player_state = JUMPING
                    player_animation_index = 0
                    hovering = False
                # if player is jumping and holding down button then continue
                elif player_state == JUMPING:
                    pass
            # if player stops holding down jump button then end vertical velocity upwards
            elif player_state == JUMPING and player_vy < 0:
                player_vy = 0
    
            '''if keys[pygame.K_LEFT] and player_state == DASH and player_facing == 1:
                # stop a right dash by pressing left
                player_state = JUMPING
                player_animation_index = 0
                player_vx = 0
            elif keys[pygame.K_RIGHT] and player_state == DASH and player_facing == -1:
                # stop a a left dash by pressing right
                player_state = JUMPING
                player_animation_index = 0
                player_vx = 0
            '''
     
            # move left
            if keys[pygame.K_LEFT] and player_state != DASH and player_state != LANDING:
                if player_state == JUMPING:
                    player_facing = -1
                    player_vx -= AIRBORNE_ACCELERATION  # Decelerate when moving left while airborne
                elif player_state == HOVER:
                    player_facing = -1
                    player_vx -= HOVER_ACCELERATION 
                
                else:
                    player_facing = -1
                    player_vx -= ACCELERATION  # Accelerate/Decelerate
                    player_state = WALKING
                
                # Cap velocity
                if player_state != DASH and player_vx < -MAX_ACCELERATION:  
                    player_vx = -MAX_ACCELERATION
                elif player_state == DASH and player_vx < -DASH_VELOCITY:
                    player_vx = -DASH_VELOCITY
            
            
            # move right 
            elif keys[pygame.K_RIGHT] and player_state != DASH and player_state != LANDING:
                if player_state == JUMPING:
                    player_facing = 1
                    player_vx += AIRBORNE_ACCELERATION  # Accelerate when moving right while airborne
                elif player_state == HOVER:
                    player_facing = 1
                    player_vx += HOVER_ACCELERATION 
                    
                else:
                    player_facing = 1
                    player_vx += ACCELERATION  # Accelerate/Decelerate
                    player_state = WALKING
                 
                # Cap velocity
                if player_state != DASH and player_vx > MAX_ACCELERATION:  
                    player_vx = MAX_ACCELERATION
                elif player_state == DASH and player_vx > DASH_VELOCITY:
                    player_vx = DASH_VELOCITY
                    
            else: 
                # Decelerate when not moving
                if player_vx > 0:  
                    player_vx -= ACCELERATION * 2
                    
                    if player_vx < 0:
                        player_vx = 0       
                elif player_vx < 0:
                    player_vx += ACCELERATION * 2
                 
                    if player_vx > 0:
                        player_vx = 0
                        
                # stop walking animation when vx is 0
                if player_vx == 0 and player_state == WALKING:
                    player_state = STANDING

        # Check if the player has walked off a tile
        if player_vy >= 4:
            if player_state != JUMPING:
                player_animation_index = len(player_jumping_sprites) * player_jumping_animation_speed - 1
                stomping = False
                print('switch to falling')
            player_state = JUMPING
            hovering = False
            
            

        

        # Animate the player jumping
        if player_state == JUMPING:
            #print('before: ' + str(player_animation_index))    
            if stomping:
                if player_vy < 4 and player_animation_index < len(player_stomp_sprites) * player_stomp_animation_speed - 1:
                    player_animation_index = (player_animation_index + 1) % (len(player_stomp_sprites) * player_stomp_animation_speed)
                else:
                    player_animation_index = len(player_stomp_sprites) * player_stomp_animation_speed - 1
            else:
                if player_vy < 4 and player_animation_index < len(player_jumping_sprites) * player_jumping_animation_speed - 1:
                    player_animation_index = (player_animation_index + 1) % (len(player_jumping_sprites) * player_jumping_animation_speed)
                else:
                    player_animation_index = len(player_jumping_sprites) * player_jumping_animation_speed - 1
            #print('after: ' + str(player_animation_index))        
        # Animate the player walking
        elif player_state == WALKING:
            player_animation_index = (player_animation_index + 1) % (len(player_walking_sprites) * player_walking_animation_speed)
        #elif player_state != LANDING:
        #    player_walking_index = 0
        #    player_state = STANDING
        #    print('switch to standing')
        
        # Animate the player landing
        elif player_state == LANDING:
            player_animation_index += 1
            if player_animation_index >= len(player_landing_sprites) * player_landing_animation_speed:
                player_state = STANDING
                player_animation_index = 0
                player_vx = player_vx / 2
                hover_counter = 0
                print('finish landing')
                if stomping:
                    stomping = False
                    # get tile nearest feet
                    #print('player_x=' + str(player_x))
                    if player_facing == 1:
                        tile_x = int((player_x + TILE_SIZE/2) / TILE_SIZE)
                    else:
                        tile_x = int((player_x - TILE_SIZE/2) / TILE_SIZE)
                    tile_y = int((player_y + HALF_HEIGHT) // TILE_SIZE)
                    tile_x_2 = int(player_x / TILE_SIZE) # in case the first fails try a second tile
                    # try to stomp tile near foot
                    if tile_x >= 0 and tile_y >= 0 and tile_x < len(tilemap[0]) and tile_y < len(tilemap):
                        tile = tilemap[tile_y][tile_x]
                        print('stomp tile x=' + str(tile_x) + ', y=' + str(tile_y))
                        if tile.solid():
                            tile.id = 0
                            exploding_tile = True
                            explosion_counter = 0
                            explosion_x, explosion_y = tile_x*TILE_SIZE + TILE_SIZE/2, tile_y*TILE_SIZE + TILE_SIZE/2
                            player_state = STANDING
                    # try to stomp tile beneath player
                    if not exploding_tile and tile_x_2 >= 0 and tile_y >= 0 and tile_x_2 < len(tilemap[0]) and tile_y < len(tilemap):
                        tile = tilemap[tile_y][tile_x_2]
                        print('stomp tile x=' + str(tile_x_2) + ', y=' + str(tile_y))
                        if tile.solid():
                            tile.id = 0
                            exploding_tile = True
                            explosion_counter = 0
                            explosion_x, explosion_y = tile_x_2*TILE_SIZE + TILE_SIZE/2, tile_y*TILE_SIZE + TILE_SIZE/2
                            player_state = STANDING
                        
                        
                    
                
                
        # Animate the player death
        elif player_state == DEAD:
            if player_animation_index < len(player_death_sprites) * player_death_animation_speed - 1:
                player_animation_index += 1 
                
        # Animate the player getting hit
        elif player_state == HIT:
            if player_animation_index < len(player_hit_sprites) * player_hit_animation_speed - 1:
                player_animation_index += 1
            else:
                player_state = STANDING
                player_animation_index = 0
                
            # Move the player backwards 
            player_vx = -player_facing * TILE_SIZE / 20
            
        # Animate the player dashing
        elif player_state == DASH:
            if player_animation_index < (len(player_dash_sprites) - 1) * player_dash_animation_speed - 1:
                # if we're not on the second to last sprite then increment index
                player_animation_index += 1
            else:
                # we're on the second to last sprite. normally we end the dash here.
                # but if there is a tile above our head (player fits within two tiles heights)
                # then do NOT end the dash yet but instead retain the last frame of animation
                # and make the player slide until there is no tile above their head
                player_vx = player_facing
                if dash_collision_check(player_x + player_vx, player_y + player_vy):
                    # retain same animation frame
                    print('retain frame')
                    player_animation_index = len(player_dash_sprites) * player_dash_animation_speed - 1
                    player_vx = player_facing * 4.5
                else:
                    print('end dash')
                    player_state = JUMPING
                    player_animation_index = 0
                    player_vx = 0
        
        # Animate the player stomping
        #elif player_state == STOMP:
        #    if player_animation_index < len(player_stomp_sprites) * player_stomp_animation_speed - 1:
        #        player_animation_index += 1
        #    else:
        #        player_state = STANDING
        #        player_animation_index = 0
        # Animate the player getting hit
        elif player_state == HOVER:
            player_animation_index = (player_animation_index + 1) % (len(player_hover_sprites) * player_hover_animation_speed)
       
   
        
        
        
        # increase player velocities
        new_player_x = player_x + player_vx
        new_player_y = player_y + player_vy



        
        # do collision check                      
        collided_x, collided_y = collision_check(new_player_x, new_player_y)
        if not collided_x:
            player_x = new_player_x
        if not collided_y:
            player_y = new_player_y
            player_vy += GRAVITY
            if player_vy > MAX_FALL_VELOCITY:
                player_vy = MAX_FALL_VELOCITY

        
        if not collided_x or not collided_y:
            new_room_x, new_room_y = current_room_x, current_room_y
            
            # Determine the direction of the transition
            transition_direction_x = 0
            transition_direction_y = 0
            
            if player_x + HALF_WIDTH/2 > WIDTH:
                new_room_x += 1
                transition_direction_x = 1
                screen_offset_x, screen_offset_y = -WIDTH, 0
            elif player_x - HALF_WIDTH/2 < 0:
                new_room_x -= 1
                transition_direction_x = -1
                screen_offset_x, screen_offset_y = WIDTH, 0
            if player_y + HALF_WIDTH > HEIGHT:
                new_room_y += 1
                transition_direction_y = 1
                screen_offset_x, screen_offset_y = 0, -HEIGHT
            elif player_y < 0 + TILE_SIZE:
                new_room_y -= 1
                transition_direction_y = -1
                screen_offset_x, screen_offset_y = 0, HEIGHT
            
            # Start the transition
            if new_room_x != current_room_x or new_room_y != current_room_y:
                print('entering room x=' + str(new_room_x) + '-' + str(new_room_y))
            
                exploding_tile = False
                transition_x = transition_direction_x * WIDTH
                transition_y = transition_direction_y * HEIGHT
                
                previous_tilemap = tilemap  # Save the old room's tilemap
                load_tilemap(new_room_x, new_room_y) # Load the new room

                while abs(transition_x) > 0 or abs(transition_y) > 0:
                    
                    redraw_room_transitioning(tilemap, previous_tilemap, transition_x, transition_y, screen_offset_x, screen_offset_y)
       
                    redraw_player(player_x, player_y, player_facing, player_state, player_animation_index, stomping)
                    
                    # Update the transition progress
                    transition_x -= transition_speed * transition_direction_x
                    transition_y -= transition_speed * transition_direction_y

                    # Cap the transition progress
                    if transition_direction_x > 0 and transition_x < 0:
                        transition_x = 0
                    elif transition_direction_x < 0 and transition_x > 0:
                        transition_x = 0
                    if transition_direction_y > 0 and transition_y < 0:
                        transition_y = 0
                    elif transition_direction_y < 0 and transition_y > 0:
                        transition_y = 0
                     
                    # the player coordinates should be updated too
                    player_x -= transition_speed * transition_direction_x * .92
                    player_y -= transition_speed * transition_direction_y * .88
                    
                    # Update the display
                    pygame.display.update()
                    
                    # Wait for the next frame
                    await asyncio.sleep(0)
    
                
                redraw_room(tilemap, collected_items)
                
                # Update the current room
                current_room_x = new_room_x
                current_room_y = new_room_y
                
                previous_tilemap = []
                
                ''''
                # Reset the player position
                if transition_direction_x > 0:
                    player_x = TILE_SIZE
                elif transition_direction_x < 0:
                    player_x = WIDTH - TILE_SIZE
                if transition_direction_y > 0:
                    player_y = TILE_SIZE
                elif transition_direction_y < 0:
                    player_y = HEIGHT - TILE_SIZE
                '''
                
        
        
            # Clear the area around the player
            x1 = min(player_x - HALF_WIDTH*2, new_player_x - HALF_WIDTH*2, player_x + HALF_WIDTH*2, new_player_x + HALF_WIDTH*2)
            x2 = max(player_x - HALF_WIDTH*2, new_player_x - HALF_WIDTH*2, player_x + HALF_WIDTH*2, new_player_x + HALF_WIDTH*2)
            y1 = min(player_y - HALF_HEIGHT*2, new_player_y - HALF_HEIGHT*2, player_y + HALF_HEIGHT*2, new_player_y + HALF_HEIGHT*2)
            y2 = max(player_y - HALF_HEIGHT*2, new_player_y - HALF_HEIGHT*2, player_y + HALF_HEIGHT*2, new_player_y + HALF_HEIGHT*2)
            rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
            

            # Redraw room rect
            redraw_room_rect(tilemap, rect, collected_items)
            
            # Redraw player
            redraw_player(player_x, player_y, player_facing, player_state, player_animation_index, stomping)

        
            pygame.display.update(rect)
            
        
        
        if exploding_tile:
            if explosion_counter % EXPLOSION_ANIMATION_SPEED == 0:
        
                rect_radius = (TILE_SIZE+3)*2
                explosion_rect = pygame.Rect(explosion_x - rect_radius, explosion_y - rect_radius, rect_radius*2, rect_radius*2)
                redraw_room_rect(tilemap, explosion_rect, collected_items) # first clear that area
                
                if explosion_counter > EXPLOSION_COUNTER_LIMIT:  # end explosion
                    explosion_counter = 0
                    exploding_tile = False
                    
                
                if exploding_tile:  # if the tile is still exploding then draw it
                    redraw_explosion(explosion_x, explosion_y, explosion_counter)
                    
                pygame.display.update(explosion_rect)
              
            explosion_counter += 1
           
            
            
            

        await asyncio.sleep(0)
        
        
asyncio.run(main())





                
