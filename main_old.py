
import asyncio
import pygame
import os


# Initialize Pygame
pygame.init()


from globs import *
from gui import *
from draw import *
from collision import *







def load_tilemap(room_x, room_y):
    global tilemap, previous_tilemap #, game.previous_room_x, game.previous_room_y
    filename = f"{room_x}-{room_y}.txt"
    
    path = os.path.join("maps", filename)
    if not os.path.exists(path):
        # Handle the case where the file does not exist
        print(f"Error: {path} does not exist")
        return

    previous_tilemap = tilemap
    #game.previous_room_x = game.current_room_x
    #game.previous_room_y = game.current_room_y

    tilemap = []
    with open(path, 'r') as f:
        for y, line in enumerate(f.readlines()):
            row = []
            for x, char in enumerate(line.strip()):
                #if is_item(char):
                #    print('item at ' + str(x) + ',' + str(y))
                if is_item(char) and (room_x, room_y, x, y) in game.collected:
                    row.append(Tile(x * TILE_SIZE, y * TILE_SIZE, '0'))
                else:
                    row.append(Tile(x * TILE_SIZE, y * TILE_SIZE, char))
            tilemap.append(row)


def cancel():
    redraw_room(tilemap, (game.current_room_x,game.current_room_y), game.collected_items, game.gate_y_offset, game.item_in_room)


def toggle_music(play = False):
    if game.music_on and not play:
        pygame.mixer.music.stop()
        game.music_on = False
    else:
        music_path = "Words_be.mid"
        pygame.mixer.music.load(music_path)
        try:
            pygame.mixer.music.play(-1)
            game.music_on = True
        except:
            print('cant load music')
            game.music_on = False

def initialize_game(save_progress = False):
    global game
    
    if save_progress:
        game.reset_some_stuff()
    else:
        game = Game()

    load_tilemap(game.current_room_x, game.current_room_y)
    enter_room(game.current_room_x, game.current_room_y)
   
    toggle_music(True)
   
def enter_room(x, y):
    # Update the current room
    print('entering room ' + str(x) + '-' + str(y))
    game.current_room_x = x
    game.current_room_y = y
    
    # gate
    game.gate_y_offset = 0
    if (x,y) in game.gate_open.keys() and game.gate_open[(x,y)]:
        print('already open for ' + str(x) + ',' + str(y))
        game.gate_y_offset = GATE_BLOCK_SIZE * (GATE_BLOCKS + 1)
        
    # item
    game.item_in_room = False
    for row in tilemap:
        for tile in row:
            if tile.is_item():
                if (game.current_room_x, game.current_room_y, tile.x, tile.y) not in game.collected:
                    game.item_in_room = True
                    game.animate_item_tile = tile
                continue
        
    redraw_room(tilemap, (game.current_room_x,game.current_room_y), game.collected_items, game.gate_y_offset, game.item_in_room)
    
    if game.current_room_x == 101 and game.current_room_y == 97:
        game.fading_message = "unfinished area of the game. explore elsewhere"

async def main():
    global game, tilemap, previous_tilemap
    
    initialize_game()
    game.fading_message = tutorial('1')
    
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
            # KEY SINGLE PRESSES
            elif event.type == pygame.KEYDOWN:
                if event.key == RESTART_KEY:
                    await create_dialog_box(screen, "Restart game?", initialize_game, cancel)
                    
                #elif event.key == pygame.K_x:
                #    game.fading_message = "you should eat your cornflakes, dude"
                 
                elif event.key == MUSIC_KEY:
                    toggle_music()
                 
                elif game.player_state != DEAD and game.player_state != HIT and game.player_state != DASH:
                    
                    if event.key == DIE_KEY:  
                        game.player_state = DEAD
                        game.player_animation_index = 0
                    #elif event.key == pygame.K_h:
                    #    game.player_state = HIT
                    #    game.player_animation_index = 0
                    #elif event.key == pygame.K_g:
                    #    game.exploding_tile = True
                    #    game.explosion_x, game.explosion_y = 50,50
                    #    game.explosion_counter = 0
                    #    print('game.explosion_x=' + str(game.explosion_x) + ' game.explosion_y=' + str(game.explosion_y))
                        
                    # dash
                    elif event.key == DASH_KEY:
                        if 'D' in game.collected_items.keys():
                            if ((game.player_state != JUMPING and game.player_state != HOVER) or \
                             'A' in game.collected_items.keys()):
                                game.air_dash = True if game.player_state == JUMPING else False
                                game.player_state = DASH
                                game.player_vx = game.player_facing * DASH_VELOCITY
                                game.player_vy = 0
                                game.player_animation_index = 0
                    
                    # stomp
                    elif event.key == STOMP_KEY:
                        if 'S' in game.collected_items.keys() and \
                         game.player_state == JUMPING and not game.stomping:
                            game.stomping = True
                            game.player_animation_index = 0
                            print('stomp')
                            game.player_vy = MAX_FALL_VELOCITY  # fall fast when game.stomping
                    
                    '''
                    if event.key == pygame.K_o:
                        if game.gate_open[(game.current_room_x, game.current_room_y)]:
                            pass
                        else:
                            game.gate_open[(game.current_room_x, game.current_room_y)] = True
                            game.animate_gate = True
                            print('opened for ' + str(game.current_room_x) + ',' + str(game.current_room_y))
                    '''        
                        
                    
                        
                        
                elif (event.key == pygame.K_RETURN and game.player_state == DEAD):
                    # Implement something here, e.g. restart the game
                    initialize_game(save_progress = True)
                    
                


        
        if game.player_state != LANDING and game.player_state != DEAD and \
         game.player_state != HIT:  # if not landing and not dead
         
            # KEY HOLD DOWNS
            keys = pygame.key.get_pressed()
            
            # hover
            if keys[HOVER_KEY] and 'H' in game.collected_items.keys():
                # initiate game.hover_counter
                if not game.hovering and game.player_vy == 0 and game.player_state != JUMPING and game.hover_counter == 0:
                    print('initiate hover')
                    game.hovering = True
                    game.player_vy = -2
                    game.player_state = HOVER
                # sustain hover
                elif game.hovering:
                    game.hover_counter += 1
                    # if hover hasn't run out
                    if game.hover_counter >= HOVER_LIMIT:
                        game.player_vy = 0
                        game.hovering = False
                    # if hover elevation has reached max
                    elif game.hover_counter >= HOVER_ELEVATE_LIMIT:
                        game.player_vy = 0
                    # otherwise keep elevating
                    else:
                        game.player_vy = -.5
                    # stop hover
                    #if game.hover_counter == MAX_game.hover_counter:
                    #   game.hovering = False
                    #    game.player_state = JUMPING
  
                else:
                    pass
                #print('game.hovering=' + str(game.hovering) + ' game.player_vy=' + str(game.player_vy) + ' game.hover_counter=' + str(game.hover_counter))
            else:
                game.hovering = False

            
            # jump
            if keys[JUMP_KEY] and game.player_state != DASH:
                # initiate jump
                if game.can_jump:
                    game.player_vy = -JUMP_VELOCITY
                    game.can_jump = False
                    game.player_state = JUMPING
                    game.player_animation_index = 0
                    game.hovering = False
                # if player is jumping and holding down button then continue
                elif game.player_state == JUMPING:
                    pass
            # if player stops holding down jump button then end vertical velocity upwards
            elif game.player_state == JUMPING and \
             (game.player_vy < 0 and not game.reverse_gravity) or (game.player_vy > 0 and game.reverse_gravity):
                game.player_vy = 0
    
            '''if keys[pygame.K_LEFT] and game.player_state == DASH and game.player_facing == 1:
                # stop a right dash by pressing left
                game.player_state = JUMPING
                game.player_animation_index = 0
                game.player_vx = 0
            elif keys[pygame.K_RIGHT] and game.player_state == DASH and game.player_facing == -1:
                # stop a a left dash by pressing right
                game.player_state = JUMPING
                game.player_animation_index = 0
                game.player_vx = 0
            '''
     
            # move left
            if keys[pygame.K_LEFT] and game.player_state != LANDING and \
             (game.player_state != DASH or dash_collision_check(tilemap, game.player_x - game.player_vx, game.player_y + game.player_vy)):
                if game.player_state == JUMPING:
                    game.player_facing = -1
                    game.player_vx -= AIRBORNE_ACCELERATION  # Decelerate when moving left while airborne
                elif game.player_state == HOVER:
                    game.player_facing = -1
                    game.player_vx -= HOVER_ACCELERATION
                elif game.player_state == DASH:
                    game.player_facing = -1
                
                else:
                    game.player_facing = -1
                    game.player_vx -= ACCELERATION  # Accelerate/Decelerate
                    if game.player_state == WALKING_DOWN:
                        game.player_vy = abs(game.player_vx)
                    elif game.player_state == WALKING_UP:
                        game.player_vx += min(ACCELERATION*3/4, -game.player_vx) # harder to go up slope
                        game.player_vy = -game.player_vx
                    else:
                        game.player_state = WALKING
                     
                
                # Cap velocity
                if game.player_state == JUMPING and game.player_vx < - MAX_JUMP_VELOCITY:
                    game.player_vx = -MAX_JUMP_VELOCITY
                elif game.player_state != DASH and game.player_vx < -MAX_VELOCITY:  
                    game.player_vx = -MAX_VELOCITY
                elif game.player_state == DASH and game.player_vx < -DASH_VELOCITY:
                    game.player_vx = -DASH_VELOCITY
            
            
            # move right 
            elif keys[pygame.K_RIGHT] and game.player_state != LANDING and \
             (game.player_state != DASH or dash_collision_check(tilemap, game.player_x + game.player_vx, game.player_y + game.player_vy)):
                if game.player_state == JUMPING:
                    game.player_facing = 1
                    game.player_vx += AIRBORNE_ACCELERATION  # Accelerate when moving right while airborne
                elif game.player_state == HOVER:
                    game.player_facing = 1
                    game.player_vx += HOVER_ACCELERATION 
                elif game.player_state == DASH:
                    game.player_facing = 1
                    
                else:
                    game.player_facing = 1
                    game.player_vx += ACCELERATION  # Accelerate/Decelerate
                    if game.player_state == WALKING_DOWN:
                        game.player_vy = abs(game.player_vx)
                    elif game.player_state == WALKING_UP:
                        game.player_vx -= min(ACCELERATION*3/4, game.player_vx) # harder to go up slope
                        game.player_vy = -game.player_vx
                    else:
                        game.player_state = WALKING
                 
                # Cap velocity
                if game.player_state == JUMPING and game.player_vx > MAX_JUMP_VELOCITY:
                    game.player_vx = MAX_JUMP_VELOCITY
                elif game.player_state != DASH and game.player_vx > MAX_VELOCITY:  
                    game.player_vx = MAX_VELOCITY
                elif game.player_state == DASH and game.player_vx > DASH_VELOCITY:
                    game.player_vx = DASH_VELOCITY
                    
            else: 
                # Decelerate when not moving
                if game.player_vx > 0: 
                    dec_amount = min(ACCELERATION * 2, game.player_vx)
                    game.player_vx -= dec_amount
                    
                    #if game.player_state == WALKING_DOWN:
                    #    game.player_vy = game.player_vx
                    #elif game.player_state == WALKING_UP:
                    #    game.player_vy = -game.player_vx
                        
                    #if game.player_vx < 0:
                    #    game.player_vx = 0       
                elif game.player_vx < 0:
                    dec_amount = min(ACCELERATION * 2, -game.player_vx)
                    game.player_vx += dec_amount
                 
                    #if game.player_state == WALKING_DOWN:
                    #    game.player_vy = -game.player_vx
                    #elif game.player_state == WALKING_UP:
                    #    game.player_vy = game.player_vx
                        
                    #if game.player_vx > 0:
                    #    game.player_vx = 0
                        
                # stop walking animation when vx is 0
                if game.player_vx == 0 and game.player_state == WALKING:
                    game.player_state = STANDING

        # Check if the player has walked off a tile
        #if (game.player_vy >= 4 and game.player_state != WALKING_DOWN) or game.player_vy >= 8:
        if game.player_vy >= 4: # and game.player_state != WALKING_DOWN and game.player_state != WALKING_UP:
            if game.player_state != JUMPING:
                game.player_animation_index = len(player_jumping_sprites) * player_jumping_animation_speed - 1
                game.stomping = False
                print('switch to falling')
            game.player_state = JUMPING
            game.hovering = False
            game.can_jump = False
        elif game.player_vy > 0:
            game.can_jump = False
            

        

        # Animate the player jumping
        if game.player_state == JUMPING:
            #print('before: ' + str(game.player_animation_index))    
            if game.stomping:
                if game.player_vy < 4 and game.player_animation_index < len(player_stomp_sprites) * player_stomp_animation_speed - 1:
                    game.player_animation_index = (game.player_animation_index + 1) % (len(player_stomp_sprites) * player_stomp_animation_speed)
                else:
                    game.player_animation_index = len(player_stomp_sprites) * player_stomp_animation_speed - 1
            else:
                if game.player_vy < 4 and game.player_animation_index < len(player_jumping_sprites) * player_jumping_animation_speed - 1:
                    game.player_animation_index = (game.player_animation_index + 1) % (len(player_jumping_sprites) * player_jumping_animation_speed)
                else:
                    game.player_animation_index = len(player_jumping_sprites) * player_jumping_animation_speed - 1
            #print('after: ' + str(game.player_animation_index))        
        # Animate the player walking
        elif game.player_state == WALKING or \
         (game.player_vx != 0 and (game.player_state == WALKING_UP or game.player_state == WALKING_DOWN)):
            game.player_animation_index = (game.player_animation_index + 1) % (len(player_walking_sprites) * player_walking_animation_speed)
        #elif game.player_state != LANDING:
        #    player_walking_index = 0
        #    game.player_state = STANDING
        #    print('switch to standing')
        
        # Animate the player landing
        elif game.player_state == LANDING:
            game.player_animation_index += 1
            if game.player_animation_index >= len(player_landing_sprites) * player_landing_animation_speed:
                game.player_state = STANDING
                game.player_animation_index = 0
                game.player_vx = game.player_vx / 2
                game.hover_counter = 0
                print('finish landing')
                if game.stomping:
                    game.stomping = False
                    # get tile nearest feet
                    #print('player_x=' + str(player_x))
                    if game.player_facing == 1:
                        tile_x = int((game.player_x + TILE_SIZE/2) / TILE_SIZE)
                    else:
                        tile_x = int((game.player_x - TILE_SIZE/2) / TILE_SIZE)
                    tile_y = int((game.player_y + HALF_HEIGHT) // TILE_SIZE)
                    tile_x_2 = int(game.player_x / TILE_SIZE) # in case the first fails try a second tile
                    # try to stomp tile near foot
                    if tile_x >= 0 and tile_y >= 0 and tile_x < len(tilemap[0]) and tile_y < len(tilemap):
                        tile = tilemap[tile_y][tile_x]
                        print('stomp tile x=' + str(tile_x) + ', y=' + str(tile_y))
                        if tile.breakable():
                            tile.id = 0
                            game.exploding_tile = True
                            game.explosion_counter = 0
                            game.explosion_x, game.explosion_y = tile_x*TILE_SIZE + TILE_SIZE/2, tile_y*TILE_SIZE + TILE_SIZE/2
                            game.player_state = STANDING
                    # try to stomp tile beneath player
                    if not game.exploding_tile and tile_x_2 >= 0 and tile_y >= 0 and tile_x_2 < len(tilemap[0]) and tile_y < len(tilemap):
                        tile = tilemap[tile_y][tile_x_2]
                        print('stomp tile x=' + str(tile_x_2) + ', y=' + str(tile_y))
                        if tile.breakable():
                            tile.id = 0
                            game.exploding_tile = True
                            game.explosion_counter = 0
                            game.explosion_x, game.explosion_y = tile_x_2*TILE_SIZE + TILE_SIZE/2, tile_y*TILE_SIZE + TILE_SIZE/2
                            game.player_state = STANDING
                        
                        
                    
                
                
        # Animate the player death
        elif game.player_state == DEAD:
            if game.player_animation_index < len(player_death_sprites) * player_death_animation_speed - 1:
                game.player_animation_index += 1 
                
        # Animate the player getting hit
        elif game.player_state == HIT:
            if game.player_animation_index < len(player_hit_sprites) * player_hit_animation_speed - 1:
                game.player_animation_index += 1
            else:
                game.player_state = STANDING
                game.player_animation_index = 0
                
            # Move the player backwards 
            game.player_vx = -game.player_facing * TILE_SIZE / 20
            
        # Animate the player dashing
        elif game.player_state == DASH:
            if game.player_animation_index < (len(player_dash_sprites) - 1) * player_dash_animation_speed - 1:
                # if we're not on the second to last sprite then increment index
                game.player_animation_index += 1
            else:
                # we're on the second to last sprite. normally we end the dash here.
                # but if there is a tile above our head (player fits within two tiles heights)
                # then do NOT end the dash yet but instead retain the last frame of animation
                # and make the player slide until there is no tile above their head
                game.player_vx = game.player_facing
                if dash_collision_check(tilemap, game.player_x + game.player_vx, game.player_y + game.player_vy):
                    # retain same animation frame
                    print('retain frame')
                    game.player_animation_index = len(player_dash_sprites) * player_dash_animation_speed - 1
                    game.player_vx = game.player_facing * 4.5
                else:
                    print('end dash')
                    game.player_state = JUMPING
                    game.player_animation_index = 0
                    game.player_vx = 0
        
        # Animate the player game.stomping
        #elif game.player_state == STOMP:
        #    if game.player_animation_index < len(player_stomp_sprites) * player_stomp_animation_speed - 1:
        #        game.player_animation_index += 1
        #    else:
        #        game.player_state = STANDING
        #        game.player_animation_index = 0
        # Animate the player getting hit
        elif game.player_state == HOVER:
            game.player_animation_index = (game.player_animation_index + 1) % (len(player_hover_sprites) * player_hover_animation_speed)
       

        
        # increase player velocities
        new_player_x = game.player_x + game.player_vx
        new_player_y = game.player_y + game.player_vy



        game.reverse_gravity = False
        # do collision check                      
        collided_x, collided_y = collision_check(game, tilemap, new_player_x, new_player_y)
        # do collision check with item
        item_id = await item_collision_check(game, tilemap, new_player_x, new_player_y)
        if item_id != "":
            game.fading_message = tutorial(item_id)
        #print('collided_x=' + str(collided_x) + ' collided_y=' + str(collided_y))
        if not collided_x:
            game.player_x = new_player_x
        if not collided_y:
            game.player_y = new_player_y
            
            # gravity
            if True: #game.player_state != WALKING_UP and game.player_state != WALKING_DOWN:
                if game.reverse_gravity:
                    game.player_vy -= GRAVITY
                    if game.player_vy < -MAX_FALL_VELOCITY:
                        game.player_vy = -MAX_FALL_VELOCITY
                else:
                    game.player_vy += GRAVITY
                    if game.player_vy > MAX_FALL_VELOCITY:
                        game.player_vy = MAX_FALL_VELOCITY
            

        
        if not collided_x or not collided_y:
            new_room_x, new_room_y = game.current_room_x, game.current_room_y
            
            # Determine the direction of the transition
            transition_direction_x = 0
            transition_direction_y = 0
            
            if game.player_x + HALF_WIDTH/2 > WIDTH:
                new_room_x += 1
                transition_direction_x = 1
                screen_offset_x, screen_offset_y = -WIDTH, 0
            elif game.player_x - HALF_WIDTH/2 < 0:
                new_room_x -= 1
                transition_direction_x = -1
                screen_offset_x, screen_offset_y = WIDTH, 0
            if game.player_y + HALF_WIDTH > HEIGHT:
                new_room_y += 1
                transition_direction_y = 1
                screen_offset_x, screen_offset_y = 0, -HEIGHT
            elif game.player_y < 0 + TILE_SIZE:
                new_room_y -= 1
                transition_direction_y = -1
                screen_offset_x, screen_offset_y = 0, HEIGHT
            
            # Start the transition
            if new_room_x != game.current_room_x or new_room_y != game.current_room_y:
                print('entering room x=' + str(new_room_x) + '-' + str(new_room_y))
            
                game.exploding_tile = False
                game.transition_x = transition_direction_x * WIDTH
                game.transition_y = transition_direction_y * HEIGHT
                
                previous_tilemap = tilemap  # Save the old room's tilemap
                load_tilemap(new_room_x, new_room_y) # Load the new room

                # Transition
                while abs(game.transition_x) > 0 or abs(game.transition_y) > 0:
                    
                    redraw_room_transitioning(tilemap, previous_tilemap, (game.current_room_x,game.current_room_y), (new_room_x,new_room_y), game.transition_x, game.transition_y, screen_offset_x, screen_offset_y)
                    if game.fading_message != "":
                        draw_fading_message(screen, game.fading_message, game.fading_message_counter)
                    redraw_player(game.player_x, game.player_y, game.player_facing, game.player_state, game.player_animation_index, game.stomping, game.reverse_gravity)
                    
                    # Update the transition progress
                    game.transition_x -= transition_speed * transition_direction_x
                    game.transition_y -= transition_speed * transition_direction_y

                    # Cap the transition progress
                    if transition_direction_x > 0 and game.transition_x < 0:
                        game.transition_x = 0
                    elif transition_direction_x < 0 and game.transition_x > 0:
                        game.transition_x = 0
                    if transition_direction_y > 0 and game.transition_y < 0:
                        game.transition_y = 0
                    elif transition_direction_y < 0 and game.transition_y > 0:
                        game.transition_y = 0
                     
                    # the player coordinates should be updated too
                    game.player_x -= transition_speed * transition_direction_x * .92
                    game.player_y -= transition_speed * transition_direction_y * .88
                    
                    # Update the display
                    pygame.display.update()
                    
                    # Wait for the next frame
                    await asyncio.sleep(0)
    
    
                enter_room(new_room_x, new_room_y)
                
                
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
            x1 = min(game.player_x - HALF_WIDTH*2, new_player_x - HALF_WIDTH*2, game.player_x + HALF_WIDTH*2, new_player_x + HALF_WIDTH*2)
            x2 = max(game.player_x - HALF_WIDTH*2, new_player_x - HALF_WIDTH*2, game.player_x + HALF_WIDTH*2, new_player_x + HALF_WIDTH*2)
            y1 = min(game.player_y - HALF_HEIGHT*2, new_player_y - HALF_HEIGHT*2, game.player_y + HALF_HEIGHT*2, new_player_y + HALF_HEIGHT*2)
            y2 = max(game.player_y - HALF_HEIGHT*2, new_player_y - HALF_HEIGHT*2, game.player_y + HALF_HEIGHT*2, new_player_y + HALF_HEIGHT*2)
            rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
            

            # Redraw room rect
            redraw_room_rect(tilemap, (game.current_room_x,game.current_room_y), rect, game.collected_items, game.gate_y_offset, game.item_in_room)
            
            # Redraw player
            redraw_player(game.player_x, game.player_y, game.player_facing, game.player_state, game.player_animation_index, game.stomping, game.reverse_gravity)

        
            pygame.display.update(rect)
        


        
        # redraw exploding tiles
        if game.exploding_tile:
            if game.explosion_counter % EXPLOSION_ANIMATION_SPEED == 0:
        
                rect_radius = (TILE_SIZE+3)*2
                explosion_rect = pygame.Rect(game.explosion_x - rect_radius, game.explosion_y - rect_radius, rect_radius*2, rect_radius*2)
                redraw_room_rect(tilemap, (game.current_room_x,game.current_room_y), explosion_rect, game.collected_items, game.gate_y_offset, game.item_in_room) # first clear that area
                
                if game.explosion_counter > EXPLOSION_COUNTER_LIMIT:  # end explosion
                    game.explosion_counter = 0
                    game.exploding_tile = False
                    
                
                if game.exploding_tile:  # if the tile is still exploding then draw it
                    redraw_explosion(game.explosion_x, game.explosion_y, game.explosion_counter)
                    
                pygame.display.update(explosion_rect)
              
            game.explosion_counter += 1
           
        
        # redraw gate  
        if game.animate_gate:
            game.gate_y_offset += 1

            if game.gate_y_offset >= GATE_BLOCK_SIZE * (GATE_BLOCKS + 1):
                game.animate_gate = False
                print('animate gate complete')
                
        
        # redraw items
        if game.item_in_room:
            draw_item(game.animate_item_tile, game.last_item_animation_time)
         

        # redraw fading message
        if game.fading_message != "":
            top_rect = pygame.Rect(0, 0, WIDTH, 120)
            redraw_room_rect(tilemap, (game.current_room_x,game.current_room_y), top_rect, game.collected_items, game.gate_y_offset, game.item_in_room)
            draw_fading_message(screen, game.fading_message, game.fading_message_counter)
            
            game.fading_message_counter -= 2
            if game.fading_message_counter <= -10:
                game.fading_message_counter = 850
                if game.fading_message == tutorial('1'):
                    game.fading_message = tutorial('2')
                elif game.fading_message == tutorial('2'):
                    game.fading_message = tutorial('3')
                else:    
                    game.fading_message = ""
                

        
            

        await asyncio.sleep(0)
        
    

    
asyncio.run(main())





                
