import pygame
import math

pygame.init()

# setting up pygame window
width, height = 1000, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Miryam's Expanding Solar System Simulation")


back_color = (20, 20, 40) # dark blue color
yellow = (255, 255, 0)
blue = (100, 150, 235)
red = (188, 39, 50)
mustard_yellow = (225, 173, 1)
grey = (229, 229, 229)
white = (255, 255, 255)

font = pygame.font.SysFont("comicsans", 16) # how to initialize font
title_font = pygame.font.SysFont("Ariel", 30) # how to initialize font
signature_font = pygame.font.SysFont("comicsans", 12) # how to initialize font


# let's put some planets
class Planet:

    AU = 149.6e6 * 1000 # in meters 
    G = 6.67428e-11 
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

        title = title_font.render("An Expanding Simulation of our Solar System", 1, white)
        signature = signature_font.render("Amata's Creations", 1, white)

        window.blit(title, (width / 3.5, 20))
        window.blit(signature, (870, height - 30))

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + width / 2
                y = y * self.SCALE + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2) # drawing the orbit

        pygame.draw.circle(win, self.color, (x, y), self.radius) # how we tell our program to draw a circle

        if not self.sun:
            distance_text = font.render(self.name, 1, white)
            window.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        # calculate force of attraction
        force = self.G * self.mass * other.mass / distance**2

        # break down force into x & y 
        theta = math.atan2(distance_y, distance_x)
        x_force = math.cos(theta) * force
        y_force = math.sin(theta) * force

        return x_force, y_force

    # make the planets move according to all forces acting upon them
    def update_position(self, planets):

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue 
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # velocity
        self.x_vel += total_fx / self.mass * self.TIMESTEP 
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # distance is updated (v = d / t <=> d = v * t)
        self.x += self.x_vel * self.TIMESTEP 
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append([self.x, self.y]) # adding a point to orbit list



# pygame event loop
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 40, yellow, 1.98892*10**30, "Sun")
    sun.sun = True

    # planets & their velocities
    mercury = Planet(0.387*Planet.AU, 0, 12, grey, 3.30104*10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(-0.72*Planet.AU, 0, 14, mustard_yellow, 4.86732*10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1*Planet.AU, 0, 16, blue, 5.974*10**24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(1.52*Planet.AU, 0, 13, red, 6.41693*10**23, "Mars")
    mars.y_vel = 24.077 * 1000
   

    planets = [sun, earth, mars, venus, mercury]


    while run:
        clock.tick(60) # 60 frames per second
        window.fill(back_color)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # only event is user quitting the window
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)

        pygame.display.update() # takes drawing actions since last update 

    pygame.quit()

main()