# Solar System Simulation Catalogue
A simulation of ours and all currently known solar systems in the Universe using NASA's Exoplanet archive and OpenData Solar System API with space and time scales control.
[Try it out here](https://melsamad.github.io/planet_simulation/)

<img width="1679" height="892" alt="Screenshot 2026-09-05 at 1 51 29 PM" src="https://github.com/user-attachments/assets/bc118030-d27e-4c71-8242-94fc7764fc3e" />

## Quick Start
- Open the following URL: https://melsamad.github.io/planet_simulation/
- Wait until loading is done and press the screen to start the simulation 

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

## Credits / Acknowledgements
- [Planet Simulation Tutorial in Python using Pygame - Tech with Tim](https://www.youtube.com/watch?v=WTLPmUHTPqo&t=1s)
- [Open Exoplanet Catalogue](https://openexoplanetcatalogue.com/)
- [The Solar System OpenData](https://api.le-systeme-solaire.net/en/)
