"""
File: pong.py
Original Author: Br. Burton
Designed to be completed by others
This program implements a simplistic version of the
classic Pong arcade game.
"""
import arcade
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 300
BALL_RADIUS = 10

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
MOVE_AMOUNT = 10

SCORE_WIN = 1
SCORE_LIMIT = 15

# Point class

class Point:
    def __init__(self):
        # set the point of x,y
        self.x = float(0)
        self.y = float(0)

# Velocity class

class Velocity:
    def __init__(self):
        # set the speed of x,y change
        self.dx = float(0)
        self.dy = float(0)
        
# Paddle class:

class Paddle:
    def __init__(self, center):
        self.center = center
    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.BLACK)
    def move_up(self):
        if self.center.y < SCREEN_HEIGHT- PADDLE_HEIGHT/2:
            self.center.y += MOVE_AMOUNT
    def move_down(self):
        if self.center.y > PADDLE_HEIGHT/2:
            self.center.y -= MOVE_AMOUNT

    
# Ball class

class Ball:
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT/2
        self.velocity.dx = random.uniform(4,8)
        self.velocity.dy = random.uniform(4,9)
  
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, BALL_RADIUS, arcade.color.GREEN)
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    def bounce_horizontal(self):
        self.velocity.dx *= -1 
    def bounce_vertical(self):
        self.velocity.dy *= -1
    def restart(self):
        center = Point()
        

     

    
class Pong(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Point
        Velocity
        Ball
        Paddle
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class,
    but should not have to if you don't want to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.ball_1 = Ball()

        
        center_1 = Point()
        center_1.x = PADDLE_WIDTH/2
        center_1.y = random.uniform(PADDLE_HEIGHT/2, SCREEN_HEIGHT - (PADDLE_HEIGHT/2))
        self.paddle_1 = Paddle(center_1)

        center_2 = Point()
        center_2.x = SCREEN_WIDTH - PADDLE_WIDTH/2 
        center_2.y = random.uniform( PADDLE_HEIGHT/2, SCREEN_HEIGHT - (PADDLE_HEIGHT/2))
        self.paddle_2 = Paddle(center_2)

        
        self.score_1 = 0
        self.score_2 = 0

        # These are used to see if the user is
        # holding down the arrow keys
        self.holding_up_paddle_1 = False       
        self.holding_down_paddle_1 = False
        self.holding_up_paddle_2 = False         
        self.holding_down_paddle_2 = False
        self.holding_start_button = False
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.ball_1.draw()
        
        self.paddle_1.draw()
        self.paddle_2.draw()
        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}:{}".format(self.score_1,self.score_2)
        start_x = SCREEN_WIDTH/2 - 50
        start_y = SCREEN_HEIGHT/2
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=20, color=arcade.color.NAVY_BLUE)
        
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """


        # Check to see if keys are being held, and then
        # take appropriate action
        self.check_keys(self.ball_1)

        # check for ball at important places
        self.check_score(self.ball_1)

       
        self.check_hit(self.ball_1)


        self.check_bounce(self.ball_1)

       
        

    def check_hit(self, ball):
        """
        Checks to see if the ball has hit the paddle
        and if so, calls its bounce method.
        :return:
        """
        too_close_x = (PADDLE_WIDTH / 2) + BALL_RADIUS
        too_close_y = (PADDLE_HEIGHT / 2) + BALL_RADIUS


        if (abs(ball.center.x - self.paddle_1.center.x) < too_close_x and
                    abs(ball.center.y - self.paddle_1.center.y) < too_close_y and
                    ball.velocity.dx < 0):
            # we are too close and moving right, this is a hit!
            ball.bounce_horizontal()
            
        if (abs(ball.center.x - self.paddle_2.center.x) < too_close_x and
                    abs(ball.center.y - self.paddle_2.center.y) < too_close_y and
                    ball.velocity.dx > 0):
            # we are too close and moving right, this is a hit!
            ball.bounce_horizontal()



    def check_score(self, ball):
        """
        Checks to see if the ball went past the paddle
        and if so, restarts it.
        """
        if ball.center.x > SCREEN_WIDTH:
            # We missed!
            self.score_1 += SCORE_WIN 
            ball.restart()
            ball.center.x = 0
            ball.center.y = self.paddle_1.center.y
           
        if ball.center.x < 0:
            self.score_2 += SCORE_WIN 
            ball.restart()
            ball.center.x = SCREEN_WIDTH 
            ball.center.y = self.paddle_2.center.y

    def check_bounce(self, ball):
        """
        Checks to see if the ball has hit the borders
        of the screen and if so, calls its bounce methods.
        """

        if ball.center.y < 0 and ball.velocity.dy < 0:
            ball.bounce_vertical()

        if ball.center.y > SCREEN_HEIGHT and ball.velocity.dy > 0:
            ball.bounce_vertical()
        

    def check_keys(self,ball):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        if self.holding_down_paddle_1:
            self.paddle_1.move_down()        
        
        if self.holding_up_paddle_1:
            self.paddle_1.move_up()
            
        if self.holding_up_paddle_2:
            self.paddle_2.move_up()

        if self.holding_down_paddle_2:
            self.paddle_2.move_down()           
        
        if self.holding_start_button:
            ball.advance()



    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.UP: 
            self.holding_up_paddle_2 = True
        
        if key == arcade.key.DOWN:
            self.holding_down_paddle_2 = True

        if key == arcade.key.W:
            self.holding_up_paddle_1 = True

        if key == arcade.key.S:
            self.holding_down_paddle_1 = True
            
        if key == arcade.key.SPACE:
            self.holding_start_button = True

           
            
            
    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.UP: 
            self.holding_up_paddle_2 = False
        
        if key == arcade.key.DOWN:
            self.holding_down_paddle_2 = False

        if key == arcade.key.W:
            self.holding_up_paddle_1 = False

        if key == arcade.key.S:
            self.holding_down_paddle_1 = False




# Creates the game and starts it going
window = Pong(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
