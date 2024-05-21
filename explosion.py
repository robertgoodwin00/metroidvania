
# Import the pygame library and initialise the game engine
import pygame
from random import randint
pygame.init()
# Set the screen size and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Explosion Animation")
clock = pygame.time.Clock()
# Define a color for the background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' old method for implosion
# Function to create an explosion animation
def create_explosion(explosion_x, explosion_y):
   # Number of frames in the explosion animation
   number_of_frames = 10
   # Radius of the explosion
   explosion_radius = 50
   for frame in range(number_of_frames):
       # Set the background color
       screen.fill(BLACK)
       # Adjust the radius for fading effect
       radius = explosion_radius - frame * 5
       for _ in range(80):  # Number of dots in the explosion
           x = explosion_x + randint(-radius, radius)
           y = explosion_y + randint(-radius, radius)
           #pygame.draw.circle(screen, WHITE, (x, y), 2)
           pygame.draw.rect(screen, WHITE, (x,y,3,3))
       # Reduce the frame rate to slow down the animation
       pygame.display.flip()
       clock.tick(10)
'''
# Function to create an explosion animation
def create_explosion(explosion_x, explosion_y):
   # Number of frames in the explosion animation
   number_of_frames = 12
   for frame in range(number_of_frames):
       # Set the background color
       screen.fill(BLACK)
       # Adjust the radius for fading effect
       radius = frame * 5
       for _ in range(60):  # Number of dots in the explosion
           x = explosion_x + randint(-radius, radius)
           y = explosion_y + randint(-radius, radius)
           #pygame.draw.circle(screen, WHITE, (x, y), 2)
           pygame.draw.rect(screen, WHITE, (x,y,3,3))
       # Reduce the frame rate to slow down the animation
       pygame.display.flip()
       clock.tick(10)
       
       
# Get the user input for the explosion coordinates
#explosion_x = int(input("Enter the x-coordinate for the explosion: "))
#explosion_y = int(input("Enter the y-coordinate for the explosion: "))  
explosion_x, explosion_y = 20, 20
# Call the function to show the explosion animation
create_explosion(explosion_x, explosion_y)    
# Quit the game
create_explosion(explosion_x + 50, explosion_y + 50)
create_explosion(explosion_x + 100, explosion_y + 100)

   