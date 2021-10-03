import turtle
import time
from random import randint
import pygame
from pygame import mixer
import os
import sys


#Create global path for one-file packaged app
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
 
    return os.path.join(base_path, relative_path)


#Start app creation
screen = turtle.Screen()
screen.bgcolor("red")
screen.title("PING PONG GAME")
screen.bgpic(resource_path("img/greenback1.gif"))

screen.setup(width = 600, height = 500)
screen.tracer()
screen.delay(0)

#Create Bg Music
mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
mixer.init()
mixer.music.load(resource_path("audio/introMusic1.mp3"))

#Create Sound Objects
pong = mixer.Sound(resource_path("audio/pong.wav"))
loss = mixer.Sound(resource_path("audio/whistle.wav"))
win = mixer.Sound(resource_path('audio/winSound.wav'))

#Function to tweak bg Music on or off
intromusicState = "start"

def introMusic(x):
	global intromusicState

	if x == "stopped":
		intromusicState = x
		mixer.music.stop()
		
	else:
		intromusicState = x
		mixer.music.play(-1)

introMusic(intromusicState)


#Border
play_top = screen.window_height() / 2 - 100 #top of the screen minus 100
play_bottom = -screen.window_height() / 2 + 100 #100 from bottom
play_left = -screen.window_width() / 2 + 50 #50 from left
play_right = screen.window_width() / 2 - 50 #50 from right

vert_middle = play_top + play_bottom #middle of screen


#Create the Border
area = turtle.Turtle()
area.hideturtle()
area.color("white")
area.pensize(3)
area.speed(0)
area.penup()
area.goto(play_left, play_top)
area.pendown()
area.goto(play_right, play_top)
area.goto(play_right, play_bottom)
area.goto(play_left, play_bottom)
area.goto(play_left, play_top)

#Write instruction on startScreen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.hideturtle()
pen.penup()
pen.goto(0, 10)
pen.write("Press ENTER Key to", align = "center", font = ("Courier", 18, "normal"))

pen1 = turtle.Turtle()
pen1.speed(0)
pen1.shape("square")
pen1.color("Blue")
pen1.hideturtle()
pen1.penup()
pen1.goto(0, -50)
pen1.write("S T A R T  G A M E", align = "center", font = ("Courier", 26, "bold"))

#player names
playernames = turtle.Turtle()
playernames.penup()
playernames.hideturtle()
playernames.color("black")


#Create Ball
ball = turtle.Turtle()
ball.speed(0)
ball.color("red")
ball.shape("circle")
ball.shapesize(0.5, 0.5)
ball.penup()
ball_radius = 10 * 0.5

#gameEnd display
penend = turtle.Turtle()
penend.speed(0)
penend.shape("square")
penend.color("Blue")
penend.hideturtle()
penend.penup()


#Create the paddles

LPaddle = turtle.Turtle()
RPaddle = turtle.Turtle()
LPaddle.penup()
LPaddle.speed(0)
RPaddle.penup()
RPaddle.speed(0)


#Paddles Shape

paddle_w_half = 10 / 2 #10 Units wide
paddle_h_half = 40 / 2 #40 Units high

paddle_shape = turtle.Shape("compound")
paddle_points = ((-paddle_h_half, -paddle_w_half), (-paddle_h_half, paddle_w_half), 
	(paddle_h_half, paddle_w_half), (paddle_h_half, -paddle_w_half))

paddle_shape.addcomponent(paddle_points, "blue")
screen.register_shape("paddle", paddle_shape)
LPaddle.shape("paddle")
RPaddle.shape("paddle")

#Move paddles to their position'
LPaddle.setx(play_left + 15)
RPaddle.setx(play_right - 15)


paddle_L_move_direction = 0   # L paddle movement direction in next frame
paddle_R_move_direction = 0   # R paddle movement direction in next frame

paddle_move_vert   = 6        # Vertical movement distance per frame

#AI Original position
L_new_y_pos = LPaddle.ycor()
LPaddle.sety(L_new_y_pos)

def paddle_is_allowed_to_move_here (new_y_pos) :
    if (play_bottom > new_y_pos - paddle_h_half) : # bottom of paddle below bottom of field
        return False
    if (new_y_pos + paddle_h_half > play_top) :    # top of paddle above top of field
        return False
    return True


def update_paddle_positions ():
    global L_new_y_pos
    
    R_new_y_pos = RPaddle.ycor() + (paddle_R_move_direction * paddle_move_vert)

    
    if paddle_is_allowed_to_move_here (R_new_y_pos):
        RPaddle.sety( R_new_y_pos )

def update_AI_paddle_pos():
    global paddle_L_move_direction, ball_move_horiz, ball_move_vert, L_new_y_pos, vert_middle, paddle_move_vert

    if ball_move_horiz == abs(ball_move_horiz):
        if L_new_y_pos < vert_middle:
            paddle_L_move_direction = 1
            L_new_y_pos = L_new_y_pos + (paddle_L_move_direction * (paddle_move_vert - 0.5))
            LPaddle.sety(L_new_y_pos)
            

        elif L_new_y_pos > vert_middle:
            paddle_L_move_direction = -1
            L_new_y_pos = L_new_y_pos + (paddle_L_move_direction * (paddle_move_vert - 0.5))
            LPaddle.sety(L_new_y_pos)
            

    elif ball_move_horiz != abs(ball_move_horiz):
        if L_new_y_pos < ball.ycor():
            paddle_L_move_direction = 1
            L_new_y_pos = L_new_y_pos + (paddle_L_move_direction * (paddle_move_vert - 0.5))
            if paddle_is_allowed_to_move_here (L_new_y_pos):
                LPaddle.sety(L_new_y_pos) 

        
        elif L_new_y_pos > ball.ycor():
            paddle_L_move_direction = -1
            L_new_y_pos = L_new_y_pos + (paddle_L_move_direction * (paddle_move_vert - 0.5))
            if paddle_is_allowed_to_move_here (L_new_y_pos):
                LPaddle.sety(L_new_y_pos)           


#Commands
def R_up():
    global paddle_R_move_direction
    paddle_R_move_direction = 1

def R_down():
    global paddle_R_move_direction
    paddle_R_move_direction = -1

def R_off():
    global paddle_R_move_direction
    paddle_R_move_direction = 0

power = False
def increaseSpeed():
	global power
	power = True

def startGame():
    global ball_move_horiz, ball_move_vert, gameStart
    gameStart = True
    pen.clear()
    pen1.clear()
    write_scores()
    playernames.goto(-600/4, 500/2 - 40)
    playernames.write("P L A Y E R  1", align = "center", font = ("Arial", 16, "normal"))
    playernames.goto(600/4, 500/2 - 40)
    playernames.write("P L A Y E R  2", align = "center", font = ("Arial", 16, "normal"))
    introMusic("stopped")
    ball.showturtle()
    time.sleep(1)
    ball.setpos(0,0)
    ball_move_horiz = 6
    ball_move_vert = 6


def closeWindow():
    screen.bye()
    


#KeyPresses
screen.onkeypress(R_up, "Up")
screen.onkeypress(R_down, "Down")
screen.onkeyrelease(R_off, "Up")
screen.onkeyrelease(R_off, "Down")
screen.onkeypress(increaseSpeed, 'space')
screen.onkeypress(startGame, 'Return')
#screen.onkeypress(closeWindow, 'Escape')
screen.listen()

#Scores
score_turtle = turtle.Turtle()
score_turtle.penup()
score_turtle.hideturtle()
score_turtle.color("white")
score_LPaddle = 0
score_RPaddle = 0


def write_scores():
    score_turtle.clear()
    score_turtle.goto(-600/4, 500/2 - 90)
    score_turtle.write(score_LPaddle, align="center", font=("Arial", 30, "bold"))
    score_turtle.goto(600/4, 500/2 - 90)
    score_turtle.write(score_RPaddle, align="center", font=("Arial", 30, "bold"))


def check_if_someone_scores() :
    global score_LPaddle, score_RPaddle, ball_move_horiz, ball_move_vert

    #Player1 (LPaddle)
    if (ball.xcor() + ball_radius) >= play_right + 20:   # right of ball at right of field
        score_LPaddle += 1
        if score_LPaddle >= 5:
            loss.play()
            write_scores()
            mixer.music.load(resource_path('audio/pongMusic.mp3'))
            win.play()
            time.sleep(4)
            introMusic('start')
            ball_move_horiz = 0
            ball_move_vert = 0
            ball.setpos(0,0)
            ball.hideturtle()
            pen1.goto(0, 50)
            pen1.write("P L A Y E R  1   W I N S", align = "center", font = ("Courier", 24, "bold"))
            pen.goto(0, -20) 
            pen.write("- press ENTER to replay -", align = "center", font = ("Comic Sans MS", 16, "bold"))
            pen.goto(0, -60)
            pen.write("- press ESC to Exit -", align = "center", font = ("Comic Sans MS", 16, "bold"))  
            score_LPaddle = 0
            score_RPaddle = 0
            resetPaddle()
        else:
            write_scores()
            loss.play()
            time.sleep(2)
            reset_ball()
            resetPaddle()
       

    #Player2 (RPaddle)
    elif play_left - 20 >= (ball.xcor() - ball_radius):  # left of ball at left of field
        score_RPaddle += 1
        if score_RPaddle >= 5:
            loss.play()
            write_scores()
            mixer.music.load(resource_path('audio/pongMusic.mp3'))
            win.play()
            time.sleep(4)  
            introMusic('start') 
            ball_move_horiz = 0
            ball_move_vert = 0
            ball.setpos(0,0)
            ball.hideturtle()
            pen1.goto(0, 50)
            pen1.write("P L A Y E R  2   W I N S", align = "center", font = ("Courier", 24, "bold"))
            pen.goto(0, -20)
            pen.write("- press ENTER to replay -", align = "center", font = ("Comic Sans MS", 16, "bold"))
            pen.goto(0, -60)
            pen.write("- press ESC to Exit -", align = "center", font = ("Comic Sans MS", 16, "bold")) 
            score_LPaddle = 0
            score_RPaddle = 0
            resetPaddle()
        else:
            write_scores()
            loss.play()
            time.sleep(2)
            reset_ball()
            resetPaddle()
   


ball_move_horiz = 0     # Horizontal movement per frame
ball_move_vert  = 0     # Vertical movement per frame

def ball_collides_with_paddle (paddle):
    x_distance = abs(paddle.xcor() - ball.xcor())
    y_distance = abs(paddle.ycor() - ball.ycor())
    overlap_horizontally = (ball_radius + paddle_w_half >= x_distance -6)  # either True or False
    overlap_vertically   = (ball_radius + paddle_h_half >= y_distance -6)  # either True or False
    return overlap_horizontally and overlap_vertically                  # so it returns either True or False

def update_ball_position ():
	global ball_move_horiz, ball_move_vert, power

	if ball.ycor() + ball_radius >= play_top :       # top of ball at or above top of field
	    ball_move_vert *= -1
	    pong.play()

	elif play_bottom >= ball.ycor() - ball_radius :  # bottom of ball at or below bottom of field
	    ball_move_vert *= -1
	    pong.play()

	if ball_collides_with_paddle(LPaddle):
	    ball_move_horiz *= -1
	    pong.play()
	    if power == True:
	    	ball_move_horiz += 3
	    	power = False 

	if ball_collides_with_paddle(RPaddle):
		ball_move_horiz *= -1
		pong.play()
		if power == True:
			ball_move_horiz -= 3
			power = False
	

	ball.setx(ball.xcor() + ball_move_horiz)
	ball.sety(ball.ycor() + ball_move_vert)


def reset_ball() :
    global ball_move_vert, ball_move_horiz

    ball.setpos(0, 0)
    speed_horiz = randint(6,8)
    speed_vert = randint(6,8)
    direction_horiz = 1
    direction_vert = 1
    if randint(0,100) > 50 :  # 50% chance of going left instead of right
        direction_horiz = -1
    if randint(0,100) > 50 :  # 50% chance of going down instead of up
        direction_vert = -1
    ball_move_horiz = direction_horiz * speed_horiz
    ball_move_vert  = direction_vert * speed_vert

def resetPaddle():
	LPaddle.sety(0)
	RPaddle.sety(0)
	time.sleep(2)


def check_if_press_esc():
	screen.onkeypress(closeWindow, 'Escape')




#WHILE LOOP / EVENT LOOP
#FRAME
def frame():
    check_if_someone_scores() 
    update_paddle_positions()
    update_AI_paddle_pos()
    update_ball_position()
    check_if_press_esc()
    screen.update()                      # show the new frame
    screen.ontimer(frame, framerate_ms)  # schedule this function to be called again a bit later


framerate_ms = 30  # Every how many milliseconds must frame function be called?
frame()

screen.mainloop()

