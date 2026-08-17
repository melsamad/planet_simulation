import pygame
import math

pygame.init()

# setting up pygame window
width, height = 1000, 1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Miryam's Expanding Solar System Simulation")

# pygame event loop, only event is moving planets here

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # only event is user quitting the window
                run = False

    pygame.quit()

main()