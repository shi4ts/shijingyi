# -*- coding:utf-8 -*-

import pygame
import time
import random
import sys
from pygame.locals import *

# Global variables
# window
window_screen = None
# hero
hero = None
# Score.
hit_score = 0
# Whether to suspend
is_pause = False

# Picture variables
# Pause picture
pause_image = None
# hero_fire_music
hero_fire_music = None
# number photo
number_image = []
# score_hp photo.
score_hp_image = None
# Single triple barrel shell photo
one_or_three_barral = []
# Photo of three barrels of ammunition remaining.
bullet_3_stock = None
# max_score
max_score_image = None
# boss_hp
boss_HP_image = None
# line
line_image = None
# Background
background = None
# Start over
restart = None
# Quit the game
exit_game = None
# Operating instructions
description = None

# About the aircraft
## Aircraft HP
HP_list = [1, 20, 100, 20] # enemy0, enemy1, enemy2, hero
# Aircraft size
plane_size = [{"width": 51, "height": 39}, {"width": 69, "height": 89}, {"width": 165, "height": 246},
              {"width": 100, "height": 124}]
# Various aircraft explosive effects count replacement pictures
plane_bomb_time = [5, 8, 14, 8] # enemy0, enemy1, enemy2, hero
# Maximum number of rounds for aircraft
plane_maximum_bullet = [2, 5, 7, 8] # enemy0, enemy1, enemy2, hero
# Blood replenishment
blood_supply = None
# Bullet resupply
bullet_supply = None

# About the bullet
# Type of enemy bullet
bullet_type = ["bullet1.png", "bullet-1.gif", "bullet2.png", "bullet.png"]
# Bullet damage value
bullet_damage_value = [1, 1, 3, 1] # enemy0, enemy1, enemy2, hero
# Replenishment
supply_image = ["bomb-1.gif", "bomb-2.gif"]
# Size of the resupply
supply_size = [{"width": 58, "height": 88}, {"width": 60, "height": 103}]
# List of enemy aircraft references
enemy0_list = [] # enemy0 exists aircraft list
enemy0_maximum = 8 # enemy0 aircraft presence maximum
enemy1_list = [] # enemy1 exists aircraft list
enemy1_maximum = 1
enemy2_list = [] # enemy2 exists aircraft list
enemy2_maximum = 1


class Base(object):
    """base class for all classes"""

    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)


class BasePlane(Base):
    """Aircraft base class"""

    def __init__(self, plane_type, screen_temp, x, y, image_name, picture_num, HP_temp):
        Base.__init__(self, screen_temp, x, y, image_name) # plane_type plane_type
        self.bullet_list = [] # Store references to bullets fired out
        self.plane_type = plane_type # plane type label, 3 is hero
        # The following attributes are used for explosive effects
        self.hitted = False # Indicates if it's going to explode
        self.bomb_picture_list = [] # Used to store the pictures needed for the explosion
        self.bomb_picture_num = picture_num # Number of pictures of the airplane explosion effect
        self.picture_count = 0 # Used to record the number of while True. When the number of times reaches a certain value, an exploded picture is displayed and then emptied.
        self.image_index = 0 # The serial number of the picture used to record the current explosion effect to be displayed
        self.HP = HP_temp # aircraft hp
        self.fire_bullet_count = 0 # The plane has fired bullet count

    def display (self):
        "" "Show player's plane" ""
        global hit_score
        global HP_list
        global plane_bomb_time # Aircraft explosion effect count
        # If it is hit, the explosion effect is displayed, otherwise the normal aircraft effect is displayed
        if self.hitted == True and self.image_index <self.bomb_picture_num and self.HP <= 0:
            self.screen.blit (self.bomb_picture_list [self.image_index], (self.x, self.y))
            if self.plane_type! = 3 and self.image_index == 0 and self.picture_count == 0:
                if self.plane_type == 0: # destroy enemy0 score + HP
                    if hit_score <650: # The initial health is 1
                        hit_score + = HP_list [self.plane_type]
                    else: # The initial health is 2
                        hit_score + = HP_list [self.plane_type] / 2
                elif self.plane_type == 1: # destroy enemy1 score + HP / 2
                    hit_score + = HP_list [self.plane_type] / 2
                else: # Destroy enemy2 score + HP / 4
                    hit_score + = HP_list [self.plane_type] / 4
            self.picture_count + = 1
            if self.picture_count == plane_bomb_time [self.plane_type]: # Depending on the type of aircraft, the duration of the explosion effect is different
                self.picture_count = 0
                self.image_index + = 1
        elif self.image_index <self.bomb_picture_num:
            self.screen.blit (self.image, (self.x, self.y)) # show original image
        if self.hitted == True and not self.bullet_list and self.image_index> = self.bomb_picture_num and self.HP <= 0:
            del_plane (self) # Delete the object hit by the enemy plane
        # Delete the enemy plane after flying out of the window
        if self.y> 860:
            del_plane (self)
        # Delete out-of-bounds bullets
        del_outWindow_bullet (self)

    # Create a reference to the picture of the explosion effect
    def crate_images (self, bomb_picture_name):
        for i in range (1, self.bomb_picture_num + 1):
            self.bomb_picture_list.append (pygame.image.load ("./ feiji /" + bomb_picture_name + str (i) + ".png"))

    # Determine if it was hit
    def isHitted (self, plane, width, height): # widht and height indicate the range
        if plane.bullet_list and self.HP:
            for bullet in plane.bullet_list:
                if bullet.x> self.x + 0.05 * width and bullet.x <self.x + 0.95 * width and bullet.y + 0.1 * height> self.y and bullet.y <self.y + 0.8 * height:
                    self.HP-= bullet.damage_value # hero's HP minus bullet damage value
                    if self.plane_type == 3:
                        show_score_HP ()
                    plane.bullet_list.remove (bullet) # remove the bullet hit
                    self.hitted = True
            if plane.plane_type == 3 and plane.barrel_2 and plane.barrel_3:
                for bullet in plane.barrel_2: # Determine whether the barrel 3 hit
                    if bullet.x> self.x + 0.05 * width and bullet.x <self.x + 0.95 * width and bullet.y + 0.1 * height> self.y and bullet.y <self.y + 0.8 * height:
                        self.HP-= bullet.damage_value # hero's HP minus bullet damage value
                        plane.barrel_2.remove (bullet) # remove the bullet hit
                        self.hitted = True
                for bullet in plane.barrel_3: # Determine whether the barrel 3 hit
                    if bullet.x> self.x + 0.05 * width and bullet.x <self.x + 0.95 * width and bullet.y + 0.1 * height> self.y and bullet.y <self.y + 0.8 * height:
                        self.HP-= bullet.damage_value # hero's HP minus bullet damage value
                        plane.barrel_3.remove (bullet) # remove the bullet hit
                        self.hitted = True

    # Airplane fire
    def fire (self, bullet_maximun):
        if self.HP> 0:
            random_num = random.randint (1, 60)
            if (random_num == 10 or random_num == 45) and len (self.bullet_list) <bullet_maximun:
                self.bullet_list.append (EnemyBullet (self.screen, self.x, self.y, self))
                self.fire_bullet_count + = 1


class HeroPlane (BasePlane):
    global supply_size

    def __init __ (self, screen_temp):
        BasePlane .__ init __ (self, 3, screen_temp, 210, 728, "./feiji/hero1.png", 4, HP_list [3]) # super () .__ init __ ()
        BasePlane.crate_images (self, "hero_blowup_n")
        self.key_down_list = [] # used to store the keyboard up, down, left and right moving keys
        self.space_key_list = [] # save space key
        self.is_three_bullet = False
        self.barrel_2 = [] # No. 2 barrel (left)
        self.barrel_3 = [] # No. 3 barrel (right)
        self.three_bullet_stock = 50 # The initial value of a three-pronged bullet is 50

    # One-touch moving direction
    def move_left (self):
        self.x-= 7

    def move_right (self):
        self.x + = 7

    def move_up (self):
        self.y-= 6

    def move_down (self):
        self.y + = 6

    # Double key movement direction
def move_left_and_up (self):
        self.x-= 5
        self.y-= 6

    def move_right_and_up (self):
        self.x + = 5
        self.y-= 6

    def move_lef_and_down (self):
        self.x-= 5
        self.y + = 6

    def move_right_and_down (self):
        self.x + = 5
        self.y + = 6

    # Control the range of aircraft movement
    def move_limit (self):
        if self.x <0:
            self.x = -2
        elif self.x + 100> 480:
            self.x = 380
        if self.y> 728:
            self.y = 728
        elif self.y <350:
            self.y + = 6

    # Press the keyboard to add a key to the list
    def key_down (self, key):
        self.key_down_list.append (key)

    # Release the keyboard to delete the key to the list
    def key_up (self, key):
        if len (self.key_down_list)! = 0: # judge whether it is empty
            try:
                self.key_down_list.remove (key)
            except Exception:
                pass

    # Control the continuous movement of hero
    def press_move (self):
        if len (self.key_down_list)! = 0:
            if len (self.key_down_list) == 2: # two keys
                if (self.key_down_list [0] == K_LEFT and self.key_down_list [1] == K_UP) or (
                        self.key_down_list [1] == K_LEFT and self.key_down_list [
                    0] == K_UP): # key_down_list list key is left, up or up, call move_left_and_up () method when left
                    self.move_left_and_up ()
                elif (self.key_down_list [0] == K_RIGHT and self.key_down_list [1] == K_UP) or (
                        self.key_down_list [1] == K_RIGHT and self.key_down_list [0] == K_UP):
                    self.move_right_and_up ()
                elif (self.key_down_list [0] == K_LEFT and self.key_down_list [1] == K_DOWN) or (
                        self.key_down_list [1] == K_LEFT and self.key_down_list [0] == K_DOWN):
                    self.move_lef_and_down ()
                elif (self.key_down_list [0] == K_RIGHT and self.key_down_list [1] == K_DOWN) or (
                        self.key_down_list [1] == K_RIGHT and self.key_down_list [0] == K_DOWN):
                    self.move_right_and_down ()
            else: # a key
                if self.key_down_list [0] == K_LEFT:
                    self.move_left ()
                elif self.key_down_list [0] == K_RIGHT:
                    self.move_right ()
                elif self.key_down_list [0] == K_UP:
                    self.move_up ()
                elif self.key_down_list [0] == K_DOWN:
                    self.move_down ()

    # Blew
    def bomb (self):
        self.hitted = True
        self.HP = 0

    # Press the keyboard to add space to the list
    def space_key_down (self, key):
        self.space_key_list.append (key)

    # Keyboard release to delete space to the list
    def space_key_up (self, key):
        if len (self.space_key_list)! = 0: # judge whether it is empty
            try:
                self.space_key_list.pop (0)
            except Exception:
                raise

    # Keep pressing the space button and keep firing
    def press_fire (self):
        if len (self.bullet_list) == 0 and len (self.space_key_list):
            self.fire ()
        else:
            if len (self.space_key_list)! = 0:
                if self.bullet_list [len (self.bullet_list)-1] .y <self.y-14-60:
                    self.fire ()

    # Fire
    def fire (self):
        global plane_maximum_bullet
        hero_fire_music.play ()
        if not self.is_three_bullet:
            if len (self.bullet_list) <plane_maximum_bullet [self.plane_type]: # The limit of a single round bullet is 8
                self.bullet_list.append (Bullet (self.screen, self.x + 40, self.y-14, self))
        else: # No bullet limit
    # Main barrel
            self.bullet_list.append (Bullet (self.screen, self.x + 40, self.y-14, self))
            # Create No. 2 and No. 3 barrel bullets
            self.barrel_2.append (Bullet (self.screen, self.x + 5, self.y + 20, self))
            self.barrel_3.append (Bullet (self.screen, self.x + 75, self.y + 20, self))
            self.three_bullet_stock-= 1 # Three-barrel shell ammunition balance -1
            if not self.three_bullet_stock: # Three-pronged ammunition runs out
                self.is_three_bullet = False

    # Whether to eat supplies
    def supply_hitted (self, supply_temp, width, height): # widht and height indicate the range
        if supply_temp and self.HP:
            # More precise determination of whether to get supplies
            supply_temp_left_x = supply_temp.x + supply_size [supply_temp.supply_type] ["width"] * 0.15
            supply_temp_right_x = supply_temp.x + supply_size [supply_temp.supply_type] ["width"] * 0.85
            supply_temp_top_y = supply_temp.y + supply_size [supply_temp.supply_type] ["height"] * 0.4
            supply_temp_bottom_y = supply_temp.y + supply_size [supply_temp.supply_type] ["height"] * 0.9
            if supply_temp_left_x> self.x + 0.05 * width and supply_temp_right_x <self.x + 0.95 * width and supply_temp_top_y <self.y + 0.95 * height and supply_temp_bottom_y> self.y + 0.1 * height:
                if supply_temp.supply_type == 0: # 0 is the blood volume supply, eat the blood volume supply
                    self.HP-= supply_temp.supply_HP # blood volume-(-3)
                    if self.HP> 41: # The maximum blood volume is 41
                        self.HP = 41
                    show_score_HP ()
                else: # Eat ammo supply
                    self.is_three_bullet = True
                    self.three_bullet_stock + = 20 # Three-barrel shell remaining +20
                del_supply (supply_temp)


class Enemy0Plane (BasePlane):
    "" "enemy0 的 类" ""

    def __init __ (self, screen_temp):
        random_num_x = random.randint (12, 418)
        random_num_y = random.randint (-50, -40)
        BasePlane .__ init __ (self, 0, screen_temp, random_num_x, random_num_y, "./feiji/enemy0.png", 4, HP_list [0])
        BasePlane.crate_images (self, "enemy0_down") # The second parameter is the plane_type of the aircraft, 0 is enemy0

    def move (self):
        self.y + = 4


class Enemy1Plane (BasePlane):
    "" "enemy1" "" "

    def __init __ (self, screen_temp):
        BasePlane .__ init __ (self, 1, screen_temp, 205, -90, "./feiji/enemy1.png", 4, HP_list [1])
        BasePlane.crate_images (self, "enemy1_down")
        self.direction = "right" # used to store the default display direction of the aircraft
        self.num_y = random.randint (15, 400) # The y value that moves left and right after it appears

    # Move
    def move (self):
        if self.direction == "right":
            self.x + = 4
        elif self.direction == "left":
            self.x-= 4
        # Direction judgment
        if self.x + 70> 480:
            self.direction = "left"
        elif self.x <0:
            self.direction = "right"
        if self.y <self.num_y:
            self.y + = 3
        elif self.fire_bullet_count> 10: # The number of bullets fired exceeds 10, ie move down
            self.y + = 4


class Enemy2Plane (BasePlane):
    "" "enemy2" "" "


    def __init __ (self, screen_temp):
        BasePlane .__ init __ (self, 2, screen_temp, 158, -246, "./feiji/enemy2.png", 5, HP_list [2])
        BasePlane.crate_images (self, "enemy2_down")
        self.direction = "right" # used to store the default display direction of the aircraft

    # Move
    def move (self):
        if self.direction == "right":
            self.x + = 5
        elif self.direction == "left":
            self.x-= 5
        # Direction judgment
        if self.x + 165> 480:
            self.direction = "left"
        elif self.x <0:
            self.direction = "right"
        if self.y <0:
            self.y + = 4
        elif self.fire_bullet_count> 25: # The number of bullets fired exceeds 25, ie move down
            self.y + = 3


class BaseBullet (Base):
    "" "Bullet base class" ""
    global bullet_damage_value

    def __init __ (self, screen_temp, x, y, image_name, plane):
        Base .__ init __ (self, screen_temp, x, y, image_name)
if plane:
            self.damage_value = bullet_damage_value [plane.plane_type]

    # Bullet display
    def display (self):
        self.screen.blit (self.image, (self.x, self.y))


class Bullet (BaseBullet):
    "" "hero 子弹" ""
    global bullet_type

    def __init __ (self, screen_temp, x, y, plane):
        BaseBullet .__ init __ (self, screen_temp, x, y, "./feiji/" + bullet_type [plane.plane_type], plane)

    def move (self):
        self.y-= 16

    def judge (self):
        if self.y <0:
            return True
        else:
            return False


class EnemyBullet (BaseBullet):
    "" "enemy 子弹" ""
    global bullet_type
    global plane_size

    def __init __ (self, screen_temp, x, y, plane):
        BaseBullet .__ init __ (self, screen_temp, x + plane_size [plane.plane_type] ["width"] / 2,
                            y + plane_size [plane.plane_type] ["height"] / 2, "./feiji/" + bullet_type [plane.plane_type],
                            plane) # x, y is the location of the bullet

    def move (self):
        self.y + = 7

    # Cross-border judgment
    def judge (self):
        if self.y> 852:
            return True
        else:
            return False


class supply_2_hero (BaseBullet):
    "" "hero supply" "" "

    def __init __ (self, screen_temp, x, y, suppl_type_temp, speed_temp, s_HP):
        BaseBullet .__ init __ (self, screen_temp, x, y, "./feiji/" + supply_image [suppl_type_temp], None)
        self.speed = speed_temp
        self.supply_HP = s_HP
        self.supply_type = suppl_type_temp

    def move (self):
        self.y + = self.speed

    # Cross-border judgment
    def judge (self):
        if self.y> 855:
            return True
        else:
            return False


# Function
def del_outWindow_bullet (plane):
    "" "Delete the plane's cross-border bullet
    bullet_list_out = [] # out of bound bullet
    for bullet in plane.bullet_list:
        bullet.display ()
        bullet.move ()
        if bullet.judge (): # Determine whether the bullet is out of bounds
            bullet_list_out.append (bullet)
    # Delete out-of-bounds bullets
    if bullet_list_out:
        for bullet in bullet_list_out:
            plane.bullet_list.remove (bullet)
    # If it is a hero and it is fired in three tubes, then judge whether the bullet of the barrel 23 crosses the boundary
    if plane.plane_type == 3 and (plane.barrel_2 or plane.barrel_3):
        barrel2_bullet_out = [] # out of bound bullet
        barrel3_bullet_out = [] # out of bound bullet
        # Judge barrel 2
        for bullet in plane.barrel_2:
            bullet.display ()
            bullet.move ()
            if bullet.judge (): # Determine whether the bullet is out of bounds
                barrel2_bullet_out.append (bullet)
        # Delete out-of-bounds bullets
        if barrel2_bullet_out:
            for bullet in barrel2_bullet_out:
                plane.barrel_2.remove (bullet)
        # Judge barrel 3
        for bullet in plane.barrel_3:
            bullet.display ()
            bullet.move ()
            if bullet.judge (): # Determine whether the bullet is out of bounds
                barrel3_bullet_out.append (bullet)
        # Delete out-of-bounds bullets
if barrel3_bullet_out:
            for bullet in barrel3_bullet_out:
                plane.barrel_3.remove (bullet)


def del_plane (plane):
    "" "Recover the target of the hit enemy aircraft" ""
    global hero
    global hit_score
    global enemy0_list
    global enemy1_list
    global enemy2_list
    if plane in enemy0_list: # Recycle object is enemy0
        enemy0_list.remove (plane)
    elif plane in enemy1_list:
        enemy1_list.remove (plane)
    elif plane in enemy2_list:
        enemy2_list.remove (plane)
    elif plane == hero: # Recycle object is hero
        hit_score = 0
        show_score_HP ()
        hero = None


def del_supply (supply):
    "" "Recycling Supplies" ""
    global blood_supply
    global bullet_supply
    if supply == blood_supply: # The recovery target is blood volume supply
        blood_supply = None
    elif supply == bullet_supply:
        bullet_supply = None


def reborn ():
    "" "Hero Rebirth" ""
    global hero
    global window_screen
    global hit_score
    hero = HeroPlane (window_screen)
    show_score_HP ()
    hit_score = 0


# Write the highest score to the file
def max_score_2_file ():
    global hit_score
    file = None
    try:
        file = open ("./ Aircraft battle scoreboard.txt", 'r +')
    except Exception:
        file = open ("./ Aircraft battle scoreboard.txt", 'w +')
    finally:
        if file.read (): # Determine whether the file is empty
            file.seek (0, 0) # Go to the beginning of the file
            file_score = eval (file.read ())
            if hit_score> file_score:
                file.seek (0, 0) # Go to the beginning of the file
                file.truncate () # clear file content
                file.write (str (hit_score))
        else:
            file.write (str (hit_score))
        file.close ()


def create_enemy_plane ():
    "" "Generate enemy aircraft" ""
    global window_screen
    global hit_score
    global enemy0_list
    global enemy0_maximum
    global enemy1_list
    global enemy1_maximum
    global enemy2_list
    global enemy2_maximum
    global HP_list

    if hit_score <40:
        random_num = random.randint (1, 70)
        HP_list = [1, 20, 100, 20]
    elif hit_score <450:
        random_num = random.randint (1, 60)
        HP_list = [1, 20, 120, 20]
    elif hit_score <650:
        random_num = random.randint (1, 60)
        HP_list = [1, 30, 140, 20]
    elif hit_score <850:
        random_num = random.randint (1, 55)
        HP_list = [2, 36, 160, 20]
    else:
        random_num = random.randint (1, 50)
        HP_list = [2, 40, 180, 20]
    random_appear_boss1 = random.randint (18, 28)
    random_appear_boss2 = random.randint (80, 100)
    # enemy0
    if (random_num == 20 or random == 40) and len (enemy0_list) <enemy0_maximum:
        enemy0_list.append (Enemy0Plane (window_screen))
    # enemy1
    if (hit_score> = random_appear_boss1 and (hit_score% random_appear_boss1) == 0) and len (
            enemy1_list) <enemy1_maximum:
    enemy1_list.append (Enemy1Plane (window_screen))
    # enemy2
    if (hit_score> = random_appear_boss2 and (hit_score% random_appear_boss2) == 0) and len (
            enemy2_list) <enemy2_maximum:
        enemy2_list.append (Enemy2Plane (window_screen))


def create_supply_2_hero (s_type):
    "" "Create blood volume and ammunition supply for hero" ""
    global window_screen
    global blood_supply
    global bullet_supply
    global enemy2_list
    if enemy2_list: # enemy2 has a higher supply probability when it exists
        random_limitation = 1201
    else:
        random_limitation = 2080
    random_supply = random.randint (1, random_limitation)
    if (random_supply% 690) == 0 and s_type == 0: # HP
        blood_supply = supply_2_hero (window_screen, random.randint (0, 480-58), random.randint (-105, -95), s_type, 3,
                                     -3) # -Supply type, -Speed, -Supply blood volume value (subtraction is used)
    elif (random_supply% 300) == 0 and s_type == 1: # ammunition supply
        bullet_supply = supply_2_hero (window_screen, random.randint (0, 480-60), random.randint (-115, -108), s_type, 3,
                                      0)


def enemy_display_move_fire (enemy):
    "" "Display of enemy aircraft, move, fire" ""
    global window_screen
    global hero
    global plane_maximum_bullet

    enemy.display () # enemy display
    enemy.move () # Control the movement of enemy aircraft
    enemy.fire (plane_maximum_bullet [enemy.plane_type]) # enemy plane fires
    if hero: # Aircraft hit judgment
        hero.isHitted (enemy, plane_size [hero.plane_type] ["width"], plane_size [hero.plane_type] ["height"]) # whether to hit hero
        enemy.isHitted (hero, plane_size [enemy.plane_type] ["height"],
                       plane_size [enemy.plane_type] ["height"]) # Whether to hit enemy


def supply_display_move (supply):
    "" "Judgment of Supply" "" "
    supply.display ()
    supply.move ()
    if supply.judge (): # Cross-border recycling
        del_supply (supply)


# Score, hp, single tube, three tube, three tube bullet remaining display
def show_score_HP ():
    global window_screen
    global hero
    global hit_score
    global number_image
    global score_hp_image
    global one_or_three_barral
    global bullet_3_stock
    global max_score_image
    global boss_HP_image
    global enemy2_list
    # line
    window_screen.blit (line_image, (482, 445))
    if hero: # hero object exists
        # Post score_hp
        window_screen.blit (score_hp_image, (480, 460))
        if not hero.is_three_bullet: # single tube
            window_screen.blit (one_or_three_barral [0], (480, 560))
        else: # Three tubes
            window_screen.blit (one_or_three_barral [1], (480, 560))
        window_screen.blit (bullet_3_stock, (480, 605)) # paste three tube bullets
        # Post score
        hit_score_temp = cut_number (hit_score) # Get the cut tuple (hundred, ten, one)
        window_screen.blit (number_image [hit_score_temp [0]], (600, 460))
        window_screen.blit (number_image [hit_score_temp [1]], (630, 460))
        window_screen.blit (number_image [hit_score_temp [2]], (660, 460))
        # Post hp
        HP_temp = cut_number (hero.HP)
        window_screen.blit (number_image [HP_temp [0]], (600, 510))
        window_screen.blit (number_image [HP_temp [1]], (630, 510))
        window_screen.blit (number_image [HP_temp [2]], (660, 510))
        # Post three bullets
        three_bullet_stock_temp = cut_number (hero.three_bullet_stock)
        window_screen.blit (number_image [three_bullet_stock_temp [0]], (605, 600))
        window_screen.blit (number_image [three_bullet_stock_temp [1]], (635, 600))
        window_screen.blit (number_image [three_bullet_stock_temp [2]], (665, 600))
    else: # hero object does not exist
        # Paste score_hp, single tube, three tube bullet allowance
        window_screen.blit (score_hp_image, (480, 460))
        window_screen.blit (one_or_three_barral [0], (480, 560))
        window_screen.blit (bullet_3_stock, (480, 605)) # paste three tube bullets
        # Post score
        window_screen.blit (number_image [0], (600, 460))
        window_screen.blit (number_image [0], (630, 460))
        window_screen.blit (number_image [0], (660, 460))
        # Post hp
        window_screen.blit (number_image [0], (600, 510))
        window_screen.blit (number_image [0], (630, 510))
        window_screen.blit (number_image [0], (660, 510))
        # Post three bullets
window_screen.blit (number_image [0], (605, 600))
        window_screen.blit (number_image [0], (635, 600))
        window_screen.blit (number_image [0], (665, 600))
    if enemy2_list: # Hp posted enemy2
        # boss_hp
        window_screen.blit (boss_HP_image, (480, 640))
        enemy2_hp_temp = (0, 0, 0)
        if enemy2_list [0] .HP> 0: # Avoid enemy2 having a negative health when it is in an explosion
            enemy2_hp_temp = cut_number (enemy2_list [0] .HP)
            # Paste enemy2_hp
            window_screen.blit (number_image [enemy2_hp_temp [0]], (590, 640))
            window_screen.blit (number_image [enemy2_hp_temp [1]], (620, 640))
            window_screen.blit (number_image [enemy2_hp_temp [2]], (650, 640))
    # line
    window_screen.blit (line_image, (482, 690))


# Show maximum score
def show_max_score ():
    global number_image
    global window_screen
    file = None
    max_score = 0
    try:
        file = open ("./ Aircraft battle scoreboard.txt", "r")
        max_score = eval (file.read ())
    except Exception as e:
        raise
    finally: # Post the highest score
        max_score_temp = cut_number (max_score)
        window_screen.blit (number_image [max_score_temp [0]], (590, 700))
        window_screen.blit (number_image [max_score_temp [1]], (620, 700))
        window_screen.blit (number_image [max_score_temp [2]], (650, 700))

    # Cut the number into hundreds of ten digits


def cut_number (number):
    if number> 999:
        number = 999
    hundred_num = round (number // 100) # round down
    number% = 100
    ten_num = round (number // 10)
    number% = 10
    single_num = round (number // 1)
    return (hundred_num, ten_num, single_num)


# Whether to pause
def pause ():
    global is_pause
    global window_screen
    global pause_image
    global is_play_music
    while is_pause:
        pygame.mixer.music.pause () # Pause music
        # Show paused pictures
        window_screen.blit (pause_image, (170, 402)) # background
        # Update picture
        pygame.display.update ()
        time.sleep (0.1) # sleep for 0.1 seconds
        key_control ()


# Import digital pictures
def image_load ():
    global number_image
    global score_hp_image
    global one_or_three_barral
    global bullet_3_stock
    global max_score_image
    global boss_HP_image
    global line_image
    global background
    global restart
    global exit_game
    global description
    global pause_image
    try:
        # Pause the picture
        pause_image = pygame.image.load ("./ feiji / btn_finish.png")
        # Import from the right picture
        background = pygame.image.load ("./ feiji / background.png")
        restart = pygame.image.load ("./ feiji / restart_nor.png")
        exit_game = pygame.image.load ("./ feiji / quit_nor.png")
        description = pygame.image.load ("./ feiji / description.png")
        # Digital picture import
        for i in range (10):
            number_image.append (pygame.image.load ("./ feiji / number_" + str (i) + ".png"))
        # score_hpimport
        score_hp_image = pygame.image.load ("./ feiji / score_hp.png")
        # Single three-barrel shell photo
        one_or_three_barral.append (pygame.image.load ("./ feiji / bullet_temp1.png")) # single tube
        one_or_three_barral.append (pygame.image.load ("./ feiji / bullet_temp3.png")) # Three tubes
        # Three-barrel bullet residual photo
        bullet_3_stock = pygame.image.load ("./ feiji / bullet_3_stock.png")
        # Highest score
        max_score_image = pygame.image.load ("./ feiji / max_score.png")
        # boss_hp
        boss_HP_image = pygame.image.load ("./ feiji / boss_HP.png")
# line_image
        line_image = pygame.image.load ("./ feiji / line.png")
    except Exception as e:
        raise


# Display background image and picture on the right
def show_background_right_image ():
    global background
    global restart
    global exit_game
    global description
    global max_score_image
    window_screen.blit (background, (0, 0)) # background
    window_screen.blit (description, (482, 10)) # Operation instruction picture
    window_screen.blit (max_score_image, (480, 705)) # maximum score
    max_score_2_file () # Can score synchronously when breaking records
    show_max_score () # can show the score when breaking records simultaneously
    window_screen.blit (restart, (530, 760)) # restart the game picture
    window_screen.blit (exit_game, (532, 810)) # Exit game picture


# Import music
pygame.mixer.init ()


def background_music_load ():
    try:
        global hero_fire_music
        pygame.mixer.music.load ("./ music / PlaneWarsBackgroundMusic.mp3") # game background music
        pygame.mixer.music.set_volume (0.3) # Set the volume (0-1)
        pygame.mixer.music.play (-1) # loop play
        hero_fire_music = pygame.mixer.Sound ("./ music / hero_fire.wav") # hero fire music
        hero_fire_music.set_volume (0.2)
    except Exception as e:
        raise


# Keyboard control
def key_control ():
    global hero
    global is_pause
    global hero_fire_music
    global plane_maximum_bullet
    global enemy0_list
    global enemy1_list
    global enemy2_list
    global blood_supply
    global bullet_supply
    global hit_score
    # Get events, such as key presses, etc.
    for event in pygame.event.get ():
        # Determine if the exit button is clicked
        if event.type == QUIT:
            # print ("exit")
            exit ()
        # Determine if the key is pressed
        elif event.type == KEYDOWN:
            # Check if the key is left
            if hero:
                if event.key == K_LEFT:
                    hero.key_down (K_LEFT)
                # Check if the key is right
                elif event.key == K_RIGHT:
                    hero.key_down (K_RIGHT)
                elif event.key == K_UP:
                    hero.key_down (K_UP)
                # Check if the key is right
                elif event.key == K_DOWN:
                    hero.key_down (K_DOWN)
                # Check if the key is s
                elif event.key == K_s: # Save or enable the number of three-tube bullets
                    if hero.three_bullet_stock> 0:
                        if hero.is_three_bullet: # true to false
                            hero.is_three_bullet = False
                        else: # false becomes true
                            hero.is_three_bullet = True
                # Check if the key is a space bar
                elif event.key == K_SPACE and hero.HP:
                    hero.space_key_down (K_SPACE) # Add k_space to the space list
                # Check if the button is b
                elif event.key == K_b: # self-explosive
                    hero.bomb ()
            # Check if the key is q
            if event.key == K_q:
                if is_pause: # true to false
                    is_pause = False
                    pygame.mixer.music.unpause () # resume playing
                else: # false becomes true
                    is_pause = True
            if event.key == K_r:
                reborn ()
        # Determine whether the key is released
        elif event.type == KEYUP and hero:
            # Check if the loose key is left
            if event.key == K_LEFT:
                hero.key_up (K_LEFT)
            # Check if the key is right
            elif event.key == K_RIGHT:
                hero.key_up (K_RIGHT)
# Check if the key is up
            elif event.key == K_UP:
                hero.key_up (K_UP)
            # Check if the button is down
            elif event.key == K_DOWN:
                hero.key_up (K_DOWN)
            # Check if the key is space
            elif event.key == K_SPACE:
                hero.space_key_up (K_SPACE)
        # Determine the click of the mouse
        elif event.type == MOUSEBUTTONDOWN: # mouse down
            pressed_array = pygame.mouse.get_pressed () # get mouse click type [0,1,2] left button, wheel, mail
            for index in range (len (pressed_array)):
                if pressed_array [index]:
                    if index == 0: # left mouse button clicked
                        pos = pygame.mouse.get_pos () # Get the mouse click coordinates
                        mouse_x = pos [0]
                        mouse_y = pos [1]
                        # Determine the type of event triggered by mouse click coordinates
                        if mouse_x> 170 and mouse_x <310 and mouse_y> 402 and mouse_y <450 and is_pause == True: # return game events
                            pygame.mixer.music.unpause () # resume playing
                            is_pause = False # do not pause
                        elif mouse_x> 530 and mouse_x <642 and mouse_y> 760 and mouse_y <808: # restart the game event
                            # Recycle all pairs
                            reborn ()
                            enemy0_list = []
                            enemy1_list = []
                            enemy2_list = []
                            blood_supply = None
                            bullet_supply = None
                            # hit_score = 0
                            # main ()
                        elif mouse_x> 532 and mouse_x <642 and mouse_y> 810 and mouse_y <834: # exit game event
                            exit ()


def main ():
    global window_screen
    global hero
    global hit_score
    global HP_list
    global blood_supply
    global bullet_supply
    global enemy0_list
    global enemy1_list
    global enemy2_list
    global number_image
    global score_hp_image
    global one_or_three_barral
    global bullet_3_stock
    global background
    global restart
    global exit_game
    global description
    global is_play_music

    print ("Author: GuYongtao, E-mail: guyongtao@qq.com, Time: 2018/04/21")
    # Score transition
    hit_score_temp = hit_score
    # Background color
    bg_color = (205, 205, 205)
    # 1. Create a window
    window_screen = pygame.display.set_mode ((695, 852), 0, 32)
    # 2. Create a background image
    try:
        image_load () # Import of digital pictures etc.
    except Exception:
        raise

    # 3. Create an airplane object
    hero = HeroPlane (window_screen)
    # 4. Import background music
    background_music_load ()
    # Title
    pygame.display.set_caption ('Airplane Wars')
    while True:
        # Background color fill
        window_screen.fill (bg_color)
        # Score update
        if hit_score> = 999:
            hit_score = 999
        if hit_score> hit_score_temp and hero:
            hit_score_temp = hit_score
            show_score_HP ()
        elif hit_score <hit_score_temp:
            hit_score_temp = 0
        # Create enemy aircraft
        create_enemy_plane ()
        # Create supplies
        # Health volume supply, 0- supply type, 3- supply speed, -3- supply HP
        if not blood_supply:
            create_supply_2_hero (0)
        # Ammunition supply
        if not bullet_supply:
            create_supply_2_hero (1)
        # Display background and right picture
        show_background_right_image ()

        # hero
        if hero:
hero.display () # hero display
            if hero:
                hero.press_move () # keep moving
                hero.press_fire () # Keep firing
                hero.move_limit () # hero moving range judgment
        # blood_supply
        if blood_supply:
            supply_display_move (blood_supply)
        # bullet_supply
        if bullet_supply:
            supply_display_move (bullet_supply)
        # Whether to eat supplies
        if hero and blood_supply:
            hero.supply_hitted (blood_supply, plane_size [hero.plane_type] ["width"],
                               plane_size [hero.plane_type] ["height"])
        if hero and bullet_supply:
            hero.supply_hitted (bullet_supply, plane_size [hero.plane_type] ["width"],
                               plane_size [hero.plane_type] ["height"])
        # enemy0
        if enemy0_list:
            for enemy0 in enemy0_list:
                enemy_display_move_fire (enemy0)
        # enemy1
        if enemy1_list:
            for enemy1 in enemy1_list:
                enemy_display_move_fire (enemy1)
        # enemy2
        if enemy2_list:
            for enemy2 in enemy2_list:
                enemy_display_move_fire (enemy2)
        # Score, HP display
        show_score_HP ()
        # Whether to pause
        pause ()
        # Update picture
        pygame.display.update ()
        # Call keyboard control
        key_control ()
        # System sleep time (different computer configurations affect the smooth running of the game)
        time.sleep (0.04)


if __name__ == "__main__":
    main ()


