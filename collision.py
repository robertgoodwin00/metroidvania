
import pygame
from globs import *
from draw import *
from gui import *



def collision_check(game, tilemap, new_player_x, new_player_y): #, allow_dash_bonus = True):
    #print('x=' + str(new_player_x) + ' y=' + str(new_player_y) + ' state=' + str(game.player_state) + ' vx=' + str(game.player_vx) + ' vy=' + str(game.player_vy))
    
    # Check for collisions with adjacent tiles
    collided_x = False
    collided_y = False
    collided_slope = False # doesn't stop processing other possible collisions but will return from method with True
    #tile_x = int(game.player_x // TILE_SIZE)
    #tile_y = int(game.player_y // TILE_SIZE)
    tile_x = int(new_player_x // TILE_SIZE)
    tile_y = int(new_player_y // TILE_SIZE)
    
    
    #dash_bonus = TILE_SIZE if (allow_dash_bonus and game.player_state == DASH) else 0  # go under tiles when dashing
    
    dash_bonus = TILE_SIZE if game.player_state == DASH and (game.player_animation_index > 5 or game.air_dash) else 0  # go under and slightly above tiles when dashing
    hover_bonus = TILE_SIZE/2 if game.player_state == HOVER else 0  # go slightly above tiles when game.hovering
    
    
    # near player's feet
    tile_x_low = int(new_player_x // TILE_SIZE) if game.player_facing == -1 else int((new_player_x + 2) // TILE_SIZE)
    tile_y_low = int((new_player_y + HALF_HEIGHT) // TILE_SIZE)
    
    
    # check based on position of player's feet
    if in_map(tile_x_low, tile_y_low, tilemap):
        tile = tilemap[tile_y_low][tile_x_low]
        
        
        if game.player_state != WALKING:
            #print('tile_x=' + str(tile_x) + ' tile_y_low=' + str(tile_y_low))
            # determine if tile closest to player's center is a slope tile and apply bonus 
             
            
            if tile.id == 7:
                #print('slope 7')
                if game.player_state != JUMPING or game.player_vy > 0:
                    game.player_state = WALKING_UP if game.player_facing == -1 else WALKING_DOWN
                px = new_player_x - tile.x
                #py = new_player_y + HALF_HEIGHT - tile.y
                              
                # Check for collision on the bottom
                if game.player_vy > 0:
                    if True:
                    #if new_player_y + HALF_HEIGHT > tile.y + px and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE + px and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:         
                        game.player_y = tile.y - HALF_HEIGHT + new_player_x - tile.x
                        #print('new_player_y=' + str(new_player_y) + ' game.player_y now=' + str(game.player_y))
                        
                        game.player_vy = 0 if game.player_state == WALKING_UP else game.player_vy
                        collided_y = True
                        game.can_jump = True
                        #if game.player_state == JUMPING:
                        #    game.player_state = LANDING
                        #    game.player_animation_index = 0
                        #    game.player_vx = game.player_vx / 2
                        #    print('switch to landing')
                        #if game.player_state == HOVER:
                        #    game.player_state = STANDING
                        game.hovering = False
                        game.hover_counter = 0
                #print(str(tile_x) + ',' + str(tile_y_low))
                return collided_x, collided_y
                
            elif tile.id == 6:
                #print('slope 6')
                if game.player_state != JUMPING or game.player_vy > 0:
                    game.player_state = WALKING_UP if game.player_facing == 1 else WALKING_DOWN
                px = new_player_x - tile.x
                #py = new_player_y + HALF_HEIGHT - tile.y
                        
                # Check for collision on the bottom
                if game.player_vy > 0:
                    if True:
                    #if new_player_y + HALF_HEIGHT > tile.y + TILE_SIZE - px and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE + TILE_SIZE - px and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:
                        game.player_y = tile.y - HALF_HEIGHT + TILE_SIZE - px
                        
                        game.player_vy = 0 if game.player_state == WALKING_UP else game.player_vy
                        collided_y = True
                        game.can_jump = True
                        #if game.player_state == JUMPING:
                        #    game.player_state = LANDING
                        #    game.player_animation_index = 0
                        #    game.player_vx = game.player_vx / 2
                        #    print('switch to landing')
                        #if game.player_state == HOVER:
                        #    game.player_state = STANDING
                        game.hovering = False
                        game.hover_counter = 0
                #print(str(tile_x) + ',' + str(tile_y_low))
                
                return collided_x, collided_y
                
            elif tile.solid():
                if game.player_state == WALKING_DOWN:
                    game.player_state = WALKING
                    collided_y = True
                    print('back to walking')
                    return collided_x, collided_y
                    
                    '''
                    tile_y2 = tile_y_low + 2
                    if in_map(tile_x, tile_y2, tilemap):
                        tile2 = tilemap[tile_y2][tile_x]
                        if tile2.solid() and tile2.id != 6 and tile2.id != 7:
                            game.player_state = WALKING
                            game.player_y += 2
                            collided_y = True
                            print('back to walking')
                            return collided_x, collided_y
                    '''
                elif game.player_state == WALKING_UP:
                    tile_y2 = tile_y_low - 2
                    if in_map(tile_x, tile_y2, tilemap):
                        tile2 = tilemap[tile_y2][tile_x]
                        if tile2.id == 0:
                            game.player_state = WALKING
                            game.player_y -= 2
                            collided_y = True
                            print('back to walking')
                            return collided_x, collided_y
                        else:
                            print('almost back to walking')
           
            elif game.player_state == WALKING_UP and tile.id == 0 and game.player_facing == 1:
                game.player_state = WALKING
                collided_y = True
                print('2 back to walking air')
                #game.player_y = tile.y - HALF_HEIGHT
                game.player_vy = tile.y - HALF_HEIGHT
                game.player_vy = 0
            
                return collided_x, collided_y
                
            
                        
            elif tile.id == 0 and (game.player_state == WALKING_UP or game.player_state == WALKING_DOWN):
                game.player_state = WALKING
                print('air so back to walking')
                
            '''elif game.player_state == WALKING_UP and tile.id == 0 and game.player_facing == 1:
                tile_x2 = int(new_player_x + 2 // TILE_SIZE)
                tile_y2 = tile_y_low - 2
                if in_map(tile_x2, tile_y2, tilemap):
                    tile2 = tilemap[tile_y2][tile_x2]
                    if tile2.id == 0:
                        game.player_state = WALKING
                        collided_y = True
                        print('2 back to walking air')
                        #game.player_y = tile.y - HALF_HEIGHT
                        game.player_vy /= 2
                        game.player_vx /= 2
                        return collided_x, collided_y
                    else:
                        print('2 almost back to walking')'''
       
                
                            
            
        elif game.player_state == WALKING:
            # check for starting to walk down slope
            #print(' tile_x=' + str(tile_x) + '  tile_y=' + str(tile_y) + ' tile_y_low=' + str(tile_y_low))
            # determine if tile closest to player's center is a slope tile and apply bonus 

            # check for walking down onto slope to the right
            if tile.id == 7 and game.player_vx > 0:
                print('slope 7 low walk down right')
                game.player_state = WALKING_DOWN
                px = new_player_x - tile.x
                #py = new_player_y + HALF_HEIGHT - tile.y
                              
                # Check for collision on the bottom
                
                #if new_player_y + HALF_HEIGHT > tile.y + px and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE + px and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:         
                game.player_y = tile.y - HALF_HEIGHT + new_player_x - tile.x
                #print('new_player_y=' + str(new_player_y) + ' game.player_y now=' + str(game.player_y))
                
                if game.player_vx > 2:
                    game.player_vx = 2
                game.player_vy = 0
                collided_y = True
                game.can_jump = True

                game.hovering = False
                game.hover_counter = 0
                #print(str(tile_x) + ',' + str(tile_y_low))
                return collided_x, collided_y
                
            # check for walking down onto slope to the left
            elif tile.id == 6 and game.player_vx < 0:
                print('slope 6 low walk down left')
                game.player_state = WALKING_DOWN
                px = new_player_x - tile.x
                py = new_player_y + HALF_HEIGHT - tile.y
                        
                # Check for collision on the bottom
                
                #if new_player_y + HALF_HEIGHT > tile.y + TILE_SIZE - px and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE + TILE_SIZE - px and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:
                game.player_y = tile.y - HALF_HEIGHT + TILE_SIZE - px
                 
                if game.player_vx < -2:
                    game.player_vx = -2
                game.player_vy = 0
                collided_y = True
                game.can_jump = True

                game.hovering = False
                game.hover_counter = 0
                #print(str(tile_x) + ',' + str(tile_y_low))
                return collided_x, collided_y

            # check for walking up onto slope to the right 
            if tile.id == 6 and game.player_vx > 0:
                print('slope 6 walk up right')
                game.player_state = WALKING_UP
                #px = new_player_x - tile.x
                #py = new_player_y + HALF_HEIGHT - tile.y
                              
                # Check for collision on the bottom
                
                #if new_player_y + HALF_HEIGHT > tile.y + px and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE + px and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:         
                #game.player_y = tile.y - HALF_HEIGHT + new_player_x - tile.x
                #print('new_player_y=' + str(new_player_y) + ' game.player_y now=' + str(game.player_y))
                
                if game.player_vx > 2:
                    game.player_vx = 2
                #game.player_vy = 0
                collided_y = True
                game.can_jump = True

                game.hovering = False
                game.hover_counter = 0
                #print(str(tile_x) + ',' + str(tile_y_low))
                return collided_x, collided_y
                
            # check for walking up onto slope to the left 
            if tile.id == 7 and game.player_vx < 0:
                print('slope 7 walk up left')
                game.player_state = WALKING_UP
                #px = new_player_x - tile.x
                #py = new_player_y + HALF_HEIGHT - tile.y
                              
                # Check for collision on the bottom
                
                #if new_player_y + HALF_HEIGHT > tile.y + px and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE + px and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:         
                #game.player_y = tile.y - HALF_HEIGHT + TILE_SIZE - px
                #print('new_player_y=' + str(new_player_y) + ' game.player_y now=' + str(game.player_y))
                
                if game.player_vx < -2:
                    game.player_vx = -2
                #game.player_vy = 0
                collided_y = True
                game.can_jump = True

                game.hovering = False
                game.hover_counter = 0
                #print(str(tile_x) + ',' + str(tile_y_low))
                return collided_x, collided_y
        

    
                   
     
    # general collision check     
    #print('no slope')      
    #print(str(tile_x) + ',' + str(tile_y_low))
    if True: #game.player_state != WALKING_UP and game.player_state != WALKING_DOWN:
        for x in range(tile_x - 2, tile_x + 3):
            for y in range(tile_y - 3, tile_y + 3):
                if in_map(x, y, tilemap):
                    tile = tilemap[y][x]
                    if tile.solid():
                        
                        # Check for collision on the left
                        if not collided_x and game.player_vx < 0 and ((tile.id != 6 and tile.id != 7) or game.player_vy > 0 or game.player_state != JUMPING) and \
                         game.player_state != WALKING_UP:
                            if new_player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/4 > tile.x and game.player_y + HALF_HEIGHT - dash_bonus/2 - hover_bonus/2 > tile.y and game.player_y - HALF_HEIGHT + dash_bonus <= tile.y: 
                                
                                # check for starting to walk up slope
                                if tile.id == 7:
                                    proposed_new_player_y = tile.y - HALF_HEIGHT + new_player_x - tile.x
                                    if game.player_y > proposed_new_player_y:
                                        game.player_y = proposed_new_player_y
                                    #print('new_player_y=' + str(new_player_y) + ' game.player_y now=' + str(game.player_y))
                                    
                                    game.player_vy = 0
                                    #game.player_state = WALKING_UP if game.player_facing == -1 else WALKING_DOWN
                                    #print('COLLIDED SLOPE 7 at ' + str(x) + ',' + str(y))
                                    collided_slope = True
                                    continue
                                
                                #if game.player_state == WALKING_DOWN or game.player_state == WALKING_UP:
                                #    game.player_state = WALKING
                                if game.player_state != WALKING_UP and game.player_state != WALKING_DOWN: #allow_dash_bonus:  # dont alter if only testing check for dash retain under tiles
                                    game.player_x = tile.x + TILE_SIZE + HALF_WIDTH/4
                                    game.player_vx = 0
                                
                                    if game.player_state == DASH:
                                        game.player_animation_index = len(player_dash_sprites) * player_dash_animation_speed - 1
                                        # check tile below it to see if the dash animation should end
                                        if y+1 < len(tilemap):
                                            tile2 = tilemap[y+1][x]
                                            if tile2.solid() and game.player_y + HALF_HEIGHT > tile2.y and game.player_y - HALF_HEIGHT < tile2.y:
                                                game.player_state = JUMPING
                                            #elif y+2 < len(tilemap):
                                            #    tile3 = tilemap[y+2][x]
                                            #    if tile3.solid() and game.player_y + HALF_HEIGHT > tile3.y and game.player_y - HALF_HEIGHT < tile3.y:
                                            #        game.player_state = JUMPING 
                                collided_x = True
                                #print('COLLIDED at ' + str(x) + ',' + str(y))
                        
                        
                        # Check for collision on the right
                        elif not collided_x and game.player_vx > 0 and ((tile.id != 6 and tile.id != 7) or game.player_vy > 0 or game.player_state != JUMPING) and \
                         game.player_state != WALKING_UP:
                            if new_player_x + HALF_WIDTH/4 > tile.x and new_player_x + HALF_WIDTH/4 < tile.x + TILE_SIZE and game.player_y + HALF_HEIGHT - dash_bonus/2 - hover_bonus/2 > tile.y and game.player_y - HALF_HEIGHT + dash_bonus <= tile.y:
                                
                                # check for starting to walk up slope
                                if tile.id == 6:
                                    proposed_new_player_y = tile.y - HALF_HEIGHT - new_player_x + tile.x + TILE_SIZE
                                    if game.player_y > proposed_new_player_y:
                                        game.player_y = proposed_new_player_y
                                    #print('new_player_y=' + str(new_player_y) + ' game.player_y now=' + str(game.player_y))
                                    
                                    game.player_vy = 0
                                    #game.player_state = WALKING_UP if game.player_facing == 1 else WALKING_DOWN
                                    #print('COLLIDED SLOPE 6')
                                    collided_slope = True
                                    continue
                                    
                              
                                #if game.player_state == WALKING_DOWN or game.player_state == WALKING_UP:
                                #    game.player_state = WALKING
                                if game.player_state != WALKING_UP and game.player_state != WALKING_DOWN: #allow_dash_bonus:  # dont alter if only testing check for dash retain under tiles
                                    game.player_x = tile.x - HALF_WIDTH/4
                                    game.player_vx = 0
                                
                                    if game.player_state == DASH:
                                        game.player_animation_index = len(player_dash_sprites) * player_dash_animation_speed - 1
                                        # check tile below it to see if the dash animation should end
                                        if y+1 < len(tilemap):
                                            tile2 = tilemap[y+1][x]
                                            if tile2.solid() and game.player_y + HALF_HEIGHT > tile2.y and game.player_y - HALF_HEIGHT < tile2.y:
                                                player_state = JUMPING
                                            #elif y+2 < len(tilemap):
                                            #    tile3 = tilemap[y+2][x]
                                            #    if tile3.solid() and game.player_y + HALF_HEIGHT > tile3.y and game.player_y - HALF_HEIGHT < tile3.y:
                                            #        player_state = JUMPING 
                                collided_x = True
                                #print('COLLIDED at ' + str(x) + ',' + str(y))
                        
                        if tile.id == 6 or tile.id == 7:
                            continue # don't do top and bottom collision for slopes; that's handled above
                        
                        # Check for collision on the top
                        if not collided_y and game.player_vy < 0:
                            if new_player_y - HALF_HEIGHT < tile.y + TILE_SIZE and new_player_y - HALF_HEIGHT > tile.y and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:
                                game.player_y = tile.y + TILE_SIZE + HALF_HEIGHT
                                game.player_vy = 0
                                collided_y = True
                                print('COLLIDED Top at ' + str(x) + ',' + str(y))
                                if game.reverse_gravity:
                                    game.player_state = STANDING
                                    game.can_jump = True

                        
                        # Check for collision on the bottom
                        elif not collided_y and game.player_vy > 0: # and game.player_state != WALKING_DOWN and game.player_state != WALKING_UP:
                            if new_player_y + HALF_HEIGHT > tile.y and new_player_y + HALF_HEIGHT < tile.y + TILE_SIZE and game.player_x + HALF_WIDTH/4 > tile.x and game.player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE:
                                game.player_y = tile.y - HALF_HEIGHT
                                game.player_vy = 0
                                collided_y = True
                                #print('COLLIDED Bottom at ' + str(x) + ',' + str(y))
                                game.can_jump = True
                                if game.player_state == JUMPING:
                                    game.player_state = LANDING
                                    game.player_animation_index = 0
                                    game.player_vx = game.player_vx / 2
                                    print('switch to landing')
                                if game.player_state == HOVER:
                                    game.player_state = STANDING
                                game.hovering = False
                                game.hover_counter = 0
                            
    
    
    #if game.player_state == WALKING and game.player_vy > 0 and not collided_x and not collided_y:
    #    game.player_state = WALKING_DOWN
        #game.player_y += new_player_x - game.player_x
    #    collided_y = True
    
    

    # check for collision with gate
    if (game.current_room_x, game.current_room_y) in game.gate_open.keys() and not collided_x and game.player_vx != 0:
        gate_solid = False if game.gate_open[(game.current_room_x, game.current_room_y)] else True
        #print('gate_solid=' + str(gate_solid))
        collided_gate = False
        for x in range(tile_x - 2, tile_x + 3):
            for y in range(tile_y - 3, tile_y + 3):
                if in_map(x, y, tilemap):
                    tile = tilemap[y][x]
                    if not collided_x and tile.id == 'G' and gate_solid:
                        
                        if game.player_vx < 0:
                            if new_player_x - HALF_WIDTH/4 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/4 > tile.x and \
                             game.player_y + HALF_HEIGHT - dash_bonus/2 - hover_bonus/2 > tile.y and game.player_y - HALF_HEIGHT + dash_bonus < tile.y + TILE_SIZE*2:  
                                game.player_x = tile.x + TILE_SIZE + HALF_WIDTH/4
                                game.player_vx = 0
                                collided_gate = True
                                continue
                        elif game.player_vx > 0:
                            if new_player_x + HALF_WIDTH/4 > tile.x and new_player_x + HALF_WIDTH/4 < tile.x + TILE_SIZE and \
                             game.player_y + HALF_HEIGHT - dash_bonus/2 - hover_bonus/2 > tile.y and game.player_y - HALF_HEIGHT + dash_bonus < tile.y + TILE_SIZE*2:
                                game.player_x = tile.x - HALF_WIDTH/4
                                game.player_vx = 0
                                collided_gate = True
                                continue
        if collided_gate:
            if game.gate_open[(game.current_room_x, game.current_room_y)]:
                pass
            elif 'K' in game.collected_items.keys():
                game.gate_open[(game.current_room_x, game.current_room_y)] = True
                game.animate_gate = True
                print('opened for ' + str(game.current_room_x) + ',' + str(game.current_room_y))
            else:
                collided_x = True

    return collided_x, collided_y or collided_slope

        
 
def pillar_collision_check(game, tilemap, player_x, player_y):  
    tile_x = int(player_x // TILE_SIZE)
    tile_y = int(player_y // TILE_SIZE)
    # check for collision with light pillar
    if 'R' in game.collected_items.keys():
        for x in range(tile_x - 2, tile_x + 3):
            for y in range(tile_y - 3, tile_y + 3):
                if in_map(x, y, tilemap):
                    tile = tilemap[y][x]
                    if tile.id == 'P':
                        if (player_x - HALF_WIDTH//3 < tile.x + TILE_SIZE and
                            player_x + HALF_WIDTH//3 > tile.x and
                            player_y - HALF_HEIGHT < tile.y + TILE_SIZE and
                            player_y + HALF_HEIGHT > tile.y): 
                            # reverse gravity
                            game.reverse_gravity = True
                            return
    
    game.reverse_gravity = False
    
'''    
from functools import partial

in_map_func = partial(in_map, tilemap)
if any(in_map_func(x, y) and tilemap[y][x].is_item() for x in range(tile_x - 1, tile_x + 2) for y in range(tile_y - 2, tile_y + 2)):
    # Handle collision
    pass  ''' 
    
async def item_collision_check(game, tilemap, new_player_x, new_player_y): 
    if not game.item_in_room:
        return ""
 
    tile_x = int(new_player_x // TILE_SIZE)
    tile_y = int(new_player_y // TILE_SIZE)
    # Check for collisions with items
    for x in range(tile_x - 1, tile_x + 2):
        for y in range(tile_y - 2, tile_y + 2):
            if in_map(x, y, tilemap):
                tile = tilemap[y][x]
                if tile.is_item():
                    # Check if the player is touching the item
                    if (new_player_x - HALF_WIDTH//3 < tile.x + TILE_SIZE and
                        new_player_x + HALF_WIDTH//3 > tile.x and
                        new_player_y - HALF_HEIGHT < tile.y + TILE_SIZE and
                        new_player_y + HALF_HEIGHT > tile.y):
                        
                        # show message
                        await show_message(screen, f"Obtained {item_title(tile.id)}")
                        
                        # Add item and erase from screen
                        game.collected.add((game.current_room_x, game.current_room_y, x, y))  # Add the item's coordinates to the collected set
                        print('added ' + str(game.current_room_x) + ',' + str(game.current_room_y) + ',' + str(x) + ',' + str(y))
                        if tile.id in game.collected_items.keys():
                            game.collected_items[tile.id] += 1  # Increment the number of H-items collected
                        else:
                            game.collected_items[tile.id] = 1
                        item_id = tile.id
                        tile.id = 0
                        game.item_in_room = False
                        game.fading_message_counter = 850
                        
                        redraw_room(tilemap, (game.current_room_x,game.current_room_y), game.collected_items, game.gate_y_offset, game.item_in_room)
                        return item_id
    return ""   
    
    
    
def dash_collision_check(tilemap, new_player_x, new_player_y):
    tile_x = int(new_player_x // TILE_SIZE)
    tile_y = int(new_player_y // TILE_SIZE)
    
    for x in range(tile_x - 1, tile_x + 2):
        for y in range(tile_y - 2, tile_y + 2):
            #if x >= 0 and y >= 0 and x < len(tilemap[0]) and y < len(tilemap):
            if in_map(x, y, tilemap):
                tile = tilemap[y][x]
                if tile.solid():
               
                    # for now left uses a different method than right, so we can figure out which is better
               
                    # Check for collision on the left
                    # Check for collision on the left
                    if new_player_x - HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/3 > tile.x and new_player_y + HALF_HEIGHT > tile.y and new_player_y - HALF_HEIGHT <= tile.y:
                        if in_map(x, y+1, tilemap):
                            tile_below = tilemap[y+1][x]
                            if not tile_below.solid() or new_player_y + HALF_HEIGHT < tile_below.y:
                                return True
                                
                        else:
                            return True
                            
                    #if new_player_x - HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/3 > tile.x  and new_player_y + HALF_HEIGHT > tile.y and new_player_y - HALF_HEIGHT <= tile.y:
                    # not (new_player_x - HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_x - HALF_WIDTH/3 > tile.x  and new_player_y + HALF_HEIGHT > tile.y and new_player_y - HALF_HEIGHT <= tile.y - TILE_SIZE): 
                    #    return True
                    
                    
                    # Check for collision on the right
                    #if new_player_x + HALF_WIDTH/3 > tile.x and new_player_x + HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_y + HALF_HEIGHT > tile.y and new_player_y - HALF_HEIGHT < tile.y and \
                    # not (new_player_x + HALF_WIDTH/3 > tile.x and new_player_x + HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_y + HALF_HEIGHT > tile.y and new_player_y - HALF_HEIGHT <= tile.y - TILE_SIZE):
                    #    return True
                    
                    # Check for collision on the right
                    if new_player_x + HALF_WIDTH/3 > tile.x and new_player_x + HALF_WIDTH/3 < tile.x + TILE_SIZE and new_player_y + HALF_HEIGHT > tile.y and new_player_y - HALF_HEIGHT <= tile.y:
                        if in_map(x, y+1, tilemap):
                            tile_below = tilemap[y+1][x]
                            if not tile_below.solid() or new_player_y + HALF_HEIGHT < tile_below.y:
                                return True
                        else:
                            return True
         
             
    return False                    
                        
            