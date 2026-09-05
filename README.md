# Solar System Simulation Catalogue
A simulation of ours and all currently known solar systems in the Universe using the Open Exoplanet Catalogue and OpenData Solar System API with space and time scales control.
[Try it out here](https://melsamad.github.io/planet_simulation/)

<img width="1679" height="892" alt="Screenshot 2026-09-05 at 1 51 29 PM" src="https://github.com/user-attachments/assets/bc118030-d27e-4c71-8242-94fc7764fc3e" />
<img width="1679" height="892" alt="Screenshot 2026-09-05 at 2 37 56 PM" src="https://github.com/user-attachments/assets/761d67aa-ecf7-454f-8c58-476ccb72eee8" />

## Quick Start
- Open the following URL: https://melsamad.github.io/planet_simulation/
- Wait until loading is done and press the screen to start the simulation
- To explore simulations of all known solar systems, click on "Explore other Solar Systems" on the left

You will be greeted by a simulation of our solar system:
<img width="1679" height="892" alt="Screenshot 2026-09-05 at 2 35 14 PM" src="https://github.com/user-attachments/assets/2140c657-efe8-4b91-8dd9-428cb8c3278f" />

## Features 
- Basic information about our solar system, accessible by pressing on a planet or our Sun
- TIMESCALE: control how fast you're moving in time
- SPACESCALE: zoom in or out to find planets orbiting their Sun at a distance, or vice versa, find planets that orbit so close to their Sun they look stuck to it
- Browsing and Filtering through a record of almost 4,000 star systems

## How to run it locally 
You can run this project locally on your desktop. This is especially useful if you want to change your source of information (in this case, you want to switch to another exoplanet catalogue), include extra info about other solar systems or alter the layout to your liking. The following steps explain how to do so:

- Ensure you have Python 3.10+ installed on your machine.
- Clone the repo: git clone https://github.com/melsamad/planet_simulator.git
cd planet_simulator
- Install the following dependencies: pip install pygame pillow pygbag
- Run fix_images.py once locally to clean ICC color profiles (avoids issues in WebAssembly)
- Launch the Pygbag WebAssembly server with this command: python -m pygbag .
- View the project in your browser on http://localhost:8000

## How it works 
  This simulation runs entirely on pygame (an open-source python library for 2D games and similar applications) using actual physics. It was compiled to WebAssembly via Pygbag. There are two distinct parts: you've got the simulation of our solar system (which is sort of like a welcome page I would say) and the simulations of all the other solar systems we know of. 
  Essentially, we calculate the gravitational force acting upon each planet (Newton's Law of Universal Gravitation) and proceed to calculate and update its x and y coordinates as it orbits its star. For the simulation of our solar system, this data is according to the OpenData Solar System. As for all the other simulations, we retrieve the data from the well-known Open Exoplanet Catalogue, which is regularly maintained. There are two ways to do this: you can either download the xml file and just directly fetch its data in your code, or you can fetch the data from their official [github repo](https://github.com/OpenExoplanetCatalogue/oec_gzip/). I chose to download the xml file because I didn't want to face Cross-Origin Resource Sharing restrictions on APIs when deploying the project on the web. This file gives back data about the name of the system, stellar properties of its star(s) and the list of planets orbiting it with their own properties respectively. 

## Notes
  This project was done in honor of the successful launch of the Nancy Grace Roman Space Telescope, which absolutely blows my mind with its stunning complexity and capabilities to image new worlds. I look forward to seeing the telescope's data and hope to someday work on exoplanets myself. 
  This project is also a very basic attempt of showing people the true scale of our Universe and the unknown through a very basic layout. I hope that someone scrolling through the simulations and taking their time to look at them realizes that what they are looking at exists out there, not just as a dot but as an entire world. 

## Credits / Acknowledgements
- [Planet Simulation Tutorial in Python using Pygame - Tech with Tim](https://www.youtube.com/watch?v=WTLPmUHTPqo&t=1s)
- [Open Exoplanet Catalogue](https://openexoplanetcatalogue.com/)
- [The Solar System OpenData](https://api.le-systeme-solaire.net/en/)
