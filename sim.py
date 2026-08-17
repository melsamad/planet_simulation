import pygame
import math

pygame.init()

# setting up pygame window
width, height = 1000, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Miryam's Expanding Solar System Simulation")


back_color = (20, 20, 40) # dark blue color
yellow = (255, 255, 0)


# let's put some planets

class Planet:

    AU = 149.6e6 * 1000 # in meters 
    G = 6.67428-11 
    SCALE = 200 / AU # not sure if my scale is correct yet I'll do the math later
    TIMESTEP = 3600*24 # one day (in seconds)

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    # drawing the planet
    def draw(self, win): 
        x = self.x * self.SCALE + width / 2
        y = self.y * self.SCALE + height / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

# pygame event loop, only event is moving planets here
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 40, yellow, 1.98892*10**30, "Sun")
    sun.sun = True

    planets = [sun]

    while run:
        clock.tick(60) # 60 frames per second
        window.fill(back_color)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # only event is user quitting the window
                run = False

        for planet in planets:
            planet.draw(window)

        pygame.display.update() # takes drawing actions since last update 

    pygame.quit()

main()