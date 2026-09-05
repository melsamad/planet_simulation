import gzip
#import io
#import urllib.request
import xml.etree.ElementTree as ET
import pygame
import math
import asyncio


# color palette
back_color = (20, 20, 40)
panel_color = (10, 10, 25)
white = (255, 255, 255)
yellow = (255, 220, 50)
cyan = (0, 200, 255)
orange = (255, 140, 0)
gray = (180, 180, 180)


def fetch_and_display_data():

    # FOR THOSE WHO WANT TO FETCH DATA WITHOUT DOWNLOADING THE FILE (don't forget to import urllib.request)

    #url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    #req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #response = urllib.request.urlopen(req)
    # with gzip.GzipFile(fileobj=io.BytesIO(data.read())) as gz_file:
        # tree = ET.parse(gz_file)
        # root = tree.getroot()

    
    tree = ET.parse("systems.xml")
    root = tree.getroot()

    systems = []


    for sys in root.findall(".//system"):
        sys_data = {
            "name": sys.findtext("name", "Unknown System"),
            "stars":[]
        }

        for star in sys.findall(".//star"):
            star_data = {
                "name":star.findtext("name", "Star"),
                "mass":float(star.findtext("mass")) if star.findtext("mass") else 1.0,
                "radius": float(star.findtext("radius")) if star.findtext("radius") else 1.0,
                "planets": []
            }

            # making sure it doesn't crash if not all data is available
            for planet in star.findall(".//planet"):
                sma = float(planet.findtext("semimajoraxis")) if planet.findtext("semimajoraxis") else None
                period = float(planet.findtext("period")) if planet.findtext("period") else None

                if sma is None and period is not None:
                    period_years = period / 365.25
                    sma = (period_years**2 * star_data["mass"]) ** (1/3)

                if sma is not None:
                    p_data = {
                        "name": planet.findtext("name", "Exoplanet"),
                        "semimajoraxis": sma,
                        "eccentricity": float(planet.findtext("eccentricity")) if planet.findtext("eccentricity") else 0.0,
                        "mass": float(planet.findtext("mass")) if planet.findtext("mass") else 0.00318,
                        "radius": float(planet.findtext("radius")) if planet.findtext("radius") else 0.1,
                    }

                    star_data["planets"].append(p_data)

                if star_data["planets"]:
                    sys_data["stars"].append(star_data)         

        if sys_data["stars"]:
            systems.append(sys_data)

    return systems


# class for celestial objects: planet & star
class CelestialObject:
    AU = 1.496e11
    G = 6.67430e-11
    m_solar = 1.989e30
    m_jupiter = 1.898e27

    def __init__(self, name, x, y, mass, radius, color):
        self.name = name
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.is_star = False

        self.x_vel = 0
        self.y_vel = 0
        self.orbit = []

    def set_circular_orbit_velocity(self, central_mass, distance):
        r = distance * self.AU
        if r > 0:
            speed = math.sqrt((self.G * central_mass) / r)
            self.y_vel = speed

    def update_position(self, central_body, timescale):
        if self.is_star:
            return

        dx = central_body.x - self.x
        dy = central_body.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            force = (self.G * self.mass * central_body.mass) / (distance ** 2)
            theta = math.atan2(dy, dx)

            acc_x = math.cos(theta) * force / self.mass
            acc_y = math.sin(theta) * force / self.mass

            self.x_vel += acc_x * timescale
            self.y_vel += acc_y * timescale

        self.x += self.x_vel * timescale
        self.y += self.y_vel * timescale

        self.orbit.append((self.x, self.y))

        if len(self.orbit) > 300:
            self.orbit.pop(0)

    def draw(self, surface, scale_px, width, height, font):
        screen_x = int(width / 2 + (self.x / self.AU) * scale_px)
        screen_y = int(height / 2 + (self.y / self.AU) * scale_px)

        if len(self.orbit) > 2 and not self.is_star:
            pts = []
            for ox, oy in self.orbit:
                px = int(width / 2 + (ox / self.AU) * scale_px)
                py = int(height / 2 + (oy / self.AU) * scale_px)
                pts.append((px, py))
            pygame.draw.lines(surface, (70, 70, 100), False, pts, 1)

        pygame.draw.circle(surface, self.color, (screen_x, screen_y), self.radius)

        label = font.render(str(self.name), True, white)
        surface.blit(label, (screen_x + self.radius + 5, screen_y - 10))



async def open_simulation(system_data, width, height, title_font, font, sim_window):
    

    star_info = system_data["stars"][0] # main star in case we're working with binary systems
    star_mass = star_info["mass"] * CelestialObject.m_solar

    central_star = CelestialObject(star_info["name"], 0, 0, star_mass, 25, yellow)
    central_star.is_star = True

    bodies = [central_star]
    planet_colors = [cyan, orange, (100, 230, 100), (220, 100, 220), (255, 100, 100)]

    max_distance = 0.1
    for i, p in enumerate(star_info["planets"]):
        sma = p["semimajoraxis"]
        max_distance = max(max_distance, sma)

        planet_body = CelestialObject(p["name"], sma * CelestialObject.AU, 0, p["mass"], max(4, int(p["radius"] * 8)), planet_colors[i % len(planet_colors)])

        planet_body.set_circular_orbit_velocity(star_mass, sma)
        bodies.append(planet_body)

    scale_pixels = (height // 2 - 80) / max_distance
    timescale = 3600 * 6

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        sim_window.fill(back_color)
        pygame.display.set_caption(f"Simulation: {system_data['name']}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                # Controls for Zoom & Time Speed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "BACK"
                elif event.key == pygame.K_i:
                    scale_pixels *= 1.25
                elif event.key == pygame.K_o:
                    scale_pixels /= 1.25
                elif event.key == pygame.K_UP:
                    timescale += 3600
                elif event.key == pygame.K_DOWN:
                    if timescale > 3600:
                        timescale -= 3600

        for body in bodies:
            if not body.is_star:
                body.update_position(central_star, timescale)
            body.draw(sim_window, scale_pixels, width, height, font)

        # Display HUD / Controls Overlay
        title_surf = title_font.render(system_data["name"], True, white)
        sim_window.blit(title_surf, (20, 20))

        hud_text = f"Zoom: 'I' / 'O' | Speed (Timescale): UP / DOWN Arrow | Press 'ESC' to return"
        hud_surf = font.render(hud_text, True, gray)
        sim_window.blit(hud_surf, (20, 60))

        time_scale_info = font.render(f"TIME SCALE: {timescale / 3600} hours", 1, white)
        sim_window.blit(time_scale_info, (10, 120))

        pygame.display.update() # takes drawing actions since last update 

        await asyncio.sleep(0)
        
    pygame.quit()



async def main_exoplanet(window):

    
    # fonts
    font = pygame.font.Font(None, 16) # how to initialize font
    search_font = pygame.font.Font(None, 22)
    title_font = pygame.font.Font(None, 28)
    # setting up pygame window
    width, height = 1500, 800
    #window = pygame.display.set_mode((width, height))
    #sim_window = pygame.display.set_mode((width, height))
    #pygame.display.set_caption("Explore all known Solar Systems")
    all_systems = fetch_and_display_data()
    filtered_systems = all_systems.copy()

    run = True
    clock = pygame.time.Clock()

    # scrolling and searching mechanism
    scroll_y = 0
    item_height = 30
    padding_left = 30
    search_bar_height = 60

    search_query = ""
    search_active = True



    while run:

        window.fill(back_color)

        clock.tick(60) # 60 frames per second

        # return to our solar system
        our_ss = font.render("Return to our Solar System", 1, back_color)
        ss_space = our_ss.get_rect(center=(1350, 750))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            elif event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * 25

            elif event.type == pygame.KEYDOWN and search_active:
                if event.key == pygame.K_BACKSPACE:
                    search_query = search_query[:-1] # removing a character from search bar
                elif event.key == pygame.K_RETURN:
                    pass
                else: 
                    search_query += event.unicode

                filtered_systems = [
                    name for name in all_systems
                    if search_query.lower() in name["name"].lower()
                ]
                scroll_y = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if ss_space.collidepoint(event.pos):
                    return "MAIN_MENU"
                start_y = search_bar_height + scroll_y
                for i, sys_data in enumerate(filtered_systems):
                    y_pos = start_y + (i * item_height)
                    if y_pos + item_height < search_bar_height or y_pos > height:
                        continue
                    system_rect = pygame.Rect(padding_left, y_pos, 400, item_height)
                    
                    if system_rect.collidepoint(event.pos):
                        await open_simulation(sys_data, width, height, title_font, font, window)
                        

        total_list_height = len(filtered_systems) * item_height
        max_scroll = max(0, total_list_height - (height - search_bar_height))
        scroll_y = max(-max_scroll, min(0, scroll_y))

        start_y = search_bar_height + scroll_y
        for i, sys_data in enumerate(filtered_systems):
            y_pos = start_y + (i * item_height)

            if y_pos + item_height < search_bar_height or y_pos > height:
                continue

            system_surface = font.render(sys_data["name"], True, white) 
            system_rect = system_surface.get_rect(topleft=(padding_left, y_pos))
            window.blit(system_surface, system_rect)
            

        pygame.draw.rect(window, back_color, (0, 0, width, search_bar_height))
        pygame.draw.line(window, white, (0, search_bar_height), (width, search_bar_height), 2)

        search_text_str = f"Search System: {search_query}" + ("|" if (pygame.time.get_ticks() // 500) % 2 == 0 else "")
        search_surface = search_font.render(search_text_str, True, white)
        window.blit(search_surface, (padding_left, 18))

        count_surface = font.render(f"Found: {len(filtered_systems)}", True, white)
        window.blit(count_surface, (width - 200, 20))
        
        pygame.draw.rect(window, white, ss_space)
        window.blit(our_ss, ss_space)

        pygame.display.update() # takes drawing actions since last update 
        await asyncio.sleep(0)
    
    pygame.quit()



