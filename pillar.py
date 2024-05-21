

import pygame
import asyncio

# Initialize pygame
pygame.init()

# Set the dimensions of the window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))

# Set the font for the message
font = pygame.font.Font(None, 36)

class Message:
    def __init__(self, message):
        self.text = font.render(message, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(window_width / 2, 50))
        self.alpha = 255

    async def display(self):
        if self.alpha > 0:
            self.text.set_alpha(self.alpha)
            screen.blit(self.text, self.text_rect)
            self.alpha -= 5

async def main():
    message = Message("Hello, world!")
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with black to clear it
        screen.fill((0, 0, 0))

        # Display the message
        await message.display()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

        # Wait for a short time
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())

