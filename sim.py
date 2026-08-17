import pygame
import math

pygame.init()

# setting up pygame window
width, height = 1000, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Miryam's Expanding Solar System Simulation")
back_color = (20, 20, 40) # dark blue color


# let's put some planets

class Planet:
    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

# pygame event loop, only event is moving planets here
def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60) # 60 frames per second
        window.fill(back_color)
        pygame.display.update() # takes drawing actions since last update 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # only event is user quitting the window
                run = False

    pygame.quit()

main()