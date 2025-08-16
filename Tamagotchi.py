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

#music note setup
show_music_note = False
music_note_timer = 0

#hunger
hunger_level = 0  # full is 5, empty is 0
HUNGER_INTERVAL = 60 * 1000  # 1 minute in milliseconds
last_hunger_tick = pygame.time.get_ticks()

#sleepiness
sleep_level = 1 #full 5, empty 0
SLEEP_INTERVAL = 60*1000 # 1 min
last_sleep_tick = pygame.time.get_ticks()

#positon variable
position = ()
kitty_rect = pygame.Rect(70, 70, 128, 128)  # kitty size and position for collison

#variable background
background = ()

# start pygame
pygame.init() # ewww british people "INNIT"

# Make a window
screen = pygame.display.set_mode((340, 240)) # makea da window 240x240 pixels wide
pygame.display.set_caption("Kitty Tamagotchi") #window title

# music note
music_note_img = pygame.image.load("musicnote.png").convert_alpha()
music_note_img = pygame.transform.scale(music_note_img, (96, 96))

# ballstuff
ball = pygame.image.load("ball.png").convert_alpha()
ball = pygame.transform.scale(ball, (64, 64))
rect = ball.get_rect()
rect.center = (230, 60)

velocity = pygame.math.Vector2(0, 0)

# clock to slow things down
clock = pygame.time.Clock()
FPS = 60
start_time = 0
timer_duration = 10000 # 10 seconds

# Set up animation
frame_list = []
current_frame = 0
frame_counter = 0
frames_between_changes = 6  # how many frames to wait before switching

def check_sleep_time():
    if state != State.SLEEP:
        return
    
    global start_time, sleep_level
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed >= SLEEP_INTERVAL:  # every minute (1 minute = 60 * 1000 ms)
        if sleep_level > 0:  # ensure sleep level doesn't go below 0
            sleep_level -= 1
        print(f"Sleep level decreased: {sleep_level}")
        start_time = pygame.time.get_ticks()  # reset the sleep timer


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
                global start_time, sleep_level  # reset sleep timer and sleep level
                start_time = pygame.time.get_ticks()  # start counting sleep time
                if sleep_level < 5:  # Ensure the sleep level doesn't go beyond 5
                    sleep_level += 1  # Increase sleep level when kitty goes to sleep
                print(f"Sleep level increased: {sleep_level}")
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
                reset_ball()
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
    # strat the ball bounce when we go to play
    global kitty_rect
    position = (70, 70)
    kitty_rect = pygame.Rect(position[0], position[1], 128, 128)
    reset_ball()

def ball_bounce():
    if state == State.PLAY:
        global rect
        global ball
        screen.blit(ball, rect)


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

# draw sleep bar 
def draw_sleep_bar():
    global sleep_level
    sleep_images = [
        "sleepempty.png", 
        "sleepminus4.png", 
        "sleepminus3.png", 
        "sleepminus2.png", 
        "sleepminus1.png", 
        "sleepfull.png"
    ]
    sleep_img = pygame.image.load(sleep_images[sleep_level]).convert_alpha()
    sleep_img = pygame.transform.scale(sleep_img, (120, 120))  # resize
    screen.blit(sleep_img, (220, -45))  # Adjust the position to fit well






def draw_hunger_bar():
    global hunger_level
    hunger_images = [
        "hungryempty.png",
        "hungryminus4.png",
        "hungryminus3.png",
        "hungryminus2.png",
        "hungryminus1.png",
        "hungryfull.png"
    ]
    
    hunger_img = pygame.image.load(hunger_images[hunger_level]).convert_alpha()
    hunger_img = pygame.transform.scale(hunger_img, (120, 120))  # resize
    screen.blit(hunger_img, (0, -45))  # right middle

def draw_feed_me_bubble():
    global hunger_level
    if hunger_level <= 1 and state == State.IDLE:  # only beg when idle and really hungry
        feedme_img = pygame.image.load("feedme.png").convert_alpha()
        feedme_img = pygame.transform.scale(feedme_img, (100, 60))  # size 
        bubble_x = position[0] + 80  # slightly to the right of kitty
        bubble_y = position[1] - 40  # floating above kitty
        screen.blit(feedme_img, (bubble_x, bubble_y))

def draw_sleep_me_bubble():
    global sleep_level
    if sleep_level <= 1 and state == State.IDLE:  # only beg when idle and really hungry
        sleepme_img = pygame.image.load("imsleepy.png").convert_alpha()
        sleepme_img = pygame.transform.scale(sleepme_img, (100, 70))  # size 
        bubble_x = position[0] + 100  # slightly to the right of kitty
        bubble_y = position[1] + 10  # middle of kitty
        screen.blit(sleepme_img, (bubble_x, bubble_y))



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

# reset bball
def reset_ball():
    global rect, velocity
    rect.center = (230, 60)
    velocity = pygame.math.Vector2(-5, 0)  # leftward & no vertical movement initially

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
    global kitty_rect
    kitty_rect = pygame.Rect(position[0], position[1], 128, 128)

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

    global kitty_rect
    position = (70, 70)
    kitty_rect = pygame.Rect(position[0], position[1], 128, 128)

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
    #hungrey
    global hunger_level
    if hunger_level < 5:
        hunger_level += 1
        print(f"Yum! Hunger level is now {hunger_level}")
    
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
    global frame_counter
    global background
    global last_hunger_tick
    global last_sleep_tick
    global hunger_level
    global show_music_note, music_note_timer
    global sleep_level
# game loop
    go_to_idle()

    while True: #runs until close window
        # 60 frames per second
        clock.tick(60)
        kitty_rect.topleft = position
        # quit if X is clicked
        check_events()

        check_sleep_time() # dont b caught slippin
        check_eat_time()
        # Update hunger every 60 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_hunger_tick >= HUNGER_INTERVAL:
            if hunger_level > 0:
                hunger_level -= 1
                print(f"Hungry... level now {hunger_level}")
            last_hunger_tick = current_time

#       Update sleep level every 60 seconds 
        current_time = pygame.time.get_ticks()
        if current_time - last_sleep_tick >= SLEEP_INTERVAL:
            if sleep_level > 0:
                sleep_level -= 1
                print(f"Sleepy... level now {sleep_level}")
            last_sleep_tick = current_time
        # background
        screen.fill(background)  # baby pink

        update_animation()
        ball_bounce()
        draw_play_UI()
        draw_idle_UI()
        draw_eat_UI()
        draw_sleep_UI()
        draw_hunger_bar()
        draw_feed_me_bubble()
        draw_sleep_me_bubble()
        draw_sleep_bar()

        if show_music_note:
            if pygame.time.get_ticks() - music_note_timer < 40:  # .02 second
                note_x = position[0] + 48  # centered-ish above kitty
                note_y = position[1] - 32  # floating above
                screen.blit(music_note_img, (note_x, note_y))
            else:
                show_music_note = False  # stop showing after 1 second


        if state == State.PLAY:
            if rect.colliderect(kitty_rect):
                show_music_note = True
                music_note_timer = pygame.time.get_ticks()

            velocity.y += 0.2  # gravity
            rect.x += velocity.x
            rect.y += velocity.y

            # Bounce off bottom
            if rect.bottom >= 225:
                rect.bottom = 225
                velocity.y *= -0.99  # bounce up with energy loss

            # Bounce off left wall
            if rect.left <= -15:
                rect.left = -15
                velocity.x *= -1  # reverse direction

            # Bounce off right wall
            if rect.right >= 350:
                rect.right = 350
                velocity.x *= -1

        # have to call this every loop to actually make your drawings appear
        pygame.display.update()
        #Limit the frame rate
        clock.tick(FPS)

gameloop()




