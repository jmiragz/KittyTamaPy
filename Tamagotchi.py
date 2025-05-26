import pygame #pygame library
import sys #lets us quit the game
from enum import Enum

# class syntax
class State(Enum):
    IDLE = 1
    SLEEP = 2
    PLAY = 3
    EAT = 4

state = State.IDLE

#positon variable
position = ()

#variable background
background = ()

# start pygame
pygame.init() # ewww british people "INNIT"

# Make a window
screen = pygame.display.set_mode((340, 240)) # makea da window 240x240 pixels wide
pygame.display.set_caption("Kitty Tamagotchi") #window title

# clock to slow things down
clock = pygame.time.Clock()
start_time = 0
timer_duration = 15000 # 15 seconds

# Set up animation
frame_list = []
current_frame = 0
frame_counter = 0
frames_between_changes = 6  # how many frames to wait before switching

def check_sleep_time():
    if state != State.SLEEP:
        return
    
    global start_time
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed >= timer_duration:
        go_to_idle()

def check_eat_time():
    if state != State.EAT:
        return
    
    global start_time
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed >= timer_duration:
        go_to_idle()


def move_kitty_right():
    global state
    global position
    if state == State.PLAY:
        position = (position[0] + 20, position[1])
    #move kitty 20 pixels riht

def move_kitty_left():
    global state
    global position
    if state == State.PLAY:
        position = (position[0] - 20, position[1])
    #move kitty 20 pixels left


def check_events():
    global state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d: # D SLEEP BUTTOn
            if state == state.IDLE:
               go_to_sleep()
            elif state == state.PLAY:
                move_kitty_right()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a: # A EAT BUTTOn / during PLAY mode left
            if state == state.IDLE:
                go_to_eat()
            elif state == state.PLAY:
                move_kitty_left()
            elif state == state.EAT:
                go_to_eat()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s: # S PLAY BUTTON / during PLAY mode right
            #kitty_play_gif()
            if state == State.SLEEP:
                go_to_idle()
            elif state == State.PLAY:
                go_to_idle()
            elif state == State.EAT:
                go_to_idle()
            else:    
                go_to_play()


# play function
def go_to_play(): #GAMING
    global state
    global frame_list
    state = State.PLAY
    print("INITIALIZE KITTY PLAY GIF")
    playkitty1 = pygame.image.load("play_kitty1.png").convert_alpha() # need alpha for transparent images
    playkitty1 = pygame.transform.scale(playkitty1, (128, 128)) #its too fcking small idek
    global background
    background = (216, 191, 216)  # purple
    frame_list = [playkitty1,playkitty1,playkitty1] 

def ball_bounce():
    if state == State.PLAY:
        ball = pygame.image.load("ball.png").convert_alpha() # need alpha for transparent images
        ball = pygame.transform.scale(ball, (64, 64)) 
        screen.blit(ball, (150, 150))

def draw_eat_UI():
    if state == State.EAT:
        eatUI = pygame.image.load("eatUI.png").convert_alpha()

        # Scale image to full width of 340 and desired height (e.g. 96)
        full_width = 340
        new_height = 250

        eatUI = pygame.transform.scale(eatUI, (full_width, new_height))

        # Blit at bottom of screen
        y_pos = 240 - new_height
        screen.blit(eatUI, (0, y_pos))


def draw_sleep_UI():
    if state == State.SLEEP:
        sleepUI = pygame.image.load("sleepUI.png").convert_alpha()

        # Scale image to full width of 340 and desired height (e.g. 96)
        full_width = 340
        new_height = 250

        sleepUI = pygame.transform.scale(sleepUI, (full_width, new_height))

        # Blit at bottom of screen
        y_pos = 240 - new_height
        screen.blit(sleepUI, (0, y_pos))

def draw_play_UI():
    if state == State.PLAY:
        playUI = pygame.image.load("playUI.png").convert_alpha()

        # Scale image to full width of 340 and desired height (e.g. 96)
        full_width = 340
        new_height = 250

        playUI = pygame.transform.scale(playUI, (full_width, new_height))

        # Blit at bottom of screen
        y_pos = 240 - new_height
        screen.blit(playUI, (0, y_pos))

def draw_idle_UI():
    if state == State.IDLE:
        idleUI = pygame.image.load("idleUI.png").convert_alpha()

        # Scale image to full width of 340 and desired height (e.g. 96)
        full_width = 340
        new_height = 250

        idleUI = pygame.transform.scale(idleUI, (full_width, new_height))

        # Blit at bottom of screen
        y_pos = 240 - new_height
        screen.blit(idleUI, (0, y_pos))

# idle function

def go_to_idle(): # I want to update to the sleep GIF
    print("INITIALIZE KITTY IDLE GIF")
    global position
    position = (70,70)
    global state
    state = State.IDLE
    kitty1 = pygame.image.load("idle_kitty1.png").convert_alpha() # need alpha for transparent images
    kitty2 = pygame.image.load("idle_kitty2.png").convert_alpha()
    kitty3 = pygame.image.load("idle_kitty3.png").convert_alpha()

    kitty1 = pygame.transform.scale(kitty1, (128, 128)) #its too fcking small idek
    kitty2 = pygame.transform.scale(kitty2, (128, 128)) #want this to be a multiple of the 32 pixels any x= 32n
    kitty3 = pygame.transform.scale(kitty3, (128, 128))
    global background
    background = (255, 192, 203)  # baby pink
    global frame_list
    frame_list = [kitty1, kitty2, kitty3] 

# Sleep Stuff
def go_to_sleep(): # I want to update to the sleep GIF
    print("INITIALIZE KITTY SLEEP GIF")
    global position
    position = (70,70)
    global background
    global state
    state = State.SLEEP
    global start_time
    start_time = pygame.time.get_ticks() # start counting
    print("Timer started!")

    background = (137, 207, 240)
    sleepy_kitty1 = pygame.image.load("sleepy_kitty1.png").convert_alpha() # need alpha for transparent images
    sleepy_kitty2 = pygame.image.load("sleepy_kitty2.png").convert_alpha()
    sleepy_kitty3 = pygame.image.load("sleepy_kitty3.png").convert_alpha()

    sleepy_kitty1 = pygame.transform.scale(sleepy_kitty1, (128, 128)) #its too fcking small idek
    sleepy_kitty2 = pygame.transform.scale(sleepy_kitty2, (128, 128)) #want this to be a multiple of the 32 pixels any x= 32n
    sleepy_kitty3 = pygame.transform.scale(sleepy_kitty3, (128, 128))
    
    global frame_list
    frame_list = [sleepy_kitty1, sleepy_kitty2, sleepy_kitty3]

def go_to_eat():
    print("INITIALIZE KITTY EAT GIF") 
    global position
    position = (70,70)
    global background
    global state
    state = State.EAT
    global start_time
    start_time = pygame.time.get_ticks() # start counting
    print("Timer started!")

    background = (193, 225, 193)
    eat_kitty1 = pygame.image.load("eat_kitty1.png").convert_alpha() # need alpha for transparent images
    eat_kitty2 = pygame.image.load("eat_kitty2.png").convert_alpha()
    eat_kitty3 = pygame.image.load("eat_kitty3.png").convert_alpha()

    eat_kitty1 = pygame.transform.scale(eat_kitty1, (128, 128)) #its too fcking small idek
    eat_kitty2 = pygame.transform.scale(eat_kitty2, (128, 128)) #want this to be a multiple of the 32 pixels any x= 32n
    eat_kitty3 = pygame.transform.scale(eat_kitty3, (128, 128))

    global frame_list
    frame_list = [eat_kitty1, eat_kitty2, eat_kitty3]
    
def update_animation(): #drawing on the screen
    global current_frame #need to talk to the variable outside the funciton
    global frame_counter
    global position
    global frame_list
    # Add 1 to the counter every frame
    frame_counter = frame_counter + 1
    # draw the current kitty frame
    screen.blit(frame_list[current_frame], position)
    # did we wait long enough to change kitty pictures?
    if frame_counter == frames_between_changes:
        # when yes reset the counter
        frame_counter = 0

        # go to the next picture
        current_frame= current_frame + 1

        # when done last picture, go back to first
        if current_frame == 3:  # because we have 3 kitty pictures
            current_frame = 0


def gameloop():
    global current_frame 
    global  frame_counter
    global background
# game loop
    go_to_idle()

    while True: #runs until close window
        # 30 frames per second
        clock.tick(30)

        # quit if X is clicked
        check_events()

        check_sleep_time() # dont b caught slippin
        check_eat_time()
        # background
        screen.fill(background)  # baby pink

        update_animation()
        ball_bounce()
        draw_play_UI()
        draw_idle_UI()
        draw_eat_UI()
        draw_sleep_UI()

        # have to call this every loop to actually make your drawings appear
        pygame.display.update()


gameloop()




