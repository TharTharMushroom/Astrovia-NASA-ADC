from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import numpy as np
import random

app = Ursina()

# Window Title info
window.title = 'Ursina Solar System Simulation'
window.fps_counter.enabled = True
max_frames = 30

window.fps_counter.max = 30


music = Audio(sound_file_name='assets/leonell-cassio-music.mp3', loop=True, autoplay=True, volume=10)

earth_t = venus_t = mars_t = mercury_t = jupiter_t = saturn_t = uranus_t = neptune_t = -np. pi

able_text = True

paused = False


def update():
    if not paused:
        global earth_t, venus_t, mars_t, mercury_t, jupiter_t, saturn_t, uranus_t, neptune_t
        mercury_t += .47 * time.dt
        venus_t += .35 * time.dt
        earth_t += .29 * time.dt
        mars_t += .24 * time.dt
        jupiter_t += .13 * time.dt
        saturn_t += .0969 * time.dt
        uranus_t += .0681 * time.dt
        neptune_t += .0543 * time.dt
        angle = np.pi * 40 / 180

        radius_1 = 96.75 + 500
        mercury.x = np.cos(mercury_t) * radius_1
        mercury.z = np.sin(mercury_t) * radius_1

        radius_2 = 180.75 + 600
        venus.x = np.cos(venus_t + angle) * radius_2
        venus.z = np.sin(venus_t + angle) * radius_2

        radius_3 = 250 + 750
        earth.x = np.cos(earth_t + angle * 2) * radius_3
        earth.z = np.sin(earth_t + angle * 2) * radius_3

        radius_4 = 381 + 800
        mars.x = np.cos(mars_t + angle * 3) * radius_4
        mars.z = np.sin(mars_t + angle * 3) * radius_4

        radius_5 = 1300 + 800
        jupiter.x = np.cos(jupiter_t + angle * 4) * radius_5
        jupiter.z = np.sin(jupiter_t + angle * 4) * radius_5

        radius_6 = 2375+800
        saturn.x = np.cos(saturn_t + angle * 5) * radius_6
        saturn.z = np.sin(saturn_t + angle * 5) * radius_6

        radius_7 = 4800+800
        uranus.x = np.cos(uranus_t + angle * 6) * radius_7
        uranus.z = np.sin(uranus_t + angle * 6) * radius_7

        radius_8 = 7525+800
        neptune.x = np.cos(neptune_t + angle * 7) * radius_8
        neptune.z = np.sin(neptune_t + angle * 7) * radius_8


t = -np. pi


def input(key):
    global paused
    if held_keys['space']:
        player.y += 800 * time.dt
    if held_keys['control']:
        player.y -= 800 * time.dt
    if key == 'p':
        paused = True
    if key == 'u':
        paused = False
    if key == '1':
        player.position = (mercury.x - 20, mercury.y, mercury.z - 20)
    if key == '2':
        player.position = (venus.x - 20, venus.y, venus.z - 30)
    if key == '3':
        player.position = (earth.x - 40, earth.y, earth.z - 20)
    if key == '4':
        player.position = (mars.x - 50, mars.y, mars.z - 50)
    if key == '5':
        player.position = (jupiter.x - 200, jupiter.y, jupiter.z - 200)
    if key == '6':
        player.position = (saturn.x - 200, saturn.y, saturn.z - 200)
    if key == '7':
        player.position = (uranus.x - 200, uranus.y, uranus.z - 200)
    if key == '8':
        player.position = (neptune.x - 200, neptune.y, neptune.z - 200)


class Planet(Entity):

    def __init__(self, x, y, z, scale, texture, name):
        super().__init__()
        self.model = 'sphere'
        self.collider = 'sphere'
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.shader = lit_with_shadows_shader
        self.texture = texture
        self.name = name

        self.sun = False

    # Displays Name of the planet on the screen
    def input(self, key):
        def text_abler():
            global able_text
            able_text = True
        global paused, able_text
        if self.hovered and able_text:
            name_text = Text(text=self.name)
            able_text = False
            name_text.appear(speed=0.15)
            destroy(name_text, delay=3)
            invoke(text_abler, delay=3)

# Creates Sun


sun = Planet(0, 0, 0, 800, 'assets/8k_sun', "Sun")
sun.sun = True
# Makes sun exempt from the shader
sun.unlit = True

# light from sun
light1 = PointLight(shadows=True, color=color.red)

# Other Planets
earth = Planet(-250+800, 0, 0, 8*10, 'assets/earth', "Earth")

mars = Planet(-381+800, 0, 0, 12*10, 'assets/mars', "Mars")

mercury = Planet(96.75+500, 0, 0, 4*10, 'assets/mercury', "Mercury")

venus = Planet(180.75+500, 0, 0, 6*10, 'assets/venus1', "Venus")

jupiter = Planet(1300+800, 0, 0, 89.6*5, 'assets/jupiter', "Jupiter")

saturn = Planet(2375+800, 0, 0, 75.68*5, 'assets/saturn', "Saturn")

# Saturn's Ring
ring = Entity(model=load_model('torus.blend'),
              shader=lit_with_shadows_shader,
              collider='mesh',
              position=(saturn.x, saturn.y, saturn.z),
              scale=300,
              scale_y=1)
ring.color = color.white
ring.rotation_x = 45
ring.reparent_to(saturn)

uranus = Planet(4800+800, 0, 0, 32.48*5, 'uranus', "Uranus")

neptune = Planet(7525+800, 0, 0, 31.04*5, 'neptune', "Neptune")


# Asteroids Belt
asteroid = Entity(model='asteroid', position=(1400, 0, 0), texture='asteroid', shader=lit_with_shadows_shader, scale=3.5)
asteroid.scale = 0.5
asteroid.color = color.light_gray
asteroid_t = uranus_t
asteroid_radius = 1400
asteroid_num_var = 360

for i in range(asteroid_num_var):
    clone = duplicate(asteroid, texture='asteroid', color=color.light_gray, shader=lit_with_shadows_shader)
    asteroid_t += 120
    clone.rotation = (random.randint(0, 360), random.randint(0, 360), random.randint(0, 360))
    clone.z = (random.randint(-50, 50))
    clone.x = np.cos(asteroid_t) * asteroid_radius
    clone.z = np.sin(asteroid_t) * asteroid_radius
asteroid.visible = False

Sky(texture="assets/space")

player = FirstPersonController(position=(0, 3500, 0), gravity=0, speed=400)

app.run()