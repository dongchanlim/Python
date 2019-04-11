"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random
from abc import ABC
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

ULT_BULLET_RADIUS = 7
ULT_BULLET_COLOR = arcade.color.RED
ULT_BULLET_SPEED = 5

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15
TARGET_BONUS_RADIUS = 10
TARTET_BONUS_COLOR = arcade.color.YELLOW

STANDARD_POINT = 1
STRONG_POINT= 7
SAFE_POINT = -10
STRONG_LIVES = 3

class Point:
    # set the point of x-coord and y-coord of center
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        
class Velocity:
    # set the speed of movement with dx and dy
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0


class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)
        
class FlyBase(ABC):
    
    # accomodate the common member datas and functions of target and bullet which has point(center) and velocity object
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True
        
    # draw function is abstract method since it is different according to the object.    
    @abstractmethod    
    def draw(self):
        pass
        
    def advance(self):
        # Make flying object move forward  
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def is_off_screen(self, screen_width, screen_height):
        # Check whether flying object move off the screen or not
        if (self.center.x > screen_width  or self.center.y > screen_height):
            return True
        else:
            return False
    
        
class Bullet(FlyBase):
    # Create the bullet based off the flying object
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.color = BULLET_COLOR        
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)
        
    
    def fire(self, angle):
        # Fire the bullet out of rifle in accordance to the angle of rifle 
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        
class Target(FlyBase, ABC):
    # Create the standard target based off the flying obejct
    def __init__(self):
        #  Make targets randomly flying across the screen
        super().__init__()
        self.center.y = random.uniform(SCREEN_HEIGHT/2, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(1,5)
        self.velocity.dy = random.uniform(-2,2)
        self.radius = TARGET_RADIUS
        self.color = TARGET_COLOR
        self.point = 0
        self.type = "unknown"

    # draw function is abstract method since it is different according to target type.    
    @abstractmethod
    def draw(self):
        pass    

    # hit function is abstract method since it is different according to target type
    @abstractmethod
    def hit(self):
        pass


class StandardTarget(Target):
    
    # Create the standard target based off the standard target
    def __init__(self):
        super().__init__()
        self.type = "Standard"
        self.point = STANDARD_POINT
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)
       
    def hit(self):
        # If the target get hit, it scores 1 point and remove the target.
        self.alive = False
        return self.point

class StrongTarget(Target):
    
    # Create the strong target based off the standard target
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1,3)
        self.velocity.dy = random.uniform(-2,2)
        self.type = "Strong"
        # Total point of strong target is 7 points
        self.point = STRONG_POINT
        # Set 3 hits to destroy this target        
        self.lives = STRONG_LIVES
        
    def draw(self):
        # Put a number inside of a circle
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, self.color)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)
       
    def hit(self):
        # 1 point is awarded for each of the first two hits, 5 points are awarded for the third hit that destroys the target.
        self.lives -= 1
        if self.lives > 0:
            self.alive = True
            self.point = 1
            return self.point
        else:
            self.alive = False
            self.point = 5
            return self.point

class SafeTarget(Target):
    
    #  Create the safe target based off the standard target
    def __init__(self):
        super().__init__()
        self.color = TARGET_SAFE_COLOR
        self.radius = TARGET_SAFE_RADIUS
        self.type = "Safe"

        
    def draw(self):
        #Draw a square instead of a circle
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.radius, self.radius, self.color)
       
    def hit(self):
        self.point = SAFE_POINT        
        # A penalty of 10 points given to score.
        self.alive = False
        return self.point
    
class BonusTarget(Target):
    
    # Create the safe target based off the standard target
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(3,5)
        self.velocity.dy = random.uniform(-2,2)
        self.radius = TARGET_BONUS_RADIUS
        self.color = TARTET_BONUS_COLOR
        self.type = "Bonus"
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)
        
     # If user hit Bonus target, it erases all targets and give the all points of targets which fly across the screeen  
    def hit(self, targets):
        self.alive = False
        for target in targets:
            self.point += target.point
            target.alive = False
        return self.point

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()

        self.draw_score()
        # if the score is less than -30, game over!
        if self.score <= -30:
            self.draw_game_over()
            arcade.finish_render()
            

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()
        

        # decide if we should start a target
        if random.randint(1, 20) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()
            
            
    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        if random.randint(1, 4) == 1:
            target = StandardTarget()
            self.targets.append(target)
        
        elif random.randint(1, 4) == 2:
            target = StrongTarget()
            self.targets.append(target)
            
        elif random.randint(1, 4) == 3:
            target = SafeTarget()
            self.targets.append(target)
            
        elif random.randint(1, 4) == 4:
            target = BonusTarget()
            self.targets.append(target)
        # TODO: Decide what type of target to create and append it to the list

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        # This is bonus target hit
                        if target.type == "Bonus":
                            bullet.alive = False
                            self.score += target.hit(self.targets)
                        # This is other targets hit    
                        else:
                            bullet.alive = False
                            self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)
                # if standard and strong target off the screen, it loses 1 point. Otherwise, it remains the score
                if not (target.type == "Bonus" or  target.type == "Safe"):
                    self.score -= 1

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire if user clicked the mouse left button
        if button == arcade.MOUSE_BUTTON_LEFT:
            angle = self._get_angle_degrees(x, y)

            bullet = Bullet()
            bullet.fire(angle)

            self.bullets.append(bullet)
        
        # Fire if user clicked the mouse right button
        if button == arcade.MOUSE_BUTTON_RIGHT:
            angle = self._get_angle_degrees(x, y)

            bullet = Bullet()
            bullet.radius =  ULT_BULLET_RADIUS
            bullet.color = ULT_BULLET_COLOR
            bullet.fire(angle)
            bullet.velocity.dx = math.cos(math.radians(angle)) * ULT_BULLET_SPEED
            bullet.velocity.dy = math.sin(math.radians(angle)) * ULT_BULLET_SPEED

            self.bullets.append(bullet)
 
            
    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees
    
    def draw_game_over(self):
        """
        Print the message "Game Over" if the score is less than -5
        """
        gameover = "Game Over"
        start_x = SCREEN_WIDTH/2 - 50
        start_y = SCREEN_HEIGHT/2
        arcade.draw_text(gameover, start_x=start_x, start_y=start_y, font_size= 20, color=arcade.color.BLACK)
        
        
        
        

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

    
