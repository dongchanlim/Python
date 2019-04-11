"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import math
import random
from abc import ABC
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.05
SHIP_RADIUS = 30

ENERGY_BAR_X = 60
ENERGY_BAR_Y = SCREEN_HEIGHT - 20
ENERGY_BAR_WIDTH = 100
ENERGY_BAR_HEIGHT = 20

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15
BIG_ROCK_POINT = 1

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5
MEDIUM_ROCK_POINT = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2
SMALL_ROCK_POINT = 10

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
    
    
        
class FlyingObject(ABC):
    # set an abstract basic class for common interface for bullet, ship, and asteroid
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = 0
        self.angle = 0

    
    @abstractmethod
    def draw(self):
        pass
    
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
    def wrap(self, screen_width, screen_height):
        # if an object goes off the right edge of the screen, it should appear on the left edge
        if self.center.x > screen_width:
            self.center.x = 0
        elif self.center.x < 0:
            self.center.x = screen_width
        elif self.center.y > screen_height:
            self.center.y = 0
        elif self.center.y < 0:
            self.center.y = screen_height
            
class EnergyBar:
    # set the energy that measure the life of ship.
    def __init__(self):
        self.center = Point()
        self.center.x = ENERGY_BAR_X
        self.center.y = ENERGY_BAR_Y
        self.alive = True
        self._width = ENERGY_BAR_WIDTH
        self.height = ENERGY_BAR_HEIGHT
        self.color = arcade.color.RED
        self.angle = 0
    
    # set the width as property so that it can't be changed off the class
    @property
    def width(self):
        if self._width <= 0:
            return 0
        return self._width 
    

        
    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.width, self.height, self.color, self.angle)
     
    # when ship get hitted by asteroids, the lifebar will decrease, and when it reaches 0, it will disappear.
    def lifereduce(self):
        self._width -= 20
        if self._width == 0:
            self.alive = False
               
        
class Ship(FlyingObject):
    # set the ship attributes and methods based off the flying object
    def __init__(self):
        super().__init__()
        self.radius = SHIP_RADIUS
        self.center.x = SCREEN_WIDTH // 2
        self.center.y = SCREEN_HEIGHT // 2
        self.turn = SHIP_TURN_AMOUNT

        
    def draw(self):
        img = "images/playerShip1_orange.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
         
        
        
class Bullet(FlyingObject):
    # Create the bullet based off the flying object
    def __init__(self):
        super().__init__()
        self.velocity.dx = BULLET_SPEED
        self.velocity.dy = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.angle = 90
        

        
    def draw(self):
        img = "images/laserBlue01.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    # when bullet is fired, it follows the angle and velocity of the ship. 
    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle - 270)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle - 270)) * BULLET_SPEED
        return (self.velocity.dx, self.velocity.dy)
    
    # The bullets are stored at the point of ship and follows the ship's speed and angle
    def store(self, ship):
        self.center.x = ship.center.x
        self.center.y = ship.center.y
        self.angle += ship.angle 
        self.velocity.dx = ship.velocity.dx + self.fire(ship.angle)[0]
        self.velocity.dy = ship.velocity.dy + self.fire(ship.angle)[1]
        
class Asteroid(FlyingObject, ABC):
    # Create abstract base class Asteroid based off the flying obejct
    def __init__(self):
        super().__init__()
        self.spinspeed = 0
        self.point = 0

    # draw function is abstract method since it is different according to asteroid type.    
    @abstractmethod
    def draw(self):
        pass
    
    # in addition to speed, asteroids spin over as it advances
    def advance(self):
        self.angle += self.spinspeed
        self.center.x += self.velocity.dx  
        self.center.y += self.velocity.dy
        
    @abstractmethod    
    def divide(self):
        pass
    
    def hit(self):
        parts = self.divide()
        return [parts, self.point]
    
class LargeA(Asteroid):
    
    def __init__(self):
        super().__init__()
        self.center.x =  random.uniform(0,SCREEN_WIDTH)
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-BIG_ROCK_SPEED ,BIG_ROCK_SPEED )  
        self.velocity.dy = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)  
        self.radius = BIG_ROCK_RADIUS
        self.spinspeed = BIG_ROCK_SPIN
        self.point = BIG_ROCK_POINT
        
    def draw(self):
        img = "images/meteorGrey_big1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    # When it is hit, it returns 1 medium A and 2 small A and corresponding points as list. 
    def divide(self):
        parts = [ MediumA(), SmallA(), SmallA()]
        for part in parts:
            part.center.x = self.center.x
            part.center.y = self.center.y
        return parts
    

        

class MediumA(Asteroid):
    
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(-(BIG_ROCK_SPEED + 2),(BIG_ROCK_SPEED + 2)) 
        self.velocity.dy = random.uniform(-(BIG_ROCK_SPEED + 2),(BIG_ROCK_SPEED + 2)) 
        self.radius = MEDIUM_ROCK_RADIUS
        self.spinspeed = MEDIUM_ROCK_SPIN
        self.point = MEDIUM_ROCK_POINT
        
    def draw(self):
        img = "images/meteorGrey_med1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)

    # When it is hit, it returns 2 small A and corresponding points as list. 
    def divide(self):
        parts = [ SmallA(), SmallA()]
        for part in parts:
            part.center.x = self.center.x
            part.center.y = self.center.y
        return parts
            
    

class SmallA(Asteroid):
    
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(-(BIG_ROCK_SPEED + 5),(BIG_ROCK_SPEED + 5))  
        self.velocity.dy = random.uniform(-(BIG_ROCK_SPEED + 5),(BIG_ROCK_SPEED + 5)) 
        self.radius = SMALL_ROCK_RADIUS
        self.spinspeed = SMALL_ROCK_SPIN
        self.point = SMALL_ROCK_POINT
        
    def draw(self):
        img = "images/meteorGrey_small1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle
        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    # When it is hit, it returns nothing and corresponding points as list.         
    def divide(self):
        parts = []
        return parts
            
           


        





class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)


        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.energybar = EnergyBar()
        self.held_keys = set()
        self.bullets = list()
        self.asteroids = list()
        self.score = 0
        for i in range(5):
            asteroid = LargeA()
            self.asteroids.append(asteroid)
        
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        
        # set the background of universe on the screen
        img = "images/universe.jpg"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, texture, 0, 1)

        # TODO: draw each object
        
        self.draw_score()
        
        for bullet in self.bullets:
            bullet.draw()
        
        for asteroid in self.asteroids:
            asteroid.draw()

        if self.energybar.alive:
            self.energybar.draw()
            
        if self.ship.alive:
            self.ship.draw()
        
        # if ship died or all asteroids disappeared, it will show game over message.
        if not self.ship.alive or len(self.asteroids) == 0:
            self.ship.alive = False
            self.energybar.alive = False
            self.draw_game_over()
            
            
            
            
    # draw a score on the top right of screen        
    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = SCREEN_WIDTH - 80
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)            
        

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()
        # TODO: Tell everything to advance or move forward one step in time
        if self.ship.alive:
            self.ship.advance()
            self.ship.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        for bullet in self.bullets:
            bullet.advance()
            
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)
        # TODO: Check for collisions
        
    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for asteroid in self.asteroids:

            # Make sure they are both alive before checking for a collision
            if self.ship.alive and asteroid.alive:
                    too_close = self.ship.radius + asteroid.radius

                    if (abs(self.ship.center.x - asteroid.center.x) < too_close and
                                abs(self.ship.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        self.energybar.lifereduce()
                        asteroid.alive = False
                        if not self.energybar.alive:
                            self.ship.alive = False


        for bullet in self.bullets:
            for asteroid in self.asteroids:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        asteroid.alive = False
                        self.score += asteroid.hit()[1]
                        

                            
        self.cleanup_zombies()                
        
        
    def cleanup_zombies(self):
        """
        Removes any dead bullets or asteroids from the list.
        :return:
        """
        for bullet in self.bullets:
            if (abs(self.ship.center.x - bullet.center.x) > BULLET_LIFE or
                                abs(self.ship.center.y - bullet.center.y) > BULLET_LIFE):
                bullet.alive = False
            if not bullet.alive:
                self.bullets.remove(bullet)
            
                
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
                self.asteroids += asteroid.hit()[0]

        
                
    

    
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        # regenerate the ship and energybar as it is initiated.
        if arcade.key.ENTER in self.held_keys:
            if not self.ship.alive and not self.energybar.alive:
                self.energybar.__init__()
                self.ship.__init__()
            
        
        if arcade.key.LEFT in self.held_keys:
            self.ship.angle += self.ship.turn
    

        if arcade.key.RIGHT in self.held_keys:
            self.ship.angle -= self.ship.turn

        if arcade.key.UP in self.held_keys:
            self.ship.velocity.dx += math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship.velocity.dy += math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            # limit the speed of ship from -5 to 5
            if self.ship.velocity.dx > 5:
                self.ship.velocity.dx = 5
            if self.ship.velocity.dx < -5:
                self.ship.velocity.dx = -5
            if self.ship.velocity.dy > 5:
                self.ship.velocity.dy = 5
            if self.ship.velocity.dy < -5:
                self.ship.velocity.dy = -5

        if arcade.key.DOWN in self.held_keys:
            self.ship.velocity.dx -= math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship.velocity.dy -= math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            # limit the speed of ship from -5 to 5
            if self.ship.velocity.dx > 5:
                self.ship.velocity.dx = 5
            if self.ship.velocity.dx < -5:
                self.ship.velocity.dx = -5
            if self.ship.velocity.dy > 5:
                self.ship.velocity.dy = 5
            if self.ship.velocity.dy < -5:
                self.ship.velocity.dy = -5

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass



    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!      
                bullet = Bullet()
                bullet.store(self.ship)
                self.bullets.append(bullet)
                
                    
            if key == arcade.key.LEFT:
                self.held_keys.add(arcade.key.LEFT)
                
            if key == arcade.key.RIGHT:
                self.held_keys.add(arcade.key.RIGHT)
                          
            if key == arcade.key.UP:
                self.held_keys.add(arcade.key.UP)
                
            if key == arcade.key.DOWN:
                self.held_keys.add(arcade.key.DOWN)
        
        # If ship died, pressing ENTER makes ship regenerate.
        if key == arcade.key.ENTER:
            self.held_keys.add(arcade.key.ENTER)
            

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            
    def draw_game_over(self):
        """
        Print the message "Game Over" 
        """
        gameover = "Game Over"
        start_x = SCREEN_WIDTH/2 - 50
        start_y = SCREEN_HEIGHT/2
        arcade.draw_text(gameover, start_x=start_x, start_y=start_y, font_size= 20, color=arcade.color.WHITE)        
            
          


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()