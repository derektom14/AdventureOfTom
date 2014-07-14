# The Adventure of Tom!
# A 2D platformer, your goal is to reach the end of the
# level by overcoming numerous obstacles in your way
# through a combination of skills, items, and wit.
# See 'How to Play' for more information, or just watch this video:
# http://www.youtube.com/watch?v=pCrzDWdvKq8&feature=g-crec-u

import simplegui
import math
import random
from time import time

# constants to indicate X and Y axes
X = 0
Y = 1

# constant to indicate directions
LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

# level constants
CELL_SIZE = 50
HALF_CELL_SIZE = CELL_SIZE / 2

# canvas constants
CANVAS_SIZE = [800, 600]

autocomplete = False

hex = [str(n) for n in range(10)] + [chr(n) for n in range(ord('A'),ord('G'))]

# returns the hex string representing the given RGB color
def color(r,g,b):
    return '#'+hex[r//16]+hex[r%16]+hex[g//16]+hex[g%16]+hex[b//16]+hex[b%16]

directory = "https://dl.dropboxusercontent.com/u/12509775/Game/" # directory where image and sound resources are accessed

# returns an image from the directory
def load_image(name):
    return simplegui.load_image(directory + name)

# returns a sound from the directory
def load_sound(name):
    return simplegui.load_sound(directory + name)

ready = False # whether or not all of the resources have been loaded

class Tom():
    IMAGE_SIZE = (100,100) # size of a single Tom frame
    SIZE = (100,100) # size that Tom is rendered
    IMAGE = load_image("Tom.png") # complete image sprites of Tom
    GUN = load_image("Pellet_Gun.png") # image of Tom's gun
    TERMINAL = [3,10] # terminal X and Y velocity
    
    FIRE_SOUND = load_sound("pistol-01.wav") # http://www.mediacollege.com/downloads/sound-effects/weapons/pistol-01.wav
    THRUSTER_SOUND = load_sound("thrust2.mp3") # http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3
    JUMP_SOUND = simplegui.load_sound("http://www.freesound.org/data/previews/89/89769_1386366-lq.mp3") # http://www.freesound.org/people/CGEffex/sounds/89769/
    JUMP_SOUND.set_volume(0.1)
    STEP_SOUND = simplegui.load_sound("http://www.freesound.org/data/previews/89/89769_1386366-lq.mp3") # http://www.freesound.org/people/CGEffex/sounds/89769/
    STEP_SOUND.set_volume(0.03)
    STEP_SOUND_SNOW = simplegui.load_sound("http://www.freesound.org/data/previews/89/89769_1386366-lq.mp3") # http://www.freesound.org/people/CGEffex/sounds/89769/
    STEP_SOUND_SNOW.set_volume(0.01)
    HIT_SOUND = simplegui.load_sound("http://www.mediacollege.com/downloads/sound-effects/hit/hit-pipe.wav") # http://www.mediacollege.com/downloads/sound-effects/hit/
    SLIDE_SOUND = load_sound("friction.mp3") # http://www.freesound.org/people/RutgerMuller/sounds/51153/ Rutger Muller
    FLAME_SOUND = load_sound("fire.mp3") # http://www.freesound.org/people/nthompson/sounds/47252/
    
    def __init__(self, pos):
        self.pos = pos # position
        self.frame = 0 # frame on the spritesheet
        self.left = False # whether or not left is held
        self.right = False # whether or not right is held
        self.up = False # whether or not the rocket boost button is held
        self.jump = False # whether or not the jump button is held
        self.vel = [0,0] # intended velocity
        self.delta = [0,0] # actual change in position each frame
        self.ground = '  ' # tiles Tom currently stands on
        self.gun = 0 # number of pellets remaining
        self.gun_max = 0 # maximum number of pellets
        self.arm = None # currently equipped hand weapon
        self.pellets = [] # pellets currently fired
        self.jetpack = 0 # jetpack fuel remaining
        self.jetpack_max = 0 # maximum jetpack fuel
        self.jetpack_jump = 0 # jetpack fuel used on this jump
        self.jetpack_jump_max = 0 # maximum fuel used in a single jump
        self.propel = False # whether or not the jetpack is currenly on
        self.max_health = 500 # maximum health
        self.health = 500 # current health
        self.hit = 0 # damage yet to be applied
        self.heal = 0 # health yet to be healed
        
        self.wall = 0 # wall Tom clings to, if any
        
        self.direction = 0 # direction Tom faces
        
        self.jump_keys = (32,87) # keys to jump
        self.jet_keys = (32,87) # keys to turn on jetpack
        self.disable = True # whether or not to disable direction button after a wall jump
    
    # draws Tom on the given canvas using the given camera
    def draw(self, canvas, camera):
        # jetpack sound only if it is on
        if self.propel:
            Tom.THRUSTER_SOUND.play()
        else:
            Tom.THRUSTER_SOUND.pause()
        Tom.SLIDE_SOUND.rewind()
        if self.hit % 10 < 5 and self.health > 0: # allow for flashing animation while hit
            if self.jetpack > 0: # wears jetpack
                flip = self.wall and self.vel[Y] > 0 and self.ground == '  '
                canvas.draw_image(Item.JETPACK_IMAGE, (25,25+50*int(self.propel)), (50,50), (self.pos[X] - camera.pos[X] + int(flip) * self.wall * -5,self.pos[Y]-50-camera.pos[Y]), (50,50),(0 if self.direction == 0 else (.2 if self.direction > 0 else -.2))*(-1 if flip else 1))
            if self.ground == '  ' and self.wall and self.vel[Y] > 0: # preparing for wall jump
                canvas.draw_image(Tom.IMAGE, (Tom.IMAGE_SIZE[X] * 11.5, Tom.IMAGE_SIZE[Y] * (int(self.arm != None) + 2 * int(self.wall < 0) + 0.5)), Tom.IMAGE_SIZE, (self.pos[X]-camera.pos[X] - 10*self.wall,self.pos[Y] - 36 - camera.pos[Y]), Tom.SIZE)    
                Tom.SLIDE_SOUND.play()
            elif abs(self.direction) < 0.1: # facing screen
                canvas.draw_image(Tom.IMAGE, (Tom.IMAGE_SIZE[X] * 0.5, Tom.IMAGE_SIZE[Y] * (int(self.arm != None) + 0.5)), Tom.IMAGE_SIZE, (self.pos[X]-camera.pos[X],self.pos[Y] - 40 - camera.pos[Y]), Tom.SIZE)
            else: # facing `direction`
                canvas.draw_image(Tom.IMAGE, (Tom.IMAGE_SIZE[X] * ((1 if self.direction > 0 else -1) * self.frame//5%10 + 1.5), Tom.IMAGE_SIZE[X] * (2 * int(self.direction < 0) + int(self.arm != None) + 0.5)), Tom.IMAGE_SIZE, (self.pos[X] - camera.pos[X],self.pos[Y] - 40 - camera.pos[Y]), Tom.SIZE)
            if self.arm != None: # currently carrying something, right now always a gun
                canvas.draw_image(Tom.GUN, (250,(50 if -math.pi/2 < self.arm < math.pi/2 else 150)), (500,100), self.shoulder(), (100,20), self.arm)
            for p in self.pellets: # pellets drawn here
                canvas.draw_image(Item.PELLET_IMAGE, (3,3), (6,6), camera.adjust(p.pos), (6,6))
    
    # adjusts Tom's health for damage and healing still needing to take place
    def apply_hit_heal(self):
        if self.hit:
            self.hit -= 1
            if self.heal:
                self.heal -= 1
            else:
                self.health -= 1
                if self.health <= 0:
                    self.health = 0
                    self.hit = 0
                    self.heal = 0
                    return False # dead
        elif self.heal:
            self.heal -= 1
            self.health += 1
            if self.health >= self.max_health:
                self.health = self.max_health
        return True
    
    # update Tom frame to frame, returning True if Tom is still alive after the frame
    def update(self):
        apply_friction = True # whether or not to apply friction
        accel = [0,Physics.GRAVITY] # current acceleration, gravity in y-direction
        cell = [p//CELL_SIZE for p in self.boundingbox()] # the cells that make up Tom's boundingbox
        
        if not self.apply_hit_heal():
            return False
        
        on_ground = any(Physics.DENSITY[g] > 0 for g in self.ground) # either ground is solid
        pos = tuple(self.pos)
        
        if on_ground or self.frame//1 not in (14, 14+25): # advance frame if running on ground or mid-jump until main jump frame
            self.frame += 1
            if on_ground and self.direction != 0 and self.frame%25 == 1: # Tom steps
                self.STEP_SOUND.rewind()
                self.STEP_SOUND_SNOW.rewind()
                if 'S' in self.ground:
                    self.STEP_SOUND_SNOW.play()
                else:
                    self.STEP_SOUND.play()
            self.frame %= 50 # exactly 50 frames in a loop
        
        if self.jump: # trying to jump
            if on_ground: # able to jump
                Tom.JUMP_SOUND.rewind()
                Tom.JUMP_SOUND.play()
                accel[Y] += (-5.25 - abs(self.delta[X])*0.3) * (0.7 if level.value(level.pos(self.core())) == 'S' else 1) # jumps
                self.up = False
            elif self.wall and (self.left if self.wall < 0 else self.right): # wall jumps
                Tom.JUMP_SOUND.rewind()
                Tom.JUMP_SOUND.play()
                # upward diagonal opposite of wall
                accel[Y] -= self.vel[Y]/2 + 3.5
                accel[X] += 3 * -self.wall
                # turns Tom around, and disables direction button if configured
                if self.wall  < 0:
                    if self.disable:
                        self.left = False
                    self.direction = 1
                else:
                    if self.disable:
                        self.right = False
                    self.direction = -1
                self.wall = 0 # no longer on wall
                apply_friction = False # don't apply friction to wall jump force
                self.up = False # up effectively disabled
            self.jump = False # jump key must be pressed again for this effect
        if self.up and self.jetpack > 0 and self.jetpack_jump < self.jetpack_jump_max: # up held, Tom has usable fuel
            accel[Y] -= .2
            fuel_used = (1 + max(-self.vel[Y],0))
            self.jetpack -= fuel_used
            self.jetpack_jump += fuel_used
            self.propel = True
        else:
            self.propel = False
        
        dir_old = self.direction # currently faced direction
        if self.left and not self.right: # accelerate to the left
            self.direction -= 0.5
            if self.direction < -1:
                self.direction = -1
            accel[X] += (self.direction + dir_old)/2 * (.3)
        elif self.right and not self.left: # accelerate to the right
            self.direction += 0.5
            if self.direction > 1:
                self.direction = 1
            accel[X] += (self.direction + dir_old)/2 * (.3)
        elif on_ground: # slow down
            if abs(self.direction) < 0.25:
                self.direction = 0
            elif self.direction < 0:
                self.direction += 0.25
            else:
                self.direction -= 0.25
            if abs(self.vel[X]) < 0.1:
                accel[X] = -self.vel[X]
            elif self.vel[X] < 0:
                accel[X] += 0.1
            else:
                accel[X] -= 0.1
                
        if apply_friction: # harder to slow down on lower friction surfaces
            friction = sum(Physics.FRICTION[g] for g in self.ground)
            accel[X] *= friction
        
        if self.wall and self.vel[Y] + accel[Y] > 0: # slower descent on a wall
            accel[Y] *= 0.7
        
        # apply the initial acceleration, then velocity
        self.vel[X] += accel[X] / 2
        self.pos[X] += self.vel[X]
        
        cell_new = [int(p//CELL_SIZE) for p in self.boundingbox()] # new cells occupied by Tom's boundingbox
        on_wall = 0 # by default, not on a wall
        if cell[LEFT] != cell_new[LEFT] or cell[RIGHT] != cell_new[RIGHT]: # change in x-axis cells
            box = self.boundingbox()
            side = box[LEFT] if self.vel[X] < 0 else box[RIGHT] # side to Tom's moving direction
            hits = [level.pos((side,k)) for k in (box[BOTTOM],(box[BOTTOM]+box[TOP])/2,box[TOP])] # three points where Tom may have hit something: top, middle, bottom
            collide = any(Physics.DENSITY[level.value(h)] > 0.5 for h in hits) # whether or not Tom collides with anything
            if collide:
                if Physics.DENSITY[level.value((cell[LEFT],cell[BOTTOM]+1))] == 0: # if he collides with a wall, he's on that wall
                    on_wall = 1 if self.vel[X] > 0 else -1
                # shift him to no longer intersect with the collision cells
                if self.vel[X] > 0:
                    self.pos[X] = self.pos[X] - side%CELL_SIZE - .000000001
                else:
                    self.pos[X] = self.pos[X] + (-side)%CELL_SIZE + .000000001
                    
                if not self.left and not self.right:
                    self.vel[X] = 0 # stops completely on collision
                else:
                    self.vel[X] /= 100 # effectively stopped, but may still face that direction
            else:
                for h in hits: # Tom uses item in each new cell
                    c = level.value(h)
                    if c in '.gj+BO':
                        level.items[h].activate(self)
                        if c != 'B':
                            level[h[Y]][h[X]] = ' '
        
        #apply the second half of the velocity
        self.vel[X] += accel[X] / 2
        # ensure Tom doesn't exceed terminal velocity
        terminal = Tom.TERMINAL[X] / 3 if level.value(level.pos(self.core())) == 'S' else Tom.TERMINAL[X]
        if self.vel[X] > terminal:
            self.vel[X] = terminal
        elif self.vel[X] < -terminal:
            self.vel[X] = -terminal
        
        # apply the initial acceleration, then velocity
        self.vel[Y] += accel[Y] / 2
        if self.vel[Y] < 0: # going upwards, there is effectively no ground
            self.ground = '  '
        self.pos[Y] += self.vel[Y]
        
        cell_new = [int(p//CELL_SIZE) for p in self.boundingbox()] # new cells occupied by Tom's boundingbox
        if cell[TOP] != cell_new[TOP] or cell[BOTTOM] != cell_new[BOTTOM]: # change in y-axis cells
            down = self.vel[Y] > 0 # whether or not moved down
            box = self.boundingbox()
            side = box[TOP] if self.vel[Y] < 0 else box[BOTTOM] # side to Tom's moving direction
            hits = [level.pos((k,side)) for k in (box[LEFT], box[RIGHT])] # two points where Tom may have hit something: left, right
            collide = False # whether or not Tom collided with something
            for h in hits:
                if Physics.DENSITY[level.value(h)] > 0.5 or level.value(h) in 'S-' and down: # collided with solid cell
                    collide = True
                    if level.value(h) == 'N' and self.vel[Y] > 0 and h not in level.fragile.keys(): # trigger fragile cell
                        level.fragile[h] = 100
                if level.value(h) == '!': # fell off
                    self.hit = 200
                    self.vel[X] = self.vel[Y] = self.delta[X] = self.delta[Y] = accel[X] = accel[Y] = 0 # stop moving
                    point = 0 # find closest checkpoint
                    while point < len(level.checkpoints) - 1 and level.checkpoints[point+1][X] < self.pos[X]:
                        point += 1
                    checkpoint = level.checkpoints[point]
                    camera.pan(checkpoint,self.hit) # set camera to pan from current location to new location
                    self.pos[X] = checkpoint[X] # move to checkpoint
                    self.pos[Y] = checkpoint[Y]
                    
                    # stop moving
                    self.left = self.right = self.up = False
                    frame.set_mousedrag_handler(nothing)
                    frame.set_mouseclick_handler(nothing)
                    frame.set_keydown_handler(nothing)
                    Tom.HIT_SOUND.rewind()
                    Tom.HIT_SOUND.play()
                    break
                    
            if down:            
                self.ground = level.value(hits[X]) + level.value(hits[Y]) # moving down, found new ground
            if collide:
                snow = sum(Physics.DENSITY[g] for g in self.ground) < 0.25 # whether or not standing on snow
                
                if abs(self.vel[Y]) > 1: # fell fast enough for step sound
                    if snow:
                        Tom.STEP_SOUND_SNOW.rewind()
                        Tom.STEP_SOUND_SNOW.play()
                    else:
                        Tom.JUMP_SOUND.rewind()
                        Tom.JUMP_SOUND.play()
                # move to no longer collide
                if self.vel[Y] < 0:
                    self.pos[Y] = self.pos[Y] + (-side)%CELL_SIZE + .000000001
                elif not snow:
                    self.pos[Y] = self.pos[Y] - side%CELL_SIZE - .000000001
                # stop moving
                self.vel[Y] = 0
                
            else:
                for h in hits: # Tom uses item in each new cell
                    c = level.value(h)
                    if c in '.gj+BO':
                        level.items[h].activate(self)
                        if c != 'B':
                            level[h[Y]][h[X]] = ' '
                            
        if self.hit == 0: # while hit, Tom cannot be hit again
            for k in range(cell_new[LEFT], cell_new[RIGHT]+1, 1): # check every cell Tom intersects
                for j in range(cell_new[TOP], cell_new[BOTTOM]+1, 1):
                    if level[j][k] in '^v><': # Tom is hit by spikes
                        self.hit = 100
                        Tom.HIT_SOUND.rewind()
                        Tom.HIT_SOUND.play()
                        break
                if self.hit > 0: # take damage only once
                    break

        self.vel[Y] += accel[Y] / 2 # apply second half of acceleration
        self.vel[Y] *= 0.995 # adds some natural terminal velocity
    
        # after checking collisions, effective actual change
        self.delta[X] = self.pos[X]-pos[X]
        self.delta[Y] = self.pos[Y]-pos[Y]
        
        # while on ground, recharge jetpack
        if on_ground and self.jetpack_jump > 0:
            self.jetpack_jump = max(self.jetpack_jump - 5, 0)
        
        # wrap around, currently unused
        self.pos[X] %= len(level[X])*CELL_SIZE
        
        # update individual pellets
        for p in self.pellets:
            if not p.update():
                self.pellets.remove(p)
        
        # if Tom hits any enemies, apply damage
        if self.hit == 0:
            for e in active_enemies:
                if intersect_box_circle(self.boundingbox(),e.bounding_circle()):
                    self.hit = e.attack
                    Tom.HIT_SOUND.rewind()
                    Tom.HIT_SOUND.play()
                    break
                    
        # if Tom falls into lava, instant death
        if level.lavaspeed and self.pos[Y] > level.lava:
            self.health = 0
            self.FLAME_SOUND.rewind()
            self.FLAME_SOUND.play()
            return False
        
        # apply whether or not Tom is on wall
        self.wall = on_wall
        
        # Tom is still alive
        return True
    
    # move Tom to the given tile
    def set_to_tile(self, tile):
        self.pos[X] = tile[X] * CELL_SIZE + HALF_CELL_SIZE
        self.pos[Y] = tile[Y] * CELL_SIZE + CELL_SIZE
    
    # resets all of Tom's attributes, and moves him to the given position
    def reset(self, pos):
        self.pos[X] = pos[X]
        self.pos[Y] = pos[Y]
        self.frame = 0
        self.left = False
        self.right = False
        self.up = False
        self.vel = [0,0]
        self.delta = [0,0]
        self.ground = '  '
        self.gun = 0
        self.gun_max = 0
        self.arm = None
        self.pellets = []
        self.jetpack = 0
        self.jetpack_max = 0
        self.jetpack_jump = 0
        self.jetpack_jump_max = 0
        self.propel = False
        self.max_health = 500
        self.health = 500
        self.hit = 0
        self.heal = 0
        
        self.wall = 0
        
        self.direction = 0
    
    # key is pressed, Tom records it using jet and jump key configurations
    def keydown(self,key):
        if key == simplegui.KEY_MAP['a']:
            self.left = True
        elif key == simplegui.KEY_MAP['d']:
            self.right = True
        else:
            if key in self.jet_keys:
                self.up = True
            if key in self.jump_keys:
                self.jump = True
        
     
    # key is released, Tom records it using jet and jump key configurations       
    def keyup(self,key):
        if key == simplegui.KEY_MAP['a']:
            self.left = False
        elif key == simplegui.KEY_MAP['d']:
            self.right = False
        else:
            if key in self.jet_keys:
                self.up = False
            if key in self.jump_keys:
                self.jump = False
    
    # define which keys activate jump
    def set_jump(self, keys):
        self.jump_keys = keys
        
    # define which keys activate jetpack
    def set_jet(self, keys):
        self.jet_keys = keys
    
    # whether or not to disable direction key on wall jump
    def set_disable(self, d):
        self.disable = d
            
    # mouse click fires gun if applicable
    def mouseclick(self, pos):
        if not self.gun:
            return
        s = self.shoulder()
        self.arm = math.atan2(pos[Y] - s[Y],pos[X] - s[X]) # location of barrel of gun
        power = 400
        # create pellet with appropriate position and velocity
        self.pellets.append(Pellet([s[X]+camera.pos[X]+45*math.cos(self.arm-(.15 if -math.pi/2 < self.arm < math.pi/2 else -.15)),s[Y]+camera.pos[Y]+45*math.sin(self.arm-(.15 if -math.pi/2 < self.arm < math.pi/2 else -.15))],[power*math.cos(self.arm)/40 + self.delta[X],power*math.sin(self.arm)/40 + self.delta[Y]]))
        self.gun -= 1 # pellet used up
        Tom.FIRE_SOUND.rewind()
        Tom.FIRE_SOUND.play()
        if self.gun == 0: # if no more pellets, Tom de-equips gun
            self.arm = None
    
    # reposition Tom's arm to face pos
    def mousedrag(self, pos):
        if not self.gun:
            return
        s = self.shoulder()
        self.arm = math.atan2(pos[Y] - s[Y],pos[X] - s[X])
    
    # (left, right, top, bottom)
    def boundingbox(self):
        h = self.height()
        w = self.width()
        return (self.pos[X] - w/2, self.pos[X] + w/2, self.pos[Y] - h, self.pos[Y] - 1); 
    
    # Tom's height
    def height(self):
        if self.direction == 0: # facing forward
            return 81
        else: # facing side, leaned over
            return 77
        
    # Tom's width
    def width(self):
        return 42
    
    # Tom's center
    def core(self):
        return (self.pos[X], self.pos[Y] - self.height()/2)
    
    # location of Tom's feet
    def standing_feet(self):
        return ((self.pos[X]-17,self.pos[Y]),(self.pos[X]+17,self.pos[Y]))
    
    # location of Tom's shoulder
    def shoulder(self):
        if self.direction == 0:
            return (self.pos[X] - 5 - camera.pos[X],self.pos[Y] - 63 - camera.pos[Y])
        disp = (10 if self.direction<0 else -10) if self.wall and self.vel[Y] > 0 and self.ground == '  ' else (-3 if self.direction<0 else 3)
        return (self.pos[X] + disp - camera.pos[X],self.pos[Y] - 60 - camera.pos[Y])

# a menu button to be clicked on
class Button():
    
    def __init__(self, image, size, pos, trigger, attr = None, active = True):
        self.image = load_image(image) # image of the button
        self.pos = pos # position that the button will be drawn on the screen
        self.size = size # size of the button
        self.trigger = trigger # what happens when the button is clicked
        self.attr = attr # argument for the trigger
        self.active = active # whether or not the button's effect is active (so clicking it doesn't do anything)
        self.group = () # the group of buttons that this button is a member of
    
    # draws the button on the canvas
    def draw(self, canvas):
        canvas.draw_image(self.image, (self.size[X]/2, self.size[Y] * (1-int(self.active)+0.5)), self.size, self.pos, self.size)
    
    # returns True if the position is contained by the button
    def contains(self, pos):
        return pos[X] > self.pos[X] - self.size[X]/2 and pos[X] < self.pos[X] + self.size[X]/2 and pos[Y] > self.pos[Y] - self.size[Y]/2 and pos[Y] < self.pos[Y] + self.size[Y]/2
    
    # sets the group of buttons this button is in
    def set_group(self,g):
        self.group = g
    
    # activates this button, deactivating all other buttons in the group and triggering the trigger
    def activate(self):
        self.active = True
        for b in self.group:
            b.active = False
        if self.attr is None: # TODO: replace with lambda call
            self.trigger()
        else:
            self.trigger(self.attr)

tom = Tom([0,0]) # hero Tom
            
class Menu():
    
    player_name = ""
    name_input = False
    
    def draw_menu(canvas):
        canvas.draw_image(Menu.MENU_SCREEN, (400,300), (800,600), (400,300), (800,600))
        for b in Menu.buttons:
            b.draw(canvas)
        if not Menu.buttons:
            canvas.draw_text("Loading"+'.'*(time()*10)//4,(200,300),20,"black")
    
    def draw_title(canvas):
        global frame_count
        frame_count += 1
        if frame_count % 25 == 1:
            Tom.STEP_SOUND.rewind()
            Tom.STEP_SOUND.play()
        Menu.draw_menu(canvas)
        canvas.draw_image(Tom.IMAGE, (Tom.IMAGE_SIZE[X] * (frame_count//5%10 + 1.5), Tom.IMAGE_SIZE[X] * 0.5), Tom.IMAGE_SIZE, (400,320), Tom.SIZE)
        if ready:
            canvas.draw_text("Click to start!",(320,250),20,"black")
        else:
            canvas.draw_text("Loading"+"."*(frame_count//20%4),(320,250),20,"black")
    
    def draw_high_scores(canvas):
        Menu.draw_menu(canvas)
        canvas.draw_image(Menu.LEVEL_BUTTONS[Menu.level_num].image, (Menu.LEVEL_THUMBNAIL_SIZE[X]/2,Menu.LEVEL_THUMBNAIL_SIZE[Y]/2), Menu.LEVEL_THUMBNAIL_SIZE, (400,100), Menu.LEVEL_THUMBNAIL_SIZE)
        count = 0
        for score in levels[Menu.level_num].high_scores:
            canvas.draw_text(str(count+1)+". ", (300,200+50*count),15, "black")
            canvas.draw_text(str(score[0]), (350,200+50*count),15,"black")
            canvas.draw_text(score[2].replace('\n',''), (425, 200+50*count),15,"black")
            count += 1
    
    def draw_how_to_play(canvas):
        Menu.draw_menu(canvas)
        canvas.draw_image(Menu.HOW_TO_PLAY_DISPLAY, (400, 300), (800,600), (400,300), (800,600))
      
    def draw_credits(canvas):
        Menu.draw_menu(canvas)
        canvas.draw_image(Menu.CREDITS_DISPLAY, (400,300), (800,600), (400,300), (800,600))
    
    def click_menu(pos):
        for b in Menu.buttons:
            if b.contains(pos):
                b.activate()
                return
                
    def enter_main_menu():
        frame.set_draw_handler(Menu.draw_menu)
        Menu.buttons = (Menu.PLAY_GAME, Menu.HOW_TO_PLAY, Menu.CREDITS, Menu.HIGH_SCORES)
    
    def enter_level_selection_menu():
        frame.set_draw_handler(Menu.draw_menu)
        Menu.play = True
        Menu.buttons = Menu.LEVEL_BUTTONS
    
    def enter_options_menu():
        pass
        
    def enter_high_scores_menu():
        frame.set_draw_handler(Menu.draw_menu)
        Menu.play = False
        Menu.buttons = Menu.LEVEL_BUTTONS
    
    def enter_credits():
        frame.set_draw_handler(Menu.draw_credits)
        Menu.play = False
        Menu.buttons = (Menu.BACK_TO_MAIN_MENU,)
    
    def enter_how_to_play():
        frame.set_draw_handler(Menu.draw_how_to_play)
        Menu.play = False
        Menu.buttons = Menu.OPTION_BUTTONS
        
    def select_level(num):
        Menu.level_num = num
        if Menu.play:
            Menu.buttons = ()
            global frame_count, level, score, disp_score
            frame_count = 0
            level = Level(levels[num])
            score = 0
            disp_score = 0
            timer.start()
            tom.reset(level.tom_start)
            frame.set_draw_handler(draw_midgame)
            frame.set_keydown_handler(tom.keydown)
            frame.set_keyup_handler(tom.keyup)
            frame.set_mouseclick_handler(tom.mouseclick)
            frame.set_mousedrag_handler(tom.mousedrag)
        else:
            Menu.buttons = [Menu.BACK_TO_HIGH_SCORES]
            frame.set_draw_handler(Menu.draw_high_scores)
    
    def level_complete(arg):
        high_scores = levels[Menu.level_num].high_scores
        high_scores.append((score, -time(), str(Menu.player_name)))
        Menu.player_name = ""
        high_scores.sort()
        high_scores.reverse()
        if len(high_scores) > 8:
            high_scores.pop(8)
        Menu.buttons = [Menu.BACK_TO_MAIN_MENU]
        frame.set_draw_handler(Menu.draw_high_scores)
        frame.set_mouseclick_handler(Menu.click_menu)
    
    def type_name(key):
        if key >= 0 and key < 256:
            if key == 8:
                if len(Menu.player_name) > 0:
                    Menu.player_name = Menu.player_name[0:-1]
            elif key == 13:
                Menu.player_name += '\n'
            elif len(Menu.player_name) < 10:
                Menu.player_name += chr(key)
    
    TITLE_SCREEN = Button("Title_Screen.png", (800,600), (400,300), enter_main_menu)
    
    MENU_SCREEN = load_image("Menu_Screen.png")
    
    PLAY_GAME = Button("PlayGame.png", (400,200), (400,200), enter_level_selection_menu)
    HIGH_SCORES = Button("HighScores.png", (150,150), (650,475), enter_high_scores_menu)
    HOW_TO_PLAY = Button("HowToPlay.png", (150,150), (150,475), enter_how_to_play)
    CREDITS = Button("Credits.png", (150,150), (400,475), enter_credits)
    
    JUMP_W = Button("W_Option.png", (14,18), (372,406), tom.set_jump, (87,), False)
    JUMP_SPACE = Button("Spacebar_Option.png", (84,22), (517,408), tom.set_jump, (32,), False)
    JUMP_EITHER = Button("Either_Option.png", (64,19), (667,405), tom.set_jump, (32,87), True)
    
    JUMP_W.set_group((JUMP_SPACE,JUMP_EITHER))
    JUMP_SPACE.set_group((JUMP_W, JUMP_EITHER))
    JUMP_EITHER.set_group((JUMP_W, JUMP_SPACE))
    
    JET_W = Button("W_Option.png", (14,18), (372,446), tom.set_jet, (87,), False)
    JET_SPACE = Button("Spacebar_Option.png", (84,22), (517,448), tom.set_jet, (32,), False)
    JET_EITHER = Button("Either_Option.png", (64,19), (667,445), tom.set_jet, (32,87), True)
    
    JET_W.set_group((JET_SPACE,JET_EITHER))
    JET_SPACE.set_group((JET_W, JET_EITHER))
    JET_EITHER.set_group((JET_W, JET_SPACE))
    
    DISABLE_YES = Button("Yes_Option.png", (34,18), (549,566), tom.set_disable, True, True)
    DISABLE_NO = Button("No_Option.png", (24,18), (637,566), tom.set_disable, False, False)
    
    DISABLE_YES.set_group((DISABLE_NO,))
    DISABLE_NO.set_group((DISABLE_YES,))
    
    BACK_TO_MAIN_MENU = Button("Back.png", (50,50), (25, 575), enter_main_menu)
    BACK_TO_HIGH_SCORES = Button("Back.png", (50,50), (25, 575), enter_high_scores_menu)
    
    HOW_TO_PLAY_DISPLAY = load_image("How to Play.png")
    CREDITS_DISPLAY = load_image("Credits Display.png")
    
    OPTION_BUTTONS = (JUMP_W,JUMP_SPACE, JUMP_EITHER, JET_W, JET_SPACE, JET_EITHER, DISABLE_YES, DISABLE_NO, BACK_TO_MAIN_MENU)
    
    buttons = [TITLE_SCREEN]
    
    LEVEL_ARRAY = ['X X',' X ','X X']
    LEVEL_THUMBNAIL_SIZE = (160, 120)
    LEVEL_THUMBNAIL_DISP = (800/(len(LEVEL_ARRAY[0])+1),600/(len(LEVEL_ARRAY)+1))
    
    LEVEL_BUTTONS = []
    
    play = False
    level_num = -1
    
    count = 0
    for y in range(len(LEVEL_ARRAY)):
        for x in range(len(LEVEL_ARRAY[y])):
            if LEVEL_ARRAY[y][x] != ' ':
                LEVEL_BUTTONS.append(Button("Level"+str(count+1)+"Thumbnail.png", LEVEL_THUMBNAIL_SIZE, (LEVEL_THUMBNAIL_DISP[X]*(x+1), LEVEL_THUMBNAIL_DISP[Y]*(y+1)), select_level, count))
                count += 1
    
    LEVEL_BUTTONS.append(BACK_TO_MAIN_MENU)

# the distance between two points
def dist(p1,p2):
    return math.sqrt((p1[X]-p2[X])**2+(p1[Y]-p2[Y])**2)

# the square of the distance between two points
def norm(p1,p2):
    return (p1[X]-p2[X])**2+(p1[Y]-p2[Y])**2

# returns True if the two bounding boxes intersect
def intersect_boxes(b1, b2): # (left, right, top, bottom)
    return b1[LEFT] <= b2[RIGHT] and b1[RIGHT] >= b2[LEFT] and b1[TOP] <= b2[BOTTOM] and b1[BOTTOM] >= b2[TOP]

# returns True if the given bounding box and circle intersect
def intersect_box_circle(rect, circle): # (left, right, top, bottom), (center, radius)
    
    rec_center = [(rect[LEFT]+rect[RIGHT])/2, (rect[TOP]+rect[BOTTOM])/2]
    w = (rect[RIGHT]-rect[LEFT])/2
    h = (rect[BOTTOM]-rect[TOP])/2
    dx = abs(circle[0][X] - rec_center[X])
    dy = abs(circle[0][Y] - rec_center[Y])
    if (dx > circle[1] + w or dy > circle[1] + h):
        return False
    circ_dist = [abs(circle[0][X] - rect[LEFT] - w), abs(circle[0][Y] - rect[TOP] - h)]
    if (circ_dist[X] <= w or circ_dist[Y] <= h):
        return True
    corner_dist = (circ_dist[X] - w)**2 + (circ_dist[Y] - h) ** 2
    return corner_dist <= circle[1]**2
    
# converts a bounding box to the four points that make it up
def box_to_polygon(b):
    return ((b[LEFT],b[TOP]),(b[LEFT],b[BOTTOM]),(b[RIGHT],b[TOP]),(b[RIGHT],b[BOTTOM]))

# returns true if the distance between p1 and p2 is less than the given (squared) distance
def within(p1, p2, dist_2):
    return (p1[X] - p2[X]) ** 2 + (p1[Y] - p2[Y]) ** 2 < dist_2
    
# returns all cells with which the given circle intersects
def circle_grid_hits(pos, radius, grid_size = CELL_SIZE):
    hits = set()
    
    r_2 = radius ** 2
    
    p = list(pos)
    p[Y] += radius
    hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
    p[X] = p[X] // grid_size * grid_size + grid_size
    p[Y] = p[Y] // grid_size * grid_size
    while p[Y] + grid_size > pos[Y]:
        if (within(pos,p,r_2)):
            hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
            p[X] += grid_size
        else:
            p[Y] -= grid_size
            p[X] -= grid_size
            
    p = list(pos)
    p[X] += radius
    hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
    p[X] = p[X] // grid_size * grid_size
    p[Y] = p[Y] // grid_size * grid_size - 1
    while p[X] + grid_size > pos[X]:
        if (within(pos,p,r_2)):
            hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
            p[Y] -= grid_size
        else:
            p[Y] += grid_size
            p[X] -= grid_size
            
    p = list(pos)
    p[Y] -= radius
    hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
    p[X] = p[X] // grid_size * grid_size - 1
    p[Y] = p[Y] // grid_size * grid_size + grid_size - 1
    while p[Y] - grid_size < pos[Y]:
        if (within(pos,p,r_2)):
            hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
            p[X] -= grid_size
        else:
            p[Y] += grid_size
            p[X] += grid_size
        
    p = list(pos)
    p[X] -= radius
    hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
    p[X] = p[X] // grid_size * grid_size + grid_size - 1
    p[Y] = p[Y] // grid_size * grid_size + grid_size
    while p[X] - grid_size < pos[X]:
        if (within(pos,p,r_2)):
            hits.add((int(p[X]//grid_size),int(p[Y]//grid_size)))
            p[Y] += grid_size
        else:
            p[Y] -= grid_size
            p[X] += grid_size
            
    return hits

score = 0 # current score
disp_score = 0 # current score as currently displayed

# the actual level itself
class Level():

    TILE_IMAGE = load_image("Tiles.png") # all of the tiles that can be drawn
    TILE_SIZE = 50
    tile_keys = 'gj+BbOZ@-^v><SI' # tiles by drawn order in TILE_IMAGE 
    
    tiles = dict() # maps tile keys to their positions on TILE_IMAGE
    k = 0
    for t in tile_keys:
        tiles[t] = [TILE_SIZE/2 + TILE_SIZE * k, TILE_SIZE/2]
        k += 1
    
    snow_tile = (TILE_SIZE/2,TILE_SIZE*5/2) # drawing over a tile with snow
    
    TICK_SOUND = load_sound("tick.mp3") # http://www.freesound.org/people/KorgMS2000B/sounds/54405/ # ticking for the temporary blocks
    COMPLETE_SOUND = load_sound("complete.mp3") # http://www.freesound.org/people/sagetyrtle/sounds/32260/ # on completion
    
    # creates the level from the given level information
    def __init__(self, level_info):
        
        self.level_info = level_info
        self.grid = list(level_info.grid) # copies the level grid
        for k in range(len(self.grid)):
            self.grid[k] = list(self.grid[k]) # turns strings into lists to be modified
        empty = ' '*len(self.grid[0])
        for k in range(12):
            self.grid.insert(0,list(empty)) # add 12 rows of emptiness to the top of the level
        for k in range(2):
            self.grid.append(list(self.grid[-1])) # copy the final row and reappend it
        for k in range(len(self.grid)):
            self.grid[k] = list(self.grid[k]) # copy the lists yet again, might not be necessary?
        
        self.colors = list(level_info.colors) # the colors of this level for X and Y blocks
        
        self.items = dict() # the items in this level, keyed by position
        
        self.enemies = set() # the enemies in this level
        
        self.checkpoints = list() # the checkpoints in this level for falling off
        
		self.boss = None # by default, level doesn't have a boss
		
        count = dict() # counting each cell type to assign attributes in turn
        for k in level_info.attr.keys():
            count[k] = 0
    
        
        # gets the next attribute for a particular cell type
        def next_attr(c):
            attr = level_info.attr[c][count[c]]
            count[c] += 1
            return attr
    
        # loop over every cell to determine what it is
        for k in range(len(self.grid[0])):
            for j in range(len(self.grid)):
                if self.grid[j][k] == 't': # Tom's starting position
                    self.tom_start = [k*CELL_SIZE+HALF_CELL_SIZE,(j+1)*CELL_SIZE]
                    self.checkpoints.append(self.tom_start)
                    self.grid[j][k] = ' '
                elif self.grid[j][k] == 'r': # checkpoint
                    self.checkpoints.append([k*CELL_SIZE+HALF_CELL_SIZE,(j+1)*CELL_SIZE])
                    self.grid[j][k] = ' '
                elif self.grid[j][k] == 'm': # Mook
                    self.enemies.add(Mook([k*CELL_SIZE+HALF_CELL_SIZE,(j)*CELL_SIZE+HALF_CELL_SIZE]))
                    self.grid[j][k] = ' '
                elif self.grid[j][k] == 'M': # King Mook
					king_mook = KingMook([k*CELL_SIZE+HALF_CELL_SIZE,j*CELL_SIZE+HALF_CELL_SIZE])
                    self.enemies.add(king_mook)
					self.boss = king_mook
                    self.grid[j][k] = ' '
                elif self.grid[j][k] == 'f': # Frog
                    self.enemies.add(Frog([k*CELL_SIZE+HALF_CELL_SIZE,j*CELL_SIZE], next_attr('f')))
                    self.grid[j][k] = ' '
                elif self.grid[j][k] == 'g': # gun
                    self.items[(k,j)] = (Item(Item.obtain_gun, next_attr('g')))
                elif self.grid[j][k] == 'j': # jetpack
                    self.items[(k,j)] = (Item(Item.obtain_jetpack, next_attr('j')))
                elif self.grid[j][k] == '+': # health
                    self.items[(k,j)] = (Item(Item.heal, next_attr('+')))
                elif self.grid[j][k] == '.': # coin
                    self.items[(k,j)] = Item(Item.collect, None)
                elif self.grid[j][k] == 'O': # CD (unused)
                    self.items[(k,j)] = (Item(Item.play, next_attr('O')))
                elif self.grid[j][k] == 'B': # temporary block switch
                    self.items[(k,j)] = Item(Item.blue, next_attr('B'))
        
        self.background = list()
        for j in range(len(self.grid)):
            self.background.append(None) # completely empty background
        
        cur_background = None # color of the background (initially nothing)
            
        # loop over every cell to determine the background
        for j in range(len(self.grid)):
            for k in range(len(self.grid[0])):
                if self.grid[j][k] == 'K': # makes background black
                    self.grid[j][k] = ' '
                    cur_background = 'black'
                elif self.grid[j][k] == 'R': # makes background red
                    self.grid[j][k] = ' '
                    cur_background = '#600000'
                
                self.background[j] = cur_background
                
#        for row in self.background:
#            print row
                
        # keeps track of fragility of fragile (N) cells
        self.fragile = dict()
    
        # time left on temporary blue blocks
        self.blue = 0
    
        # sets the lava speed and position
        if level_info.lavaspeed:
            self.lavaspeed = level_info.lavaspeed
            self.lava = len(self.grid)*CELL_SIZE
        else:
            self.lavaspeed = None
        
        # sets the wrap (whether or not things can wrap around)
        self.wrap = level_info.wrap
    
    # updates the level frame by frame
    def update(self):
        
        # all fragile cells become more fragile, disappear when done
        for k in self.fragile.keys():
            self.fragile[k] -= 1
            if self.fragile[k] == 0:
                del self.fragile[k]
                self.grid[k[Y]][k[X]] = ' '
        
        # temporary blocks are active
        if self.blue: # deduct one frame
            self.blue -= 1
            if self.blue < 200: # more than 200 frames left
                if self.blue == 0: # blocks are finished
                    Level.tiles['b'][Y] = 25 # switch tile image back to transparent
                    Level.tiles['B'][Y] = 25 # switch switch image back to off
                    Physics.FRICTION['b'] = Physics.FRICTION[' '] # effectively air
                    Physics.DENSITY['b'] = 0
                elif self.blue % 10 == 0: # ticking noise every ten frames
                    Level.TICK_SOUND.rewind()
                    Level.TICK_SOUND.play()
                    if self.blue % 20 == 0:
                        Level.tiles['b'][Y] = 25 # flash out
                    else:
                        Level.tiles['b'][Y] = 75 # flash in
            elif self.blue % 20 == 0: # ticking noise starts out every 20 frames
                self.TICK_SOUND.rewind()
                self.TICK_SOUND.play()
        if self.lavaspeed: # lava climbs higher
            self.lava -= self.lavaspeed
         
    def __getitem__(self, p):
        return self.grid[p]
             
    def __len__(self):
        return len(self.grid)
    
    # draws the level on the canvas, using the camera as reference
    def draw(self, canvas, camera):
        if camera.pos[Y] >= 0: # a negative camera shows only an empty sky
            x_major = camera.pos[X] // CELL_SIZE # calculate axes
            x_minor = camera.pos[X]%CELL_SIZE-HALF_CELL_SIZE
            y_major = camera.pos[Y] // CELL_SIZE
            y_minor = camera.pos[Y]%CELL_SIZE-HALF_CELL_SIZE
            for j in range(int(math.ceil(float(CANVAS_SIZE[Y])/CELL_SIZE)) + int(y_minor != HALF_CELL_SIZE)): # all rows to be drawn
                if j + y_major >= len(self.grid):
                    break
                if self.background[j+y_major]: # if background should be drawn
                    canvas.draw_line((0, j*CELL_SIZE-y_minor), (800, j*CELL_SIZE-y_minor), CELL_SIZE, self.background[j+y_major]) # draw it
                k = 0
                max_k = int(math.ceil(float(CANVAS_SIZE[X])/CELL_SIZE)) + int(x_major != HALF_CELL_SIZE)
                while max_k + x_major > len(self.grid[0]):
                    max_k -= 1
                while k < max_k: # all columns to be drawn
                    char = self[j+y_major][k+x_major] # this cell
                    if char == ' ': # skip emptiness
                        k += 1
                        continue
                    # draw a tile of a particular solid color
                    if char in 'XY@':
                        # choose the color
                        if char == 'X':
                            color = self.colors[X]
                        elif char == 'Y':
                            color = self.colors[Y]
                        else:
                            color = '#FFD700'
                        # identify all following tiles of the same color
                        end = k
                        while end + 1 < max_k and self[j+y_major][end+x_major+1] == char:
                            end += 1
                        # draw one solid line through all of them
                        canvas.draw_line((k*CELL_SIZE-x_minor-HALF_CELL_SIZE,j*CELL_SIZE-y_minor),(end*CELL_SIZE-x_minor+HALF_CELL_SIZE,j*CELL_SIZE-y_minor),CELL_SIZE,color)
                        k = end # skip tiles drawn with the line
                    # draw a tile that uses an image from the image sprite
                    else:
                        if char == '.':
                            sprite_pos = (Level.TILE_SIZE/2 + Level.TILE_SIZE * (frame_count//10 % 20), 175)
                        elif char in Level.tile_keys:
                            sprite_pos = Level.tiles[char]
                        elif char == 'N':
                            x = k+x_major
                            y = j+y_major
                            if (x,y) in self.fragile.keys():
                                sprite_pos = (Level.TILE_SIZE/2 + (128-self.fragile[(x,y)])//6 * Level.TILE_SIZE, 225)
                            else:
                                sprite_pos = (Level.TILE_SIZE, 225)
                        else:
                            sprite_pos = None
                        if sprite_pos:
                            canvas.draw_image(Level.TILE_IMAGE, sprite_pos, (Level.TILE_SIZE,Level.TILE_SIZE), (k*CELL_SIZE-x_minor,j*CELL_SIZE-y_minor),(CELL_SIZE,CELL_SIZE))
                    k += 1
                j += 1
        else: # draw sky darker as it goes higher
            hue = max(255+camera.pos[Y]//64,25)
            frame.set_canvas_background(color(0,hue,hue))
    
    # draws snow over Tom where he is in snow
    def draw_over_snow(self, canvas, camera, snow_char):
        if camera.pos[Y] >= 0: 
            cells = [int(p//CELL_SIZE) for p in tom.boundingbox()] # identify where Tom is
            x_major = camera.pos[X] // CELL_SIZE
            x_minor = camera.pos[X]%CELL_SIZE-HALF_CELL_SIZE
            y_major = camera.pos[Y] // CELL_SIZE
            y_minor = camera.pos[Y]%CELL_SIZE-HALF_CELL_SIZE
            for k in range(max(0,cells[X]-1),min(len(self.grid[0]),cells[Y]+2)):
                for j in range(max(0,cells[2]-1),min(len(self.grid),cells[3]+2)): # for each cell in the bounding box
                    char = self[j][k]
                    if char == 'S' or char == snow_char: # if it is snow, draw more snow
                        canvas.draw_image(Level.TILE_IMAGE,Level.snow_tile,(CELL_SIZE,CELL_SIZE),(k*CELL_SIZE-x_major*CELL_SIZE-x_minor,j*CELL_SIZE-y_major*CELL_SIZE-y_minor),(CELL_SIZE,CELL_SIZE))
    
    # draw the rising lava
    def draw_over_lava(self, canvas, camera):
        lava_line = self.lava - camera.pos[Y]
        if lava_line < 600:
            canvas.draw_polygon(((0,lava_line),(800,lava_line),(800,600),(0,600)),1,"#E00000","#E00000")
    
    # returns the cell value at the given position
    def value(self, p):
        if p[X] < 0 or p[X] >= len(self[0]):
            if self.wrap:
                if p[Y] >= 0 and p[Y] < len(self.grid):
                    return self[p[Y]][p[X]%800]
            else:
                return 'X'    
        if p[Y] < 0:
            return ' '
        if p[Y] >= len(self.grid):
            return '!'                  
        return self[p[Y]][p[X]]
    
    # returns the cell index for the given position
    def pos(self,p):
        return (p[X]//CELL_SIZE,p[Y]//CELL_SIZE)
        

def draw_square(canvas, x, y, color):
    canvas.draw_line((x, y-HALF_CELL_SIZE), (x, y+HALF_CELL_SIZE), CELL_SIZE, color)
        
# ensures that the correct part of the level is drawn at any given time
class Camera():
    
    def __init__(self, track):
        self.pos = [0,0] # the top left corner of the camera
        self.track = track # the position that the camera follows
        self.approach = None # the position that the camera approaches, if any
        self.length = 0 # the number of frames until the camera finishes its approach
        self.progress = 0 # progress in the camera's approach
        self.shaked = 0 # how shaken up the camera is (earthquake effect)
    
    # apply a shaking effect to the camera
    def shake(self, s):
        if self.shaked > 0: # add slighly more shaking
            self.shaked += math.sqrt(abs(s))
        else: # commence shaking
            self.shaked -= abs(s)
        pass

    # update the camera frame by frame to continue tracking or approaching
    def update(self):
        if (self.shaked): # shaking
            self.pos[X] += math.sqrt(abs(self.shaked)) * (1 if self.shaked > 0 else -1) # shift by shake
            self.shaked *= -0.97 # shake diminishes over time
            if abs(self.shaked) < 0.01:
                self.shaked = 0
        if self.approach: # approaching a fixed point
            self.progress += 1 # one more frame of progress
            d = 1/self.length # proportion of distance to travel per frame
            self.pos[X] += self.approach[X] * d # travel that distance in both axes
            self.pos[Y] += self.approach[Y] * d
            if self.progress == self.length: # if done approaching
                self.approach = None # stop approaching
                self.length = 0
                self.progress = 0
                frame.set_keydown_handler(tom.keydown) # Tom may move again
                frame.set_mousedrag_handler(tom.mousedrag)
                frame.set_mouseclick_handler(tom.mouseclick)
        else: # normal camera behavior
            if self.track[X] > self.pos[X] + 500: # follow right
                self.pos[X] = int(self.track[X]) - 500
            if self.track[X] < self.pos[X] + 300: # follow left
                self.pos[X] = int(self.track[X]) - 300
            if self.track[Y] > self.pos[Y] + 400: # follow top
                self.pos[Y] = int(self.track[Y]) - 400
            if self.track[Y] < self.pos[Y] + 200: # follow bottom
                self.pos[Y] = int(self.track[Y]) - 200
        if self.pos[X] < 0: # can't go out of bounds (except up)
            self.pos[X] = 0
        if self.pos[X] > len(level[X])*CELL_SIZE-800:
            self.pos[X] = len(level[X])*CELL_SIZE-800
        if self.pos[Y] > len(level.grid)*CELL_SIZE-700:
            self.pos[Y] = len(level.grid)*CELL_SIZE-700	
     
    # adjusts the given position to be relative to this camera
    def adjust(self,pos):
        return (pos[X]-self.pos[X],pos[Y]-self.pos[Y])
    
    # adjusts the given position relative to the camera to be an absolute position
    def deadjust(self,pos):
        return (pos[X]+self.pos[X],pos[Y]+self.pos[Y])

    # set the camera to approach centering on the given point over t frames
    def pan(self,p2,t):
        p2 = [p2[X] - 400, p2[Y] - 300] # shift point from center to top left
        if p2[X] < 50: # can't go too far left
            p2[X] = 50
        if p2[X] > len(level[X])*50-850: # or right
            p2[X] = len(level[X])*50-850
        if p2[Y] > len(level.grid)*50-750: # or down
            p2[Y] = len(level.grid)*50-750
        self.approach = (p2[X]-self.pos[X],p2[Y]-self.pos[Y]) # approach it
        self.length = t # over t frames
        
    def __getitem__(self,key):
        return self.pos[key]
        
class Physics():
    GRAVITY = 0.1 # force of gravity
    
    FRICTION = dict() # the friction of a given tile when Tom stands on it
    for t in 'XYZ@N- S':
        FRICTION[t] = 1
    FRICTION['I'] = 0.1
    for t in ' .gj+!?^v><BbOS':
        FRICTION[t] = 0.08

    DENSITY = dict() # the density of a tile, determines what happens when Tom attempts to pass through it
    for t in 'XYZ@NI':
        DENSITY[t] = 1
    DENSITY['S'] = 0.1
    DENSITY['-'] = 0.3
    for t in ' .gj+!?^v><BbO':
        DENSITY[t] = 0
        
        
# any of the items Tom may pick up
class Item():
    
    GUN_IMAGE = load_image("Gun.png")
    JETPACK_IMAGE = load_image("Jetpack.png")
    PELLET_IMAGE = load_image("Pellets.png")
    HEALTH_IMAGE = load_image("Health.png")
    COLLECTIBLE_IMAGE = load_image("Collectible.png")
    BLUE_BLOCK = load_image("BlueBlock.png")
    
    GUN_GET = load_sound("cockgun-02.wav") # http://www.mediacollege.com/downloads/sound-effects/weapons/cockgun-02.wav
    JETPACK_GET = load_sound("jet-start-02.wav") # http://www.mediacollege.com/downloads/sound-effects/planes/jet-start-02.wav
    COIN_GET = load_sound("coin-04.wav") # http://www.mediacollege.com/downloads/sound-effects/money/coin-04.wav
    COIN_GET.set_volume(0.4)
    HEAL_GET = simplegui.load_sound("http://www.freesound.org/data/previews/51/51713_113976-lq.mp3") # http://www.freesound.org/people/BristolStories/sounds/51713/
    
    # creates an item that performs the given action upon being obtained, with attr as arguments
    def __init__(self, action, attr = ()):
        self.action = action
        self.attr = attr
    
    # called when Tom obtains the item
    def activate(self, tom):
        self.action(tom, self.attr)
    
    # Tom gets a gun
    def obtain_gun(tom, attr):
        tom.gun += attr[0] # gains bullets
        if attr[1] > tom.gun_max: # may increase max bullet count
            tom.gun_max = attr[1]
        if tom.gun > tom.gun_max: # count cannot exceed maximum
            tom.gun = tom.gun_max
        Item.GUN_GET.rewind() # gun sound
        Item.GUN_GET.play()
    
    # Tom gets a jetpack
    def obtain_jetpack(tom, attr):
        tom.jetpack += attr[0] # gains fuel
        if attr[1] > tom.jetpack_max: # may increase max fuel
            tom.jetpack_max = attr[1]
        if attr[2] > tom.jetpack_jump_max: # may increase jump maximum
            tom.jetpack_jump_max = attr[2]
        if tom.jetpack > tom.jetpack_max: # cannot have more fuel than maximum
            tom.jetpack = tom.jetpack_max
        Item.JETPACK_GET.rewind() # jetpack sound
        Item.JETPACK_GET.play() 
    
    # Tom gets a health boost
    def heal(tom, attr):
        tom.heal += attr # heals
        Item.HEAL_GET.rewind()
        Item.HEAL_GET.play()
    
    # Tom gets a coin, general benefits
    def collect(tom, attr):
        global score
        tom.heal += 25 # heal 25 health
        tom.jetpack += 25 # gain 25 fuel 
        if tom.jetpack > tom.jetpack_max:
            tom.jetpack = tom.jetpack_max
        tom.gun += 1 # gain 1 bullet
        if tom.gun > tom.gun_max:
            tom.gun = tom.gun_max
        score += 25 # gain 25 points
        Item.COIN_GET.rewind()
        Item.COIN_GET.play()

    # Tom hits blue switch, activates blue blocks
    def blue(tom, attr):
        if not level.blue: # unless switch currently pressed
            level.blue = attr # set attr frames of blue blocks
            Level.tiles['b'][Y] = 75 # blue blocks now appear solid
            Level.tiles['B'][Y] = 75 # blue switch now appears pressed
            Physics.FRICTION['b'] = 1 # blue block is in effect a block
            Physics.DENSITY['b'] = 1
    
    # Tom obtains a CD, it plays
    def play(tom, sound):
        sound.play() # play the music

# basic circular enemy
class Mook():
    IMAGE_SIZE = (50,50)
    DRAW_SIZE = (50,50)
    SIZE = 42
    IMAGE = load_image("Mook.png")
    TERMINAL = 20
    POP_SOUND = load_sound("pop.mp3") # http://www.freesound.org/people/HerbertBoland/sounds/33369/
    
    def __init__(self, pos):
        self.pos = pos # position of the Mook, bottom center
        self.vel = [-4,0] # initial velocity, rolling left
        self.angle = 0 # angle for rolling (initially upright, facing left)
        self.ground = True # whether or not the Mook is on the ground
        self.health = 100 # health to be deducted before death
        self.attack = 100 # damage that would be dealt to Tom upon contact
        self.points = 100 # points Tom would gain upon defeating a Mook
        self.defense = 0 # negation to damage
        self.image_size = Mook.IMAGE_SIZE # size of the image as it is stored
        self.draw_size = Mook.DRAW_SIZE # size of the image as it is drawn
        self.size = Mook.SIZE # diameter
        self.image = Mook.IMAGE # image of the Mook
        self.terminal = Mook.TERMINAL # terminal velocity, either direction
     
    # draws the Mook on the canvas
    def draw(self, canvas, camera):
        canvas.draw_image(self.image, (self.image_size[X] * 0.5, self.image_size[Y] * 0.5), self.image_size, (self.pos[X]-camera.pos[X],self.pos[Y] - self.size/2 - camera.pos[Y]), self.draw_size, self.angle/float(self.size/2))
    
    # updates the Mook frame by frame, returning True only if the Mook is still alive
    def update(self):
        if self.health <= 0: # not still alive
            return False
        x0 = self.pos[X] # initial x
        self.pos[X] += self.vel[X] # move in the X direction
        self.pos[Y] += self.vel[Y] + Physics.GRAVITY / 2 # move in the Y direction
        hits = circle_grid_hits(self.center(), self.size / 2) # the grid cells that the Mook came into contact with
        for hit in hits: # for each one
            c = level.value(hit)
            if Physics.DENSITY[c] > 0: # if it's a solid
                dx, dy = get_angle(hit, self.center()) # get the angle to that cell
                if dx == 0: # vertical
                    if dy > 0: # below
                        self.pos[Y] += (dy - self.size / 2) # move up
                    else: # below
                        self.pos[Y] -= (dy + self.size / 2) # move down
                    if abs(self.vel[Y]) <= Physics.GRAVITY: # stop if moving weaker than gravity
                        self.vel[Y] = 0
                    camera.shake(self.vel[Y] ** 2 * self.size ** 3 / 1000000) # sufficiently large Mooks can shake the camera
                    self.vel[Y]  *= -0.8 # slow down over time
                elif dy == 0: # horizontal
                    if dx > 0: # to the right
                        self.pos[X] += (dx - self.size / 2) # move left
                    else: # to the left
                        self.pos[X] -= (dx + self.size / 2) # move right
                    self.vel[X] *= -0.8 # slow down over time
                else: # at an angle
                    # total = (dx ** 2 + dy ** 2) # just a guess to what direction to go next, and at what speed
                    # self.vel[X] -= dx * 50 / total
                    # self.vel[Y] -= dy * 50 / total
                    
        self.angle += (self.pos[X]-x0) # rotates as it moves horizontally, proportional to effective displacement
        
        if self.vel[Y] == 0: # didn't move vertically
            if self.vel[X] > 0: # moved to right
                if self.vel[X] < 1: # but not too fast
                    self.vel[X] += 0.01 # speed up slightly
            else: # moved to left
                if self.vel[X] > -1: # but not too fast
                    self.vel[X] -= 0.01 # speed up slightly
        
        self.vel[Y] += Physics.GRAVITY # apply gravity to velocity
        if self.vel[Y] > Mook.TERMINAL: # capped by terminal velocity
            self.vel[Y] = Mook.TERMINAL
        
        
        self.pos[X] %= len(level[X])*CELL_SIZE # loop around
        self.pos[Y] %= len(level.grid)*CELL_SIZE
        
        return True # Mook is still alive
        
    # moves the Mook to the given tile
    def set_to_tile(self, tile):
        self.pos[X] = tile[X] * CELL_SIZE + HALF_CELL_SIZE
        self.pos[Y] = tile[Y] * CELL_SIZE + CELL_SIZE
        
    # whether or not the Mook si currently on screen
    def on_screen(self):
        return self.pos[X]+self.size/2 > camera.pos[X] and self.pos[X] - self.size/2 < camera.pos[X] + 800 and self.pos[Y] > camera.pos[Y] and self.pos[Y]-self.size < camera.pos[Y] + 600

    # the center of the Mook
    def center(self):
        return (self.pos[X], self.pos[Y] - self.size/2)
    
    # the circle that bounds the Mook (center, radius)
    def bounding_circle(self):
        return ([self.pos[X],self.pos[Y]-self.size/2], self.size/2)
    
    # the box that bounds the mook (left, right, top, bottom)
    def boundingbox(self):
        return (self.pos[X]-self.size,self.pos[X]+self.size/2,self.pos[Y]-self.size,self.pos[Y])

    # deals damage to the Mook
    def hit(self, damage):
        self.health -= max(damage - self.defense, 0)

# a much larger Mook
class KingMook(Mook):
    IMAGE_SIZE = Mook.IMAGE_SIZE
    DRAW_SIZE = (290,290)
    SIZE = 290 * 21/25
    IMAGE = Mook.IMAGE
    
    def __init__(self, pos):
        Mook.__init__(self, pos)
        self.image_size = KingMook.IMAGE_SIZE
        self.draw_size = KingMook.DRAW_SIZE
        self.size = KingMook.SIZE
        self.image = KingMook.IMAGE
        self.points = 1000
        self.health = 1000
        
# calculates the angle between the given cell and the given position, relative to the horizontal
def get_angle(square, pos):
    dx = dy = 0
    other_pos = [square[X] * CELL_SIZE, square[Y] * CELL_SIZE]
    if (other_pos[X] // CELL_SIZE != pos[X] // CELL_SIZE):
        dx = other_pos[X] - pos[X]
        if (other_pos[X] < pos[X]):
            dx += CELL_SIZE
    if (other_pos[Y] // CELL_SIZE != pos[Y] // CELL_SIZE):
        dy = other_pos[Y] - pos[Y]
        if (other_pos[Y] < pos[Y]):
            dy += CELL_SIZE
    return dx, dy
    
# an enemy that moves around on the fourth wall
class Frog():
    IMAGE_SIZE = (200,200)
    SIZE = (60,60)
    IMAGE = load_image("Frog.png")
    
    # creates a Frog at the given position and whether or not it seeks Tom
    def __init__(self, pos, seeking):
        self.pos = pos # position
        self.angle = 3 * math.pi / 2 # angle relative to horizontal
        self.target = self.angle # target angle to be at
        self.jump = 1 # frames in current jump
        self.speed = 5 # jump speed 
        self.rspeed = math.pi/30 # rotation speed
        self.jump_distance = 150 # distance per jump
        self.wait = 0 # frames until current jump
        self.seeking = seeking # position to follow, if any
        self.attack = 150 # damage it can deal
        self.health = 300 if seeking else 200 # higher if it is a seeking Frog
        if self.seeking: # tracks Tom
            self.tom = tom
            self.points = 300
        else: # moves within a restricted circle
            self.startpos = [pos[X],pos[Y]]
            self.radius = 200
            self.points = 200
        
    # draws the frog on the canvas
    def draw(self, canvas, camera):
        canvas.draw_image(Frog.IMAGE, (Frog.IMAGE_SIZE[X] * 0.5, Frog.IMAGE_SIZE[Y] * (int(self.seeking) + 0.5)), Frog.IMAGE_SIZE, (self.pos[X]-camera.pos[X],self.pos[Y] - camera.pos[Y]), Frog.SIZE, self.angle)

    # updates the frog frame by frame, returning True only of the Frog is still alive
    def update(self):
        if self.health <= 0: # dead, so False
            return False
        if self.wait: # wait before jumping
            self.wait -= 1
        elif self.jump: # in mid-jump
            self.pos[X] += self.speed * math.cos(self.angle) # move through jump
            self.pos[Y] += self.speed * math.sin(self.angle)
            self.jump -= 1 # one frame of jumping complete
            if self.jump == 0:
                self.wait = 30 # wait 30 frames to rotate
                if self.seeking: # target angle to attack Tom
                    dx = tom.pos[X] - self.pos[X]
                    dy = tom.pos[Y] - self.pos[Y]
                    self.target = math.atan2(dy,dx)
                else: # choose random angle within circle of freedom
                    dx = self.startpos[X] - self.pos[X]
                    dy = self.startpos[Y] - self.pos[Y]
                    theta = math.atan2(dy,dx)
                    dist = math.sqrt(dx**2 + dy**2)
                    numerator = dist**2 + self.jump_distance**2 - self.radius**2
                    denominator = 2 * dist * self.jump_distance
                    if dist > 0 and abs(numerator) < denominator:
                        a_range = math.acos(numerator / denominator)
                    else:
                        a_range = math.pi
                    r = random.random()
                    delta = r * a_range
                    self.target = theta + delta
                if self.target > self.angle: # correct angle to be within (-pi, pi)
                    while self.target > self.angle + math.pi:
                        self.target -= 2 * math.pi
                elif self.target < self.angle:
                    while self.target < self.angle - math.pi:
                        self.target += 2 * math.pi
                if self.target < self.angle: # set rotation speed
                    self.rspeed = -abs(self.rspeed)
                else:
                    self.rspeed = abs(self.rspeed)
        elif (self.angle <= self.target if self.rspeed < 0 else self.angle > self.target): # hit target angle, jump
            self.jump = self.jump_distance / self.speed # number of frames to jump
            self.wait = 50 # wait 50 frames before jumping
        else:
            self.angle += self.rspeed # rotate towards target angle
        return True # still alive
            
    # moves the frog to be at the given tile
    def set_to_tile(self, tile):
        self.pos[X] = tile[X] * CELL_SIZE + HALF_CELL_SIZE
        self.pos[Y] = tile[Y] * CELL_SIZE + HALF_CELL_SIZE
        
    # whether or not the frog is on screen
    def on_screen(self):
        return self.pos[X]+Frog.SIZE[X]/2 > camera.pos[X] and self.pos[X] - Frog.SIZE[X]/2 < camera.pos[X] + 800 and self.pos[Y]+Frog.SIZE[Y]/2 > camera.pos[Y] and self.pos[Y] - Frog.SIZE[Y]/2 < camera.pos[Y] + 600

    # the circle that bounds the frog (center, radius)
    def bounding_circle(self):
        return ([self.pos[X],self.pos[Y]], Frog.SIZE[X])
    
    # the box that bounds the frog (left, right, top, bottom)
    def boundingbox(self):
        return (self.pos[X]-Frog.SIZE[X]/2,self.pos[X]+Frog.SIZE[X]/2,self.pos[Y]-Frog.SIZE[Y]/2,self.pos[Y]+Frog.SIZE[Y]/2)
    
    # take damage
    def hit(self, damage):
        self.health -= damage
    
# a pellet fired from Tom's gun
class Pellet():
    
    # creates a pellet at the given position, with the given velocity
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        
    # updates the pellet frame by frame, returning True only if it remains
    def update(self):
        # move
        self.pos[X] += self.vel[X]
        self.pos[Y] += self.vel[Y] + Physics.GRAVITY/2
        self.vel[Y] += Physics.GRAVITY
        
        # find the cell it hit
        pos = level.pos(self.pos)
        hit = level.value(pos)
        if Physics.DENSITY[hit] > 0: # if it hit a solid cell, it is destroyed
            if hit == 'Z': # but it destroys fragile cells
                level[pos[Y]][pos[X]] = ' '
            return False
        # if it hit any on-screen enemies
        for e in active_enemies:
            circ = e.bounding_circle()
            if norm(self.pos,circ[0]) < circ[1]**2:
                e.hit(100) # deal 100 damage, and be destroyed
                return False
        if self.pos[X] < camera.pos[X] or self.pos[X] > camera.pos[X]+800 or self.pos[Y] < camera.pos[Y] or self.pos[Y] > camera.pos[Y] + 600: # off-camera
            return False
        return True

# the camera, following Tom
camera = Camera(tom.pos)
    
# the levels of the game
import user35_p1TXccBaE4_12 as Level1
import user35_olWGcaDt6k_9 as Level2
import user35_Pr8wcUQeVe_10 as Level3
import user35_dftLktlPjt_10 as Level4
import user35_lVH6xonvnQ_8 as Level5

levels = [Level1.level, Level2.level, Level3.level, Level4.level, Level5.level]

# the frame    
frame = simplegui.create_frame("The Adventure of Tom", *CANVAS_SIZE)
frame.set_canvas_background("aqua")
           
# enemies that are active (visible on the screen, or the boss)		   
active_enemies = []

frame_count = 0 # number of frames drawn

# does nothing
def nothing(*args):
    pass

# sets handlers en masse
def set_handlers(draw = nothing, keydown = nothing, keyup = nothing, mouseclick = nothing, mousedrag = nothing):
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    frame.set_mouseclick_handler(mouseclick)
    frame.set_mousedrag_handler(mousedrag)
   
# updates the entire game
def update():
    global active_enemies, score
    active_enemies = [e for e in level.enemies if (e.on_screen())] # reset on-screen enemies
	if level.boss:
		active_enemies.append(level.boss)
    for k in [0,1]: # double-speed
        if tom.health > 0: # update Tom if he's alive
            tom.update()
        for e in active_enemies: # for each enemy
            if not e.update(): # if it dies
                level.enemies.remove(e) # remove it from the level
                active_enemies.remove(e)
                score += e.points # and Tom gains its points
                Mook.POP_SOUND.rewind()
                Mook.POP_SOUND.play()
        level.update() # update the level itself
    
# draws the game in progress, in a level
def draw_midgame(canvas):
    if tom.ground == '@@' or autocomplete: # goal
        tom.hit = tom.heal = 0 # end damage yet to be taken/healed
        # set handlers appropriately
        frame.set_mousedrag_handler(nothing)
        frame.set_mouseclick_handler(nothing)
        frame.set_draw_handler(draw_endgame)
        timer.stop() # time suspended
        Level.COMPLETE_SOUND.rewind()
        Level.COMPLETE_SOUND.play()
        return

    global active_enemies, score, frame_count, disp_score
    camera.update() # camera continues to follow Tom or pan to Tom
    frame_count += 1 # another frame is drawn
    
    update_score()
    
    # draw essential components of game
    level.draw(canvas, camera)
    tom.draw(canvas, camera)
    if level.level_info.snow:
        level.draw_over_snow(canvas, camera, level.level_info.snow)
    for e in active_enemies:
        e.draw(canvas, camera)
    if level.level_info.lavaspeed:
        level.draw_over_lava(canvas, camera)
    
    # draw Tom's health bar, flashing the healing or damaging part
    draw_tom_health(canvas)
    
    draw_score(canvas)
    
    # draw Tom's stats if he is alive
    if tom.health > 0:
        draw_tom_stats(canvas)
    # otherwise disable the player and present end-game screen
    else:
        Tom.THRUSTER_SOUND.pause()
        frame.set_keyup_handler(nothing)
        frame.set_mousedrag_handler(nothing)
        draw_end_message(canvas, "GAME OVER")

# draws Tom's score
def draw_score(canvas):
    s = str(disp_score)
    canvas.draw_text('0'*(5-len(s)) + s,(650,50),20,"black")

def update_score():
    global disp_score
    if score > disp_score:
        disp_score += 4
        if disp_score > score:
            disp_score = score
        return True
    return False
    
def draw_end_message(canvas, main_message):
    if '\n' in Menu.player_name: # player has given name, next click returns to main menu
        message = "Click anywhere to continue"
        frame.set_mouseclick_handler(Menu.level_complete)
        frame.set_keydown_handler(nothing)
    else: # player must type name
        message = "Enter your name: "+Menu.player_name
        frame.set_mouseclick_handler(nothing)
        frame.set_keydown_handler(Menu.type_name)
    message_color = level.level_info.complete_color
    canvas.draw_text(main_message, (250,320), 50, message_color)
    canvas.draw_text(message, (185, 360), 30, message_color)
        
def draw_tom_stats(canvas):
    if tom.gun > 0: # draw Tom's gun and pellets
        canvas.draw_image(Item.GUN_IMAGE, (25,25), (50,50), (30,570), (50,50))
        n = min(tom.gun // 10 * 6, 50)
        if n > 0:
            canvas.draw_image(Item.PELLET_IMAGE, (30,n/2),(60,n), (90,550+n/2),(60,n))
        m = tom.gun % 10 * 6
        if m > 0:
            canvas.draw_image(Item.PELLET_IMAGE, (m/2,3),(m,6), (60+m/2,553+n),(m,6))
    if tom.jetpack > 0: # draw Tom's jetpack and fuel, indicating jetpack heating
        canvas.draw_image(Item.JETPACK_IMAGE, (25,25), (50,50), (150, 570), (50,50))
        width = tom.jetpack*100//tom.jetpack_max
        canvas.draw_line((180,570),(180+width,570),40,"gray")
        if tom.jetpack_jump > 0:
            line_width = 40*(tom.jetpack_jump/tom.jetpack_jump_max)
            if line_width:
                canvas.draw_line((180,590-line_width/2),(180+width,590-line_width/2),line_width,"red")
				
	draw_compass(canvas)

def draw_compass(canvas):
	if level.boss and not level.boss.on_screen():
		level_center = [camera.pos[0] + 400, camera.pos[1] + 300]
		boss_center = level.boss.center()
		angle = math.atan2(level_center[1] - boss_center[1], level_center[0] - boss_center[0])
		canvas.draw_circle((400, 300), 50, 1, 'black')
		canvas.draw_line((400, 300), (400 - 50 * math.cos(angle), 300 - 50 * math.sin(angle)), 1, 'black')
				
def convert_pellets_to_points():
    global score, disp_score
    if tom.gun > 0:
        tom.gun -= 1
        score += 25
        disp_score += 25
        return True
    tom.arm = None
    return False

def convert_fuel_to_points():
    global score, disp_score
    if tom.jetpack > 0:
        if tom.jetpack < 10:
            score += int(tom.jetpack/2)
            tom.jetpack = 0
        else:
            tom.jetpack -= 10
            score += 5
        disp_score = score
        return True
    return False
    
# draws the endgame, in which everything is paused as Tom receives points or awaits user's end input
def draw_endgame(canvas):
    global score, disp_score
    message = ""
    update_score() or convert_pellets_to_points() or convert_fuel_to_points()
    level.draw(canvas, camera)
    tom.draw(canvas, camera)
    draw_tom_health(canvas)
    draw_score(canvas)
    draw_tom_stats(canvas)
    draw_end_message(canvas, "COMPLETE!")

# draws Tom's health bar, with health flashing every other frame where healing or taking damage
def draw_tom_health(canvas):
    canvas.draw_line((10,30),(10+(tom.health/4 if frame_count % 2 == 0 else max(min(tom.max_health,tom.health - tom.hit + tom.heal),0)/4),30),20,"red")

# timer that dictates updates
timer = simplegui.create_timer(20, update)

# initially draw the title screen
frame.set_draw_handler(Menu.draw_title)

# check if all resources are loaded
def check_ready():
    if Frog.IMAGE.get_width() > 0: # the final image resource is loaded
        global ready # the game is ready
        ready = True
        ready_timer.stop()
        frame.set_mouseclick_handler(Menu.click_menu) # allow user to begin clicking the menu

# prepare timer to consistently check whether or not the game is ready
ready_timer = simplegui.create_timer(100, check_ready)
ready_timer.start()

frame.set_draw_handler(Menu.draw_title)
frame.start() # let the game begin!