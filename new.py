
import pygame
import asyncio

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
DARK_GREY = (64, 64, 64)
RED = (255, 0, 0)



# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

async def show_message(message):
    # Create a surface for the message
    message_surf = font.render(message, True, WHITE)
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

    # Wait for the player to press a key
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        await asyncio.sleep(0)


last_animation_time = 0

def draw_item(x, y):
    global last_animation_time

    current_time = pygame.time.get_ticks()
    if current_time - last_animation_time >= 100:  # 100ms = 10 frames per second
        last_animation_time = current_time

        # Draw a hexagon
        points = [(x + 16, y), (x + 32, y + 8), (x + 32, y + 24), (x + 16, y + 32), (x, y + 24), (x, y + 8)]
        pygame.draw.polygon(screen, RED, points)
        pygame.draw.polygon(screen, WHITE, points, 2)

        # Draw a letter 'D'
        item_surf = font.render('D', True, WHITE)
        item_rect = item_surf.get_rect()
        item_rect.center = (x + 16, y + 17)  # Adjusted the center to make it look more centered
        screen.blit(item_surf, item_rect)

        # Animate the border
        for i in range(6):
            pygame.draw.line(screen, (255,160,160), points[i], points[(i + 1) % 6], 2)
        i = (current_time // 100) % 6
        pygame.draw.line(screen, WHITE, points[i], points[(i + 1) % 6], 2)

        pygame.display.flip()

def draw_small_item(x, y):
    # Draw a hexagon
    points = [(x + 12, y), (x + 24, y + 6), (x + 24, y + 18), (x + 12, y + 24), (x, y + 18), (x, y + 6)]
    pygame.draw.polygon(screen, (255, 100, 100), points)  # Pink-red background
    pygame.draw.polygon(screen, WHITE, points, 2)

    # Draw a letter 'D'
    small_font = pygame.font.Font(None, 24)
    item_surf = small_font.render('D', True, WHITE)
    item_rect = item_surf.get_rect()
    item_rect.center = (x + 13, y + 15)  # Adjusted the center to make it look more centered
    screen.blit(item_surf, item_rect)

    pygame.display.flip()

async def show_fading_message(message):
    # Create a surface for the message
    message_surf = font.render(message, True, WHITE)
    message_rect = message_surf.get_rect()
    message_rect.center = (WIDTH // 2, HEIGHT // 2)

    # Blit the message to the screen
    screen.blit(message_surf, message_rect)
    pygame.display.flip()

    # Fade the message away
    for i in range(255, -1, -10):
        message_surf.set_alpha(i)
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(message_surf, message_rect)
        pygame.display.flip()
        await asyncio.sleep(0.1)  # Wait a little bit
        
        
        
        
async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Your game logic here

        draw_item(100, 100)
        draw_small_item(200, 200)

        await asyncio.sleep(0)



asyncio.run(main())        
        