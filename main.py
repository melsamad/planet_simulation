import pygame
import math
from PIL import Image
import glob
import os
import exoplanet
import asyncio
import json
import sys
    

# Clean ICC Profiles from PNGs before loading them into Pygame
def clean_icc_profiles():
    for filename in glob.glob("**/*.png", recursive=True):
        try:
            with Image.open(filename) as img:
                # Remove ICC profile data from image info dictionary
                info = img.info
                info.pop("icc_profile", None)
                
                # Re-save image without the ICC profile metadata
                img.save(filename, **info)
            print(f"Fixed color profile for: {filename}")
        except Exception as e:
            print(f"Could not process {filename}: {e}")

clean_icc_profiles()


back_color = (20, 20, 40) # dark blue color
yellow = (255, 255, 0)
blue = (100, 150, 235)
red = (188, 39, 50)
mustard_yellow = (225, 173, 1)
grey = (229, 229, 229)
white = (255, 255, 255)
orange = (255, 165, 0)

PLANET_API_IDS = {
    "Sun": "soleil",
    "Mercury": "mercure",
    "Venus": "venus",
    "Earth": "terre",
    "Mars": "mars",
    "Jupiter": "jupiter",
    "Saturn": "saturne",
    "Uranus": "uranus",
    "Neptune": "neptune",
    "Pluto": "pluton"
}

FALLBACK_DATA = {
   "Sun": {"bodyType": "Star", "avgTemp": 5778, "inclination": 0.0, "axialTilt": 7.25},
    "Mercury": {"bodyType": "Planet", "avgTemp": 440, "inclination": 7.0, "axialTilt": 0.03},
    "Venus": {"bodyType": "Planet", "avgTemp": 737, "inclination": 3.39, "axialTilt": 177.36},
    "Earth": {"bodyType": "Planet", "avgTemp": 288, "inclination": 0.0, "axialTilt": 23.44},
    "Mars": {"bodyType": "Planet", "avgTemp": 210, "inclination": 1.85, "axialTilt": 25.19},
    "Jupiter": {"bodyType": "Planet", "avgTemp": 165, "inclination": 1.3, "axialTilt": 3.13},
    "Saturn": {"bodyType": "Planet", "avgTemp": 134, "inclination": 2.49, "axialTilt": 26.73},
    "Uranus": {"bodyType": "Planet", "avgTemp": 76, "inclination": 0.77, "axialTilt": 97.77},
    "Neptune": {"bodyType": "Planet", "avgTemp": 72, "inclination": 1.77, "axialTilt": 28.32},
    "Pluto": {"bodyType": "Dwarf Planet", "avgTemp": 44, "inclination": 17.16, "axialTilt": 122.53}
}

planet_images = [
    "planets/earth.png",
    "planets/jupiter.png",
    "planets/mars.png",
    "planets/mercury.png",
    "planets/neptune.png",
    "planets/saturn.png",
    "planets/uranus.png",
    "planets/venus.png"
]

async def get_planet_info(planet, window, width, title_font):
    
    api_id = PLANET_API_IDS.get(planet, planet.lower())
    url = f'https://api.le-systeme-solaire.net/rest/bodies/{api_id}'

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    data = None
    line_space = 1

    try:
        if sys.platform == "emscripten":
           
            import platform
            async with platform.fopen(url, headers=headers) as response:
                content = await response.read()
                data = json.loads(content)
        else:
            # Desktop Python (urllib avoids WebAssembly bundle dependencies)
            import urllib.request
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))

    except Exception as e:
        print(f"Error fetching data for {planet} ({api_id}): {e}")
        data = FALLBACK_DATA.get(planet)

   
    if data:
        infos = [
            f"Object Name: {planet}",
            f"Type: {data.get('bodyType', 'Unknown')}",
            f"Average Temp: {data.get('avgTemp', 'N/A')} K",
            f"Inclination: {data.get('inclination', 'N/A')}°",
            f"Axial Tilt: {data.get('axialTilt', 'N/A')}°",
        ]

        for info in infos:
            line_space += 20
            info_message = title_font.render(info, True, back_color)
            info_space = info_message.get_rect(center=(width // 2, 350 + line_space))
            pygame.draw.rect(window, white, info_space)
            window.blit(info_message, info_space)


# let's put some planets
class Planet:

    AU = 149.6e6 * 1000 # in meters 
    G = 6.67428e-11 
    # TIMESTEP = 3600*4 # one day (in seconds)

    def __init__(self, x, y, radius, color, mass, name, image):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.image = image
        self.is_imaged = True

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

        self.loaded_img = None

        if self.is_imaged and os.path.exists(self.image):
            try: 
                img = pygame.image.load(self.image).convert_alpha()
                # Diameter = radius * 2
                diameter = self.radius * 2
                self.loaded_img = pygame.transform.scale(img, (diameter, diameter))
            except Exception as e:
                print(f"Failed to load image for {self.name}: {e}")
                self.is_imaged = False
                self.loaded_img = None
        else:
            self.is_imaged = False
            self.loaded_img = None

        


    # drawing the planet
    def draw(self, win, scale, width, height, window, title_font, font, signature_font): 
        x = self.x * scale + width / 2
        y = self.y * scale + height / 2

        title = title_font.render("An Expanding Simulation of our Solar System", 1, white)
        signature = signature_font.render("Amata's Creations", 1, white)

        
        window.blit(title, (width / 3, 20))
        window.blit(signature, (width - 120, height - 30))

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * scale + width / 2
                y = y * scale + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2) # drawing the orbit

        if self.is_imaged and os.path.exists(self.image) and self.loaded_img is not None:
           rect = self.loaded_img.get_rect(center=(x, y)) # coordinates of the planets as they're moving
           window.blit(self.loaded_img, rect)

        else:
            pygame.draw.circle(window, self.color, (x, y), self.radius)
            
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
    def update_position(self, planets, timescale):

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue 
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # velocity
        self.x_vel += total_fx / self.mass * timescale
        self.y_vel += total_fy / self.mass * timescale

        # distance is updated (v = d / t <=> d = v * t)
        self.x += self.x_vel * timescale
        self.y += self.y_vel * timescale
        self.orbit.append([self.x, self.y]) # adding a point to orbit list

        if len(self.orbit) > 100 and self.name == 'Moon':
            self.orbit.pop(0)



# pygame event loop
async def main():

    # setting up pygame window
    width, height = 1500, 800
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Miryam's Expanding Solar System Simulation")
    run = True
    clock = pygame.time.Clock()

    scale_pixels = 200
    sim_scale = scale_pixels / Planet.AU

    # fonts
    font = pygame.font.Font(None, 16) # how to initialize font
    title_font = pygame.font.Font(None, 30) # how to initialize font
    signature_font = pygame.font.Font(None, 12) # how to initialize font
    
    timescale = 3600
    timescale_hours = timescale / 3600


    # settings icon
    settings_img = pygame.image.load("settings.png").convert_alpha()
    settings_img = pygame.transform.scale(settings_img, (50, 50))
    icon_rect = settings_img.get_rect(topright=(width - 20, 20))

    # playing with the time scale icon
    # add icon
    add_img = pygame.image.load("add.png").convert_alpha()
    add_img = pygame.transform.scale(add_img, (60, 60))
    add_icon = add_img.get_rect(topright=(70, 70))

    # substract icon
    substract_img = pygame.image.load("substract.png").convert_alpha()
    substract_img = pygame.transform.scale(substract_img, (60, 60))
    substract_icon = substract_img.get_rect(topright=(150, 70))

    # remove icon for object info
    remove_img = pygame.image.load("remove.png").convert_alpha()
    remove_img = pygame.transform.scale(remove_img, (40, 40))
    remove_icon = remove_img.get_rect(topright=(1000, 250))
    window.blit(remove_img, remove_icon)


    # space & time scale display
    space_scale_info = font.render(f"SPACE SCALE: {sim_scale}", 1, back_color)

    # explore all known solar systems 
    exoplanets_explore = font.render("Explore other Solar Systems", 1, back_color)

    display_message = False


    sun = Planet(0, 0, 70, yellow, 1.98892*10**30, "Sun", "planets/sun.png")
    sun.sun = True

    # planets & their velocities
    mercury = Planet(0.387*Planet.AU, 0, 12, grey, 3.30104*10**23, "Mercury", "planets/mercury.png")
    mercury.y_vel = -47.4 * 1000
   

    venus = Planet(-0.72*Planet.AU, 0, 14, mustard_yellow, 4.86732*10**24, "Venus", "planets/venus.png")
    venus.y_vel = -35.02 * 1000
    

    earth = Planet(-1*Planet.AU, 0, 16, blue, 5.974*10**24, "Earth", "planets/earth.png")
    earth.y_vel = 29.783 * 1000
    

    mars = Planet(1.52*Planet.AU, 0, 13, red, 6.41693*10**23, "Mars", "planets/mars.png")
    mars.y_vel = 24.077 * 1000
    

    # initializing Earth's Moon
    moon_distance = 0.09 * Planet.AU
    lunar_orbital_vel = math.sqrt(Planet.G * 5.974*10**24 / moon_distance)


    moon = Planet(-1 * Planet.AU, 0 + moon_distance, 4, grey, 7.342*10**22, "Moon", "planets/earth.png")
    moon.x_vel = lunar_orbital_vel
    moon.y_vel = 29.783 * 1000
    

    # the gas giants
    jupiter = Planet(5.2*Planet.AU, 0, 24, orange, 1.89813*10**27 ,"Jupiter", "planets/jupiter.png")
    jupiter.y_vel = 13.06 * 1000
    

    saturn = Planet(9.5*Planet.AU, 0, 22, mustard_yellow, 5.68*10**26 ,"Saturn", "planets/saturn.png")
    saturn.y_vel = 9.69 * 1000
    

    uranus = Planet(19.2*Planet.AU, 0, 22, blue, 8.68*10**25 ,"Uranus", "planets/uranus.png")
    uranus.y_vel = 6.8 * 1000
   

    neptune = Planet(30.06*Planet.AU, 0, 22, blue, 1.024*10**26 ,"Neptune", "planets/neptune.png")
    neptune.y_vel = 5.43 * 1000
    

    pluto = Planet(39.5*Planet.AU, 0, 10, grey, 1.30900*10**22 ,"Pluto", "planets/pluto.png")
    pluto.y_vel = 4.74 * 1000
    


    planets = [
        sun, 
        earth, 
        mars, 
        venus, 
        mercury, 
        moon, 
        jupiter,
        saturn,
        uranus,
        neptune,
        pluto
        ]

    sub_setps = 3

    is_info_displayed = False
    which_object = ""

    current_state = "MAIN_MENU"


    while run:

        hours = "hours"

        clock.tick(60) # 60 frames per second
        window.fill(back_color)
        window.blit(space_scale_info, (10, 0))
        exoplanet_space = exoplanets_explore.get_rect(center=(120, 200))
        pygame.draw.rect(window, white, exoplanet_space)
        window.blit(exoplanets_explore, exoplanet_space)


        if timescale_hours > 1.0:
                hours = "hours"
        elif timescale_hours == 1.0:
                hours = "hour"
                
        time_scale_info = font.render(f"TIME SCALE: {timescale_hours} {hours}", 1, white)
        window.blit(time_scale_info, (10, 20))

        for _ in range(sub_setps):
            for planet in planets:
                planet.update_position(planets, timescale)
                       
        for planet in planets:
            planet.draw(window, sim_scale, width, height, window, title_font, font, signature_font)


        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    scale_pixels +=100
                    print(sim_scale)
                    print(scale_pixels)

                elif event.key == pygame.K_o:
                    scale_pixels = max(10, scale_pixels - 100)
                    print(sim_scale)
                    print(scale_pixels)

                sim_scale = scale_pixels / Planet.AU

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if icon_rect.collidepoint(event.pos):
                        display_message = not display_message
                        print("works")

                    if add_icon.collidepoint(event.pos):
                        timescale += 3600

                    timescale_hours = timescale / 3600

                    if substract_icon.collidepoint(event.pos) and timescale > 3600:
                        timescale -=3600

                    timescale_hours = timescale / 3600

                    for object in planets:
                        screen_x = int(width / 2 + object.x * sim_scale)
                        screen_y = int(height / 2 + object.y * sim_scale) 
                        rect = object.loaded_img.get_rect(center=(screen_x, screen_y))
                        print(object.x, object.y)
                        if rect.collidepoint(event.pos):
                            is_info_displayed = True
                            which_object = object.name

                    if remove_icon.collidepoint(event.pos):
                        is_info_displayed = not is_info_displayed

                    if exoplanet_space.collidepoint(event.pos):
                        current_state = "EXOPLANET_SIM"

        if current_state == "EXOPLANET_SIM":
            next_state = await exoplanet.main_exoplanet()

            if next_state == "MAIN_MENU":
                current_state = "MAIN_MENU"

                    
        if is_info_displayed: 
            await get_planet_info(which_object, window, width, title_font)
            window.blit(remove_img, remove_icon)    
                            

        window.blit(settings_img, icon_rect)
        window.blit(add_img, add_icon)
        window.blit(substract_img, substract_icon)


        if display_message:
            message = font.render("Press 'I' on your keyboard to Zoom In.\nPress 'O' on your keyboard to Zoom Out.", True, white)
            message_space = message.get_rect(center=(width // 2, height // 2))
            pygame.draw.rect(window, back_color, message_space)
            window.blit(message, message_space)
            

        pygame.display.update() # takes drawing actions since last update 

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())