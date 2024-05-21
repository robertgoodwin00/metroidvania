
import asyncio
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (64, 64, 64)
FONT = pygame.font.SysFont("Arial", 24)
FADING_FONT = pygame.font.SysFont("Tahoma", 24)
message_font = pygame.font.Font(None, 28)
WIDTH, HEIGHT = 960, 640


# Function to create a dialog box
async def create_dialog_box(screen, text, yes_callback, no_callback):
    # Create a surface for the dialog box
    dialog_surface = pygame.Surface((300, 150))
    dialog_surface.fill((150,100,100))
    # Draw a border around the dialog box
    pygame.draw.rect(dialog_surface, WHITE, (3, 3, 294, 144), 0)

    # Render the text
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(150, 30))
    dialog_surface.blit(text_surface, text_rect)

    # Create the YES and NO buttons
    yes_button = pygame.Rect(50, 100, 90, 40)
    no_button = pygame.Rect(155, 100, 90, 40)

    # Draw the buttons
    pygame.draw.rect(dialog_surface, BLACK, yes_button, 2)
    pygame.draw.rect(dialog_surface, BLACK, no_button, 2)

    # Render the button text
    yes_text = FONT.render("YES", True, BLACK)
    yes_text_rect = yes_text.get_rect(center=yes_button.center)
    dialog_surface.blit(yes_text, yes_text_rect)

    no_text = FONT.render("NO", True, BLACK)
    no_text_rect = no_text.get_rect(center=no_button.center)
    dialog_surface.blit(no_text, no_text_rect)

    
    # Blit the dialog box to the screen
    screen.blit(dialog_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 75))

    # Handle events
    selected_button = yes_button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_button = yes_button
                elif event.key == pygame.K_RIGHT:
                    selected_button = no_button
                elif event.key == pygame.K_RETURN:
                    if selected_button == yes_button:
                        yes_callback()
                    else:
                        no_callback()
                    return  # Exit the loop after callback
                elif event.key == pygame.K_ESCAPE:
                    no_callback()
                    return  # Exit the loop after callback
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (mouse_pos[0] - (WIDTH // 2 - 150), mouse_pos[1] - (HEIGHT // 2 - 75))
                if yes_button.collidepoint(mouse_pos):
                    yes_callback()
                    return  # Exit the loop after callback
                elif no_button.collidepoint(mouse_pos):
                    no_callback()
                    return  # Exit the loop after callback

        dialog_surface.fill((150,100,100))
        # Draw a border around the dialog box
        pygame.draw.rect(dialog_surface, WHITE, (3, 3, 294, 144), 0)
        
        pygame.draw.rect(dialog_surface, BLACK, (0, 0, 300, 150), 2)
        pygame.draw.rect(dialog_surface, BLACK, yes_button, 2)
        pygame.draw.rect(dialog_surface, BLACK, no_button, 2)
        pygame.draw.rect(dialog_surface, BLACK, selected_button, 4)
        dialog_surface.blit(text_surface, text_rect)
        dialog_surface.blit(yes_text, yes_text_rect)
        dialog_surface.blit(no_text, no_text_rect)

        # Update the display
        screen.blit(dialog_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 75))
        pygame.display.flip()
        
        await asyncio.sleep(0)
       
       
       
async def show_message(screen, message):
    # Create a surface for the message
    message_surf = message_font.render(message, True, WHITE)
    message_rect = message_surf.get_rect()
    message_rect.center = (WIDTH // 2, HEIGHT // 2)

    # Create a background surface
    background_surf = pygame.Surface((message_rect.width + 20, message_rect.height + 20))
    background_surf.fill(DARK_GREY)
    background_rect = background_surf.get_rect()
    background_rect.center = (WIDTH // 2, HEIGHT // 2)

    # Blit the background and message to the screen
    screen.blit(background_surf, background_rect)
    screen.blit(message_surf, message_rect)
    pygame.display.flip()

    print('entering message loop')
    # Wait for the player to press a key
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and \
             (event.key == pygame.K_RETURN or event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                return
        await asyncio.sleep(0)
        #pygame.display.flip()
        
   
def draw_fading_message(screen, message, i=0):
    # Create a surface for the message
    message_surf = FADING_FONT.render(message, True, WHITE)
    message_rect = message_surf.get_rect()
    message_rect.center = (WIDTH // 2, 100)

    if i > 255:
        i = 255
    message_surf.set_alpha(i)

    # Blit the message to the screen
    screen.blit(message_surf, message_rect)
    pygame.display.flip()

    

        
        
        