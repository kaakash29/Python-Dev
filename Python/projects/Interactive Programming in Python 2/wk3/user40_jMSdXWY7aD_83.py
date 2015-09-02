# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
SHIP_ACCL = 0.3
SHIP_FRIC = 0.015
ANG_VEL = 0.1
MIS_VEL_FAC = 3

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self._exploding_ship_center = [info.get_center()[0] + 90, info.get_center()[1]]
        self._forward = 0
        
        
    def draw(self,canvas): 
        
        if self.thrust:
            centre = self._exploding_ship_center
        else:
            centre = self.image_center
        
        canvas.draw_image(self.image, 
                          centre,
                          self.image_size,
                          self.pos, 
                          self.image_size,
                          self.angle)

    def update(self):
                       
        # Accl to vector
        self._forward = [angle_to_vector(self.angle)[0] , angle_to_vector(self.angle)[1]]
        
        # Updating for the Thrust
        if self.thrust:  
            self.vel[0] += self._forward[0] * SHIP_ACCL
            self.vel[1] += self._forward[1] * SHIP_ACCL       
            
        # Position Update 
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
        # FricTion Update
        self.vel[0] *= (1 - SHIP_FRIC)
        self.vel[1] *= (1 - SHIP_FRIC)
        
        # Updating Angle with Angular Velocity 
        self.angle += self.angle_vel
        
    def thrust_sound(self, on):
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    
    def shoot(self):
        global a_missile
        angle_vector = angle_to_vector(self.angle)
        adj_angle_vector = [angle_vector[0]*self.radius , angle_vector[1]*self.radius]
        a_missile = \
            Sprite( [ self.pos[0] + adj_angle_vector[0],
                      self.pos[1] + adj_angle_vector[1] ],
               
                    [ self.vel[0] + self._forward[0] * MIS_VEL_FAC ,
                      self.vel[1] + self._forward[1] * MIS_VEL_FAC  ], 
                    
                    0, 0, 
                    missile_image, 
                    missile_info,
                    missile_sound)

            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, 
                          self.image_center,
                          self.image_size,
                          self.pos, 
                          self.image_size,
                          self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT        
        self.angle += self.angle_vel

    
# the handler functions

# draw hanfler
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw score and lives
    canvas.draw_text("Lives  " + str(lives), (WIDTH/32, 50), 20, 'Gold')
    canvas.draw_text("Score  " + str(score), (WIDTH*7/8 ,50), 20, 'Gold')

# keyhandler and its helper fns()
def upkey_pressed():
    my_ship.thrust = True
    my_ship.thrust_sound(True)

def upkey_released():
    my_ship.thrust = False
    my_ship.thrust_sound(False)

def leftkey_pressed():
    my_ship.angle_vel = -ANG_VEL

def leftkey_released():
    my_ship.angle_vel = 0

def rightkey_pressed():
    my_ship.angle_vel = ANG_VEL

def rightkey_released():
    my_ship.angle_vel = 0
    
def space_pressed():
    my_ship.shoot()

def space_released():
    pass
    
KEYDOWN = {simplegui.KEY_MAP["up"]:upkey_pressed,
           simplegui.KEY_MAP["left"]:leftkey_pressed,
           simplegui.KEY_MAP["right"]:rightkey_pressed,
           simplegui.KEY_MAP["space"]:space_pressed}

KEYUP   = {simplegui.KEY_MAP["up"]:upkey_released,
           simplegui.KEY_MAP["left"]:leftkey_released,
           simplegui.KEY_MAP["right"]:rightkey_released,
           simplegui.KEY_MAP["space"]:space_released}

def keyup(key):
    """
    Handles the key release event on al the keys.
    """
    if key in KEYDOWN.keys():
        KEYUP[key]()
    else:
        pass

def keydown(key):
    """
    Handles the key down event on all the keys
    """   
    if key in KEYDOWN.keys():
        KEYDOWN[key]()
    else:
        pass

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    a_rock = Sprite([random.randrange(800), random.randrange(600)],
                    [(random.random() - 0.5), (random.random() - 0.5)],
                    2 * math.pi * random.random(), random.random()/5, 
                    asteroid_image,
                    asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
