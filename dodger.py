import pygame, random, sys
from pygame.locals import *

# --- Global Volume Settings ---
MUSIC_VOLUME = 0.5 
SFX_VOLUME = 0.7
volume_changed = True # Flag pour réappliquer le volume après les changements

# --- Game Constants ---
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
NEXTBACKGROUNDIMAGE = None
BACKGROUND_ALPHA = 0
BACKGROUND_FADE_SPEED = 60
FPS = 60

PLAYERMOVERATE = 8
JUMPPOWER = 25
GRAVITY = 1
PLAYERHEIGHT = 150 # Hauteur fixe pour le scaling du joueur

BADDIEMINSIZE = 30
BADDIEMAXSIZE = 50
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8 
ADDNEWBADDIERATE = 30
SEASON_CHANGE_SCORE = 500
MAX_DIFFICULTY_SCORE = 2000 

current_baddie_min_speed = BADDIEMINSPEED
current_baddie_max_speed = BADDIEMAXSPEED

# --- Color Constants ---
DARK_BLUE = (60, 42, 83)
LIGHT_YELLOW = (254, 237, 181)
HOVER_RED = (204, 99, 104)

# --- General Utility Functions ---

def terminate():
    pygame.quit()
    sys.exit()

def playerHasHitBaddie(playerRect, baddies):
    """Checks if the player rectangle collides with any baddie."""
    for b in baddies:
        if playerRect.colliderect(b.rect): 
            return b
    return None

def drawText(text, font, surface, x, y, color = TEXTCOLOR, center=False):
    """Draws text on the surface, optionally centered."""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def scale_proportionally(image, height):
    """Scales an image to a fixed height while preserving aspect ratio."""
    width, h = image.get_size()
    scale_factor = height / h
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return pygame.transform.scale(image, (new_width, new_height))

# --- Baddie Class (From Code 1) ---
class Baddie:
    def __init__(self, size, speed, screen_width, screen_height, image, from_left=False):
        self.size = size
        self.speed = speed
        self.surface = pygame.transform.scale(image, (size, size))
        self.from_left = from_left
        
        if from_left:
            self.rect = pygame.Rect(-size, random.randint(0, screen_height - size), size, size)
            self.speed = abs(self.speed)
        else:
            self.rect = pygame.Rect(screen_width, random.randint(0, screen_height - size), size, size)
            self.speed = -abs(self.speed)
            
    def move(self, reverse_cheat, slow_cheat):
        """Moves the baddie based on its speed and active cheats."""
        move_amount = self.speed
        
        if reverse_cheat:
            move_amount = 5
        elif slow_cheat:
            move_amount = -1
        
        if not reverse_cheat and not slow_cheat:
            self.rect.move_ip(move_amount, 0)
        elif reverse_cheat:
            self.rect.move_ip(5, 0)
        elif slow_cheat:
            self.rect.move_ip(-1, 0)

# --- UI Class (From Code 1) ---
class Button:
    def __init__(self, text, x, y, font):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
    
    def draw(self, surface, color, hover_color = None, hover = False):
        if hover and hover_color is not None:
            color = hover_color
        else:
            color = color
        render = self.font.render(self.text, True, color)
        rect = render.get_rect(center = (self.x, self.y))
        surface.blit(render, rect)
        return rect

# --- Menu Functions ---

def MainMenu():
    """The game's main start screen."""
    global playerImage, playerRect
    hovered_play = hovered_quit = hovered_char = hovered_settings = False

    while True:
        pygame.mouse.set_visible(True)
        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText('Season Escape', menu_title_font, windowSurface, (WINDOWWIDTH/300), 0, LIGHT_YELLOW)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Button Definitions
        play_button = Button("Play", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.35), menu_button_font)
        char_button = Button("Select Character", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.55), menu_button_font) 
        settings_button = Button("Settings", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.75), menu_button_font) 
        quit_button = Button("Quit", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.9), menu_button_font) 

        # Draw buttons normally to get rects (color scheme from Code 1)
        rect_play_normal = play_button.draw(windowSurface, DARK_BLUE)
        rect_char_normal = char_button.draw(windowSurface, DARK_BLUE)
        rect_settings_normal = settings_button.draw(windowSurface, LIGHT_YELLOW) 
        rect_quit_normal = quit_button.draw(windowSurface, LIGHT_YELLOW) 

        # Check all hovers
        hover_play = rect_play_normal.collidepoint(mouse_x, mouse_y)
        hover_char = rect_char_normal.collidepoint(mouse_x, mouse_y)
        hover_settings = rect_settings_normal.collidepoint(mouse_x, mouse_y)
        hover_quit = rect_quit_normal.collidepoint(mouse_x, mouse_y)

        # Handle hover sound
        if (hover_play and not hovered_play) or (hover_char and not hovered_char) or \
           (hover_settings and not hovered_settings) or (hover_quit and not hovered_quit):
            hover_sound_menu.play()
        
        hovered_play = hover_play
        hovered_char = hover_char
        hovered_settings = hover_settings
        hovered_quit = hover_quit

        # Re-draw with hover colors
        play_button.draw(windowSurface, DARK_BLUE, HOVER_RED, hover_play)
        char_button.draw(windowSurface, DARK_BLUE, HOVER_RED, hover_char)
        settings_button.draw(windowSurface, LIGHT_YELLOW, HOVER_RED, hover_settings)
        quit_button.draw(windowSurface, LIGHT_YELLOW, HOVER_RED, hover_quit)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click_sound_menu.play()
                if rect_play_normal.collidepoint(mouse_x, mouse_y):
                    return # Start game
                if rect_char_normal.collidepoint(mouse_x, mouse_y):
                    CharacterSelectMenu()
                if rect_settings_normal.collidepoint(mouse_x, mouse_y):
                    SettingsMenu()
                if rect_quit_normal.collidepoint(mouse_x, mouse_y):
                    terminate()

        pygame.display.update()
        mainClock.tick(60)

def CharacterSelectMenu():
    global playerImage, playerRect, player_data
    
    # Character dictionary (name, image set name)
    CHAR_SETS = {
        "Ninja": "Ninja",
        "Adventurer": "Adventurer", 
        "Knight": "Knight", 
    }
    
    char_names = list(CHAR_SETS.keys())
    current_char_index = char_names.index(player_data['name'])
    
    back_button = Button("Back", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.9), font)
    
    while True:
        pygame.mouse.set_visible(True)
        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText('SELECT YOUR CHARACTER', menu_button_font, windowSurface, WINDOWWIDTH//2, int(WINDOWHEIGHT*0.1), LIGHT_YELLOW, center=True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Navigation buttons (Arrows)
        prev_button = Button("<", WINDOWWIDTH//4, WINDOWHEIGHT//2, menu_button_font)
        next_button = Button(">", 3 * WINDOWWIDTH//4, WINDOWHEIGHT//2, menu_button_font)

        rect_prev = prev_button.draw(windowSurface, (255, 255, 255))
        rect_next = next_button.draw(windowSurface, (255, 255, 255))
        rect_back = back_button.draw(windowSurface, LIGHT_YELLOW)
        
        # Display current character image and name
        current_name = char_names[current_char_index]
        # Use the 'stoic' image for the preview
        current_image = player_image_sets[current_name]["stoic"]
        
        image_rect = current_image.get_rect(center=(WINDOWWIDTH//2, WINDOWHEIGHT//2))
        windowSurface.blit(current_image, image_rect)
        
        drawText(current_name, menu_button_font, windowSurface, WINDOWWIDTH//2, int(WINDOWHEIGHT*0.7), (255, 255, 255), center=True)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click_sound_menu.play()
                if rect_back.collidepoint(mouse_x, mouse_y):
                    # Set the chosen character before returning
                    playerImage = player_image_sets[current_name]["stoic"]
                    playerRect = playerImage.get_rect()
                    player_data['name'] = current_name
                    # Note: player_data['image_path'] is no longer strictly necessary but kept for context.
                    return # Back to Main Menu
                
                # Navigation logic
                if rect_prev.collidepoint(mouse_x, mouse_y):
                    current_char_index = (current_char_index - 1) % len(char_names)
                if rect_next.collidepoint(mouse_x, mouse_y):
                    current_char_index = (current_char_index + 1) % len(char_names)
        
        pygame.display.update()
        mainClock.tick(60)

def SettingsMenu():
    global MUSIC_VOLUME, SFX_VOLUME, volume_changed

    slider_width = WINDOWWIDTH // 3
    slider_height = 20
    slider_x = WINDOWWIDTH // 2 - slider_width // 2
    
    music_y = int(WINDOWHEIGHT * 0.4)
    sfx_y = int(WINDOWHEIGHT * 0.6)

    back_button = Button("Back", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.9), font)
    
    is_dragging_music = False
    is_dragging_sfx = False

    while True:
        pygame.mouse.set_visible(True)
        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText('SETTINGS', menu_button_font, windowSurface, WINDOWWIDTH//2, int(WINDOWHEIGHT*0.1), LIGHT_YELLOW, center=True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect_back = back_button.draw(windowSurface, LIGHT_YELLOW)

        # Draw Music Slider
        drawText("Music Volume:", font, windowSurface, slider_x, music_y - 50, (255, 255, 255))
        pygame.draw.rect(windowSurface, (50, 50, 50), (slider_x, music_y, slider_width, slider_height), 0, 5)
        music_knob_x = slider_x + int(MUSIC_VOLUME * slider_width)
        music_knob_rect = pygame.Rect(music_knob_x - 10, music_y - 5, 20, 30)
        pygame.draw.rect(windowSurface, HOVER_RED, music_knob_rect, 0, 5)

        # Draw SFX Slider
        drawText("SFX Volume:", font, windowSurface, slider_x, sfx_y - 50, (255, 255, 255))
        pygame.draw.rect(windowSurface, (50, 50, 50), (slider_x, sfx_y, slider_width, slider_height), 0, 5)
        sfx_knob_x = slider_x + int(SFX_VOLUME * slider_width)
        sfx_knob_rect = pygame.Rect(sfx_knob_x - 10, sfx_y - 5, 20, 30)
        pygame.draw.rect(windowSurface, HOVER_RED, sfx_knob_rect, 0, 5)

        # Draw percentage labels
        drawText(f"{int(MUSIC_VOLUME * 100)}%", font, windowSurface, slider_x + slider_width + 20, music_y, (255, 255, 255))
        drawText(f"{int(SFX_VOLUME * 100)}%", font, windowSurface, slider_x + slider_width + 20, sfx_y, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if rect_back.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    volume_changed = True
                    return
                
                if music_knob_rect.collidepoint(mouse_x, mouse_y) or (slider_x <= mouse_x <= slider_x + slider_width and music_y <= mouse_y <= music_y + slider_height):
                    is_dragging_music = True
                    click_sound_menu.play()
                elif sfx_knob_rect.collidepoint(mouse_x, mouse_y) or (slider_x <= mouse_x <= slider_x + slider_width and sfx_y <= mouse_y <= sfx_y + slider_height):
                    is_dragging_sfx = True
                    click_sound_menu.play()
                    
            if event.type == MOUSEBUTTONUP and event.button == 1:
                is_dragging_music = False
                is_dragging_sfx = False
                
            if event.type == MOUSEMOTION:
                if is_dragging_music:
                    new_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                    MUSIC_VOLUME = (new_x - slider_x) / slider_width
                    pygame.mixer.music.set_volume(MUSIC_VOLUME)

                if is_dragging_sfx:
                    new_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                    SFX_VOLUME = (new_x - slider_x) / slider_width
                    # Apply SFX volume immediately for preview
                    hit_sound.set_volume(SFX_VOLUME)
                    click_sound_menu.set_volume(SFX_VOLUME)
                    hover_sound_menu.set_volume(SFX_VOLUME)
                    gameOverSound.set_volume(SFX_VOLUME)
                    
        pygame.display.update()
        mainClock.tick(60)

def PauseMenu():
    global volume_changed
    pygame.mouse.set_visible(True)
    pygame.mixer.music.pause()

    pause_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
    pause_surface.fill((0, 0, 0, 150))
    windowSurface.blit(pause_surface, (0, 0))

    drawText('PAUSED', menu_title_font, windowSurface, WINDOWWIDTH/2, 100, (255, 255, 255), center=True)

    resume_button = Button("Resume", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.45), menu_button_font)
    restart_button = Button("Restart", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.60), menu_button_font)
    return_menu_button = Button("Return to Menu", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.75), menu_button_font) 
    quit_button = Button("Quit", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.90), menu_button_font)

    hovered_resume = hovered_restart = hovered_return = hovered_quit = False

    while True:
        windowSurface.blit(pause_surface, (0, 0))
        drawText('PAUSED', menu_title_font, windowSurface, WINDOWWIDTH/2, 100, (255, 255, 255), center=True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rect_resume = resume_button.draw(windowSurface, (255, 255, 255), HOVER_RED, False)
        rect_restart = restart_button.draw(windowSurface, (255, 255, 255), HOVER_RED, False)
        rect_return = return_menu_button.draw(windowSurface, (255, 255, 255), HOVER_RED, False)
        rect_quit = quit_button.draw(windowSurface, (255, 255, 255), HOVER_RED, False)

        hover_resume = rect_resume.collidepoint(mouse_x, mouse_y)
        hover_restart = rect_restart.collidepoint(mouse_x, mouse_y)
        hover_return = rect_return.collidepoint(mouse_x, mouse_y)
        hover_quit = rect_quit.collidepoint(mouse_x, mouse_y)
        
        if (hover_resume and not hovered_resume) or (hover_restart and not hovered_restart) or \
           (hover_return and not hovered_return) or (hover_quit and not hovered_quit):
            hover_sound_menu.play()
        
        hovered_resume = hover_resume
        hovered_restart = hover_restart
        hovered_return = hover_return
        hovered_quit = hover_quit

        resume_button.draw(windowSurface, (255, 255, 255), HOVER_RED, hover_resume)
        restart_button.draw(windowSurface, (255, 255, 255), HOVER_RED, hover_restart)
        return_menu_button.draw(windowSurface, (255, 255, 255), HOVER_RED, hover_return)
        quit_button.draw(windowSurface, (255, 255, 255), HOVER_RED, hover_quit)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                click_sound_menu.play()
                pygame.mouse.set_visible(False)
                pygame.mixer.music.unpause()
                return "resume"

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click_sound_menu.play()
                if rect_resume.collidepoint(mouse_x, mouse_y):
                    pygame.mouse.set_visible(False)
                    pygame.mixer.music.unpause()
                    return "resume"
                if rect_restart.collidepoint(mouse_x, mouse_y):
                    return "restart"
                if rect_return.collidepoint(mouse_x, mouse_y):
                    MainMenu()
                    return "restart"
                if rect_quit.collidepoint(mouse_x, mouse_y):
                    terminate()

        pygame.display.update()
        mainClock.tick(FPS)

def GameOverScreen(current_topScore):
    """Displays the Game Over screen and handles input for restart or menu."""
    pygame.mixer.music.stop()
    gameOverSound.play()

    while True:
        pygame.mouse.set_visible(True)
        windowSurface.blit(GAMEOVER_BACKGROUND, (0, 0))
        
        drawText('GAME OVER', menu_title_font, windowSurface, WINDOWWIDTH/2, 100, (0, 0, 0), center=True) 
        
        return_button = Button("Return to Menu", WINDOWWIDTH//2, int(WINDOWHEIGHT/1.5), menu_button_font)
        
        drawText('Press any key or click to play again.', font, windowSurface, WINDOWWIDTH/2, int(WINDOWHEIGHT / 2), color = (255, 255, 255), center=True)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect_return = return_button.draw(windowSurface, LIGHT_YELLOW, HOVER_RED, False)
        hover_return = rect_return.collidepoint(mouse_x, mouse_y)
        return_button.draw(windowSurface, LIGHT_YELLOW, HOVER_RED, hover_return)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == KEYDOWN:
                gameOverSound.stop()
                return # Restart game
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                gameOverSound.stop()
                if rect_return.collidepoint(mouse_x, mouse_y):
                    MainMenu() # Go to Main Menu
                return # Restart game loop (will return to MainMenu if needed)

        mainClock.tick(FPS)

# --- Initialization & Setup ---
pygame.init()

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
pygame.display.set_caption('Season Escape')

# Load Backgrounds
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load("back_menu.png"), (WINDOWWIDTH, WINDOWHEIGHT))
GAMEOVER_BACKGROUND = pygame.transform.scale(pygame.image.load("back_gameover.png"), (WINDOWWIDTH, WINDOWHEIGHT))
backgrounds = {
    "Spring": pygame.transform.scale(pygame.image.load("back_printemps.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "Summer": pygame.transform.scale(pygame.image.load("back_été.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "Autumn": pygame.transform.scale(pygame.image.load("back_automne.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "Winter": pygame.transform.scale(pygame.image.load("back_hiver.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
}
BACKGROUNDIMAGE = backgrounds["Spring"] 

# Red filter for hit feedback
red_filter = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
red_filter.set_alpha(120)
red_filter.fill((255, 0, 0))

# Fonts
font = pygame.font.Font("8bit_font.ttf", 48)
menu_title_font = pygame.font.Font("8bit_font.ttf", 300)
menu_button_font = pygame.font.Font("8bit_font.ttf", 150)

# Sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
hit_sound = pygame.mixer.Sound('hit.mp3')
click_sound_menu = pygame.mixer.Sound('click_menu.mp3')
hover_sound_menu = pygame.mixer.Sound('hover_sound.mp3')

# Apply initial volume settings
pygame.mixer.music.set_volume(MUSIC_VOLUME)
hit_sound.set_volume(SFX_VOLUME)
click_sound_menu.set_volume(SFX_VOLUME)
hover_sound_menu.set_volume(SFX_VOLUME)
gameOverSound.set_volume(SFX_VOLUME)

# --- Character Images Setup (MERGED) ---
# Use the comprehensive image sets from Code 2
player_image_sets = {
    "Ninja": {
        "run_right" : scale_proportionally(pygame.image.load('ninja_run_right.png'), PLAYERHEIGHT),
        "run_left" : scale_proportionally(pygame.image.load('ninja_run_left.png'), PLAYERHEIGHT),
        "jump_right" : scale_proportionally(pygame.image.load('ninja_jump_right.png'), PLAYERHEIGHT),
        "jump_left" : scale_proportionally(pygame.image.load('ninja_jump_left.png'), PLAYERHEIGHT),
        "stoic": scale_proportionally(pygame.image.load('ninja_stoic.png'), PLAYERHEIGHT)
    },
    "Adventurer": {
        "run_right" : scale_proportionally(pygame.image.load('adventurer_run_right.png'), PLAYERHEIGHT),
        "run_left" : scale_proportionally(pygame.image.load('adventurer_run_left.png'), PLAYERHEIGHT),
        "jump_right" : scale_proportionally(pygame.image.load('adventurer_jump_right.png'), PLAYERHEIGHT),
        "jump_left" : scale_proportionally(pygame.image.load('adventurer_jump_left.png'), PLAYERHEIGHT),
        "stoic": scale_proportionally(pygame.image.load('adventurer_stoic.png'), PLAYERHEIGHT)
    },
    "Knight": {
        "run_right" : scale_proportionally(pygame.image.load('knight_run_right.png'), PLAYERHEIGHT),
        "run_left" : scale_proportionally(pygame.image.load('knight_run_left.png'), PLAYERHEIGHT),
        "jump_right" : scale_proportionally(pygame.image.load('knight_jump_right.png'), PLAYERHEIGHT),
        "jump_left" : scale_proportionally(pygame.image.load('knight_jump_left.png'), PLAYERHEIGHT),
        "stoic": scale_proportionally(pygame.image.load('knight_stoic.png'), PLAYERHEIGHT)
    }
}
player_data = {'name': 'Ninja', 'image_set': player_image_sets['Ninja']} # Track active set
playerImage = player_data['image_set']['stoic']
playerRect = playerImage.get_rect()

# Baddie images dictionary by season (placeholders)
baddie_images = {
    "Spring": pygame.image.load('baddie.png'), 
    "Summer": pygame.image.load('baddie.png'), 
    "Autumn": pygame.image.load('baddie.png'), 
    "Winter": pygame.image.load('baddie.png'), 
}
current_season = "Spring"
current_baddie_image = baddie_images[current_season]

# --- Main Game Loop Execution ---

MainMenu()

topScore = 0
last_direction = "right" # To determine jump image direction

while True:
    # Reset game state
    pygame.mouse.set_visible(False)
    player_data['image_set'] = player_image_sets[player_data['name']] # Set the correct image set
    playerImage = player_data['image_set']['stoic'] # Reset player image to stoic
    playerRect = playerImage.get_rect() # Recalculate rect based on chosen image dimensions
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - PLAYERHEIGHT) # Start at the bottom

    PLAYERYSPEED = 0
    JUMPSLEFT = 2
    on_ground = False
    
    baddies = [] 
    baddieAddCounter = 0
    score = 0
    lives = 3
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    
    # Apply volume settings and start music
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1, 0.0)

    # Reset season and difficulty
    current_season = "Spring"
    BACKGROUNDIMAGE = backgrounds[current_season]
    current_baddie_image = baddie_images[current_season]
    current_baddie_min_speed = BADDIEMINSPEED
    current_baddie_max_speed = BADDIEMAXSPEED

    is_playing = True
    
    while is_playing:
        score += 1
        
        # --- Difficulty increase (Baddie Speed) ---
        if score % 100 == 0 and score <= MAX_DIFFICULTY_SCORE:
            current_baddie_min_speed += 0.1
            current_baddie_max_speed += 0.1

        # --- Background change (season) based on score ---
        new_season = None
        if score == SEASON_CHANGE_SCORE and current_season != "Summer" and NEXTBACKGROUNDIMAGE is None:
            new_season = "Summer"
        elif score == 2 * SEASON_CHANGE_SCORE and current_season != "Autumn" and NEXTBACKGROUNDIMAGE is None:
            new_season = "Autumn"
        elif score == 3 * SEASON_CHANGE_SCORE and current_season != "Winter" and NEXTBACKGROUNDIMAGE is None:
            new_season = "Winter"

        if new_season:
            NEXTBACKGROUNDIMAGE = backgrounds[new_season]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0
            current_season = new_season
            current_baddie_image = baddie_images[current_season]

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause_action = PauseMenu()
                    if pause_action == "restart":
                        is_playing = False
                        break
                    elif pause_action == "resume":
                        pygame.mouse.set_visible(False)

                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True

                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                    last_direction = "left"
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                    last_direction = "right"

                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 3
                    
                if event.key == K_SPACE and JUMPSLEFT > 0:
                    PLAYERYSPEED = -JUMPPOWER
                    JUMPSLEFT -= 1
                    on_ground = False

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                if event.key == K_x:
                    slowCheat = False
                
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 1

        # --- Player Animation Logic (MERGED from Code 2) ---
        if not on_ground:
            if last_direction == "left":
                playerImage = player_data['image_set']["jump_left"]
            else:
                playerImage = player_data['image_set']["jump_right"]
        else:
            if moveLeft:
                playerImage = player_data['image_set']["run_left"]
            elif moveRight:
                playerImage = player_data['image_set']["run_right"]
            else:
                playerImage = player_data['image_set']["stoic"]
                
        # --- Game Logic ---
        
        # Add new baddies.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            baddieSpeed = random.randint(int(current_baddie_min_speed), int(current_baddie_max_speed))
            
            from_left = random.random() < 0.25 
            
            newBaddie = Baddie(
                size=baddieSize, 
                speed=baddieSpeed, 
                screen_width=WINDOWWIDTH, 
                screen_height=WINDOWHEIGHT, 
                image=current_baddie_image,
                from_left=from_left
            )
            baddies.append(newBaddie)

        # Apply gravity to the player.
        PLAYERYSPEED += GRAVITY
        playerRect.y += PLAYERYSPEED

        # Player collision with floor
        if playerRect.bottom >= WINDOWHEIGHT:
            playerRect.bottom = WINDOWHEIGHT
            PLAYERYSPEED = 0
            on_ground = True
            JUMPSLEFT = 2
        else:
            on_ground = False

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        # Move the baddies
        for b in baddies:
            b.move(reverseCheat, slowCheat)

        # Delete baddies that have gone past the screen boundaries.
        for b in baddies[:]:
            if b.rect.right < 0 or b.rect.left > WINDOWWIDTH:
                baddies.remove(b)

        # --- Drawing ---
        
        # Draw the background with fade effect
        if NEXTBACKGROUNDIMAGE:
            windowSurface.blit(BACKGROUNDIMAGE, (0, 0))

            fade_surface.set_alpha(BACKGROUND_ALPHA)
            windowSurface.blit(fade_surface, (0, 0))

            BACKGROUND_ALPHA += BACKGROUND_FADE_SPEED
            if BACKGROUND_ALPHA >= 255:
                BACKGROUNDIMAGE = NEXTBACKGROUNDIMAGE
                NEXTBACKGROUNDIMAGE = None
                BACKGROUND_ALPHA = 0
        else:
            windowSurface.blit(BACKGROUNDIMAGE, (0, 0))

        # Draw the HUD
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Lives: %s' % (lives), font, windowSurface, 10, 80)
        drawText('Season: %s' % (current_season), font, windowSurface, WINDOWWIDTH - 250, 0)

        # Draw the player
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b.surface, b.rect) 

        pygame.display.update()

        # Check for collision
        hit_baddie = playerHasHitBaddie(playerRect, baddies)
        if hit_baddie is not None:
            lives -= 1
            baddies.remove(hit_baddie)
            hit_sound.play()
        
            # Red flash on hit
            windowSurface.blit(red_filter, (0, 0))
            pygame.display.update()
            pygame.time.wait(50)

            if lives <= 0:
                if score > topScore:
                    topScore = score
                is_playing = False

        mainClock.tick(FPS)

    # --- Game Over Screen Handling ---
    if lives <= 0:
        GameOverScreen(topScore)
    # If lives > 0, the game was exited via Pause Menu (Return to Menu) and restarts automatically.