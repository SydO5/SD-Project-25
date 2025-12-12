import pygame, random, sys
from pygame.locals import *

    # Set up constants.
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
BACKGROUNDIMAGE = pygame.image.load("back_printemps.png")
NEXTBACKGROUNDIMAGE = None
BACKGROUND_ALPHA = 0
BACKGROUND_FADE_SPEED = 10
FPS = 60

MUSICVOLUME = 0.5
SFXVOLUME = 0.5
volume_changed = False

PLAYERMOVERATE = 8
JUMPPOWER = 25
GRAVITY = 1
PLAYERHEIGHT = 200

BADDIEMINSIZE = 50
BADDIEMAXSIZE = 100
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 50

ADDNEWCOINRATE = 200
ADDNEWHOURGLASSRATE = 800

PLATFORMMINWIDTH = 100
PLATFORMMAXWIDTH = 250
PLATFORMHEIGHT = 60
ADDNEWPLATFORMRATE = 90
PLATFORMSPEED = 6
PLATFORM_HITBOX_OFFSET_Y = 23

FLOOR_HITBOX_OFFSET_Y = 45
FLOORHEIGHT = 100

    # Set up functions.
# Exit the game.
def terminate():
    pygame.quit()
    sys.exit()

# Wait for the player to press enter or escape key.
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    click_sound_menu.play()
                    return "menu"
                if event.key == K_RETURN:
                    click_sound_menu.play()
                    return "play"

# Check if the player has hit a baddie.
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b["rect"]):
            return b
    return None

# Check if the player has collected a coin.
def playerHasCollectedCoin(playerRect, coins):
    for c in coins:
        if playerRect.colliderect(c["rect"]):
            return c
    return None

# Check if the player has collected an hourglass.
def playerHasCollectedHourglass(playerRect, hourglasses):
    for h in hourglasses:
        if playerRect.colliderect(h["rect"]):
            return h
    return None

# Check if baddie has hit a platform.
def baddieHasHitPlatform(platforms, baddies):
    for b in baddies:
        for p in platforms:
            if p["hitbox"].colliderect(b["rect"]):
                return b
    return None

# Draw a text on the surface.
def drawText(text, font, surface, x, y, color = TEXTCOLOR, center = False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Scale player image proportionally to a given height.
def scale_proportionally(image, PLAYERHEIGHT):
    width, height = image.get_size()
    scale_factor = PLAYERHEIGHT / height
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return pygame.transform.scale(image, (new_width, new_height))

# Load and scale floor image proportionally to a given height.
def load_and_scale_floor(image_name):
    img = pygame.image.load(image_name).convert_alpha()
    # new width based on aspect ratio
    aspect_ratio = img.get_width() / img.get_height()
    new_width = int(FLOORHEIGHT * aspect_ratio)
    return pygame.transform.scale(img, (new_width, FLOORHEIGHT))

# Play the music of the menu.
def playMenuMusic():
    pygame.mixer.music.load("music_menu.wav")
    pygame.mixer.music.set_volume(MUSICVOLUME)
    pygame.mixer.music.play(-1, 0.0, fade_ms = 1000)
def stopMenuMusic():
    pygame.mixer.music.stop()

# Set up button class.
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

# Create main menu with play, character selection, settings and quit buttons.
def MainMenu():
    playMenuMusic()
    hovered_play = False
    hovered_select = False
    hovered_settings = False
    hovered_quit = False

    while True:
        pygame.mouse.set_visible(True)

        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText("Season Escape", menu_title_font, windowSurface, (WINDOWWIDTH/2), 125, (60,42,83), center = True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        play_button = Button("Play", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.45), menu_button_font)
        select_button = Button("Select Character", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.60), menu_button_font)
        settings_button = Button("Sound Settings", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.75), menu_button_font)
        quit_button = Button("Quit", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.9), menu_button_font)
        
        rect_play_normal = play_button.draw(windowSurface, (60,42,83))
        rect_select_normal = select_button.draw(windowSurface, (254, 237, 181))
        rect_settings_normal = settings_button.draw(windowSurface, (254, 237, 181))
        rect_quit_normal = quit_button.draw(windowSurface, (254, 237, 181))

        hover_play = rect_play_normal.collidepoint(mouse_x, mouse_y)
        hover_select = rect_select_normal.collidepoint(mouse_x, mouse_y)
        hover_settings = rect_settings_normal.collidepoint(mouse_x, mouse_y)
        hover_quit = rect_quit_normal.collidepoint(mouse_x, mouse_y)

        if hover_play and not hovered_play:
            hover_sound_menu.play()
        if hover_select and not hovered_select:
            hover_sound_menu.play()
        if hover_settings and not hovered_settings:
            hover_sound_menu.play()
        if hover_quit and not hovered_quit:
            hover_sound_menu.play()
        
        hovered_play = hover_play
        hovered_select = hover_select
        hovered_settings = hover_settings
        hovered_quit = hover_quit

        rect_play = play_button.draw(windowSurface, (60,42,83), (204,99,104), hover_play)
        rect_select = select_button.draw(windowSurface, (254, 237, 181), (252,250,212), hover_select)
        rect_settings = settings_button.draw(windowSurface, (254, 237, 181), (252,250,212), hover_settings)
        rect_quit = quit_button.draw(windowSurface, (254, 237, 181), (204,99,104), hover_quit)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if rect_play.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    pygame.mouse.set_visible(False)
                    return
                if rect_select.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    CharacterSelectionMenu()
                if rect_settings.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    SettingsMenu()
                if rect_quit.collidepoint(mouse_x, mouse_y):
                    terminate()

        pygame.display.update()
        mainClock.tick(60)

# Create character selection menu.
def CharacterSelectionMenu():
    global playerImages, playerImage, playerRect
    hovered_back = False
    
    all_characters_images = {
        "Ninja": NinjaImages,
        "Adventurer": AdventurerImages,
        "Knight": KnightImages
    }
    characters = list(all_characters_images.keys())

    space_between = WINDOWWIDTH // (len(characters) + 1)
    y_position = WINDOWHEIGHT // 1.9

    characters_buttons = {}
    for i, name in enumerate(characters):
        img = all_characters_images[name]["stoic"]
        rect = img.get_rect(center=((i+1)*space_between, y_position))
        characters_buttons[name] = {"image": img, "rect": rect, "selected": False}
    
    while True:
        pygame.mouse.set_visible(True)
        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText("Select your Destiny", character_select_title_font, windowSurface, (WINDOWWIDTH/2), 125, (60,42,83), center = True)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for name, data in characters_buttons.items():
            img = data["image"]
            rect = data["rect"]

            scale = 2
            scaled_img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            scaled_rect = scaled_img.get_rect(center=rect.center)
            data["scaled_rect"] = scaled_rect

            text_color = (254, 237, 181)
            if data["selected"]:
                text_color = (204, 99, 104)
            scaled_text_surface = character_select_font.render(name, True, text_color)
            text_rect = scaled_text_surface.get_rect(center=(scaled_rect.centerx, scaled_rect.bottom + 40))
            data["text_rect"] = text_rect

            hovered = rect.collidepoint(mouse_x, mouse_y) or text_rect.collidepoint(mouse_x, mouse_y)

            if hovered and not data.get("hovered", False):
                hover_sound_menu.play()
            data["hovered"] = hovered
        
            if hovered:
                scale = 2.2
            else:
                scale = 2
        
            scaled_img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            scaled_rect = scaled_img.get_rect(center=rect.center)
            windowSurface.blit(scaled_img, scaled_rect)
            data["scaled_rect"] = scaled_rect

            if data["selected"]:
                color = (204,99,104)
            elif hovered:
                color = (252,250,212)
            else:
                color = (254, 237, 181)
        
            drawText(name, character_select_font, windowSurface, scaled_rect.centerx, scaled_rect.bottom + 40, color, center = True)
            data["text_rect"] = character_select_font.render(name, True, color).get_rect(center=(scaled_rect.centerx, scaled_rect.bottom + 40))

        back_button = Button("Back", 125, WINDOWHEIGHT - 60, character_select_font)
        back_rect = back_button.draw(windowSurface, (254, 237, 181))
        hover_back = back_rect.collidepoint(mouse_x, mouse_y)
        if hover_back and not hovered_back:
            hover_sound_menu.play()
        hovered_back = hover_back
        back_rect = back_button.draw(windowSurface, (254, 237, 181), (204,99,104), hover_back)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    click_sound_menu.play()
                    return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    return
                for name, data in characters_buttons.items():
                    if data["scaled_rect"].collidepoint(mouse_x, mouse_y) or data["text_rect"].collidepoint(mouse_x, mouse_y):
                        for n in characters_buttons:
                            characters_buttons[n]["selected"] = (n == name)
                        playerImages = all_characters_images[name]
                        playerImage = playerImages["stoic"]
                        playerRect = playerImage.get_rect()
                        click_sound_menu.play()
                        break
        pygame.display.update()
        mainClock.tick(60)

# Create sound settings menu.
def SettingsMenu():
    global MUSICVOLUME, SFXVOLUME, volume_changed
    hovered_back = False

    slider_width = WINDOWWIDTH // 3
    slider_height = 20
    slider_x = WINDOWWIDTH // 2 - slider_width // 2
    
    music_y = int(WINDOWHEIGHT * 0.4)
    sfx_y = int(WINDOWHEIGHT * 0.6)
    
    dragging_music = False
    dragging_sfx = False

    while True:
        pygame.mouse.set_visible(True)
        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText("Sound Settings", character_select_title_font, windowSurface, (WINDOWWIDTH/2), 125, (60,42,83), center = True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw Music Slider
        drawText("Music Volume:", font, windowSurface, slider_x, music_y - 50, (60,42,83))
        pygame.draw.rect(windowSurface, (60,42,83), (slider_x, music_y, slider_width, slider_height), 0, 5)
        music_knob_x = slider_x + int(MUSICVOLUME * slider_width)
        music_knob_rect = pygame.Rect(music_knob_x - 10, music_y - 5, 20, 30)
        pygame.draw.rect(windowSurface, (204, 99, 104), music_knob_rect, 0, 5)

        # Draw SFX Slider
        drawText("SFX Volume:", font, windowSurface, slider_x, sfx_y - 50, (60,42,83))
        pygame.draw.rect(windowSurface, (60,42,83), (slider_x, sfx_y, slider_width, slider_height), 0, 5)
        sfx_knob_x = slider_x + int(SFXVOLUME * slider_width)
        sfx_knob_rect = pygame.Rect(sfx_knob_x - 10, sfx_y - 5, 20, 30)
        pygame.draw.rect(windowSurface, (204, 99, 104), sfx_knob_rect, 0, 5)

        # Draw percentage labels
        drawText(f"{int(MUSICVOLUME * 100)}%", font, windowSurface, slider_x + slider_width + 20, music_y - 18, (60,42,83))
        drawText(f"{int(SFXVOLUME * 100)}%", font, windowSurface, slider_x + slider_width + 20, sfx_y - 18, (60,42,83))

        back_button = Button("Back", 125, WINDOWHEIGHT - 60, character_select_font)
        back_rect = back_button.draw(windowSurface, (254, 237, 181))
        hover_back = back_rect.collidepoint(mouse_x, mouse_y)
        if hover_back and not hovered_back:
            hover_sound_menu.play()
        hovered_back = hover_back
        back_rect = back_button.draw(windowSurface, (254, 237, 181), (204,99,104), hover_back)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    click_sound_menu.play()
                    return

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    volume_changed = True
                    return
                
                if music_knob_rect.collidepoint(mouse_x, mouse_y) or (slider_x <= mouse_x <= slider_x + slider_width and music_y <= mouse_y <= music_y + slider_height):
                    dragging_music = True
                    click_sound_menu.play()
                elif sfx_knob_rect.collidepoint(mouse_x, mouse_y) or (slider_x <= mouse_x <= slider_x + slider_width and sfx_y <= mouse_y <= sfx_y + slider_height):
                    dragging_sfx = True
                    click_sound_menu.play()
                    
            if event.type == MOUSEBUTTONUP and event.button == 1:
                dragging_music = False
                dragging_sfx = False
                
            if event.type == MOUSEMOTION:
                if dragging_music:
                    new_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                    MUSICVOLUME = (new_x - slider_x) / slider_width
                    pygame.mixer.music.set_volume(MUSICVOLUME)

                if dragging_sfx:
                    new_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                    SFXVOLUME = (new_x - slider_x) / slider_width

                    hit_sound.set_volume(SFXVOLUME)
                    click_sound_menu.set_volume(SFXVOLUME)
                    hover_sound_menu.set_volume(SFXVOLUME)
                    gameOverSound.set_volume(SFXVOLUME)
                    
        pygame.display.update()
        mainClock.tick(60)

# Set up pygame, the window, and the mouse cursor.
pygame.init()

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
pygame.display.set_caption("Dodger")

# Set up the background image for the menu.
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load("back_menu.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT))

#Set up the background image for gameover.
GAMEOVER_BACKGROUND = pygame.transform.scale(pygame.image.load("back_gameover.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT))

# Scale the background image to fit the screen.
BACKGROUNDIMAGE = pygame.transform.scale(BACKGROUNDIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

#Make dictionnary with backgrounds adjusted to screen size
backgrounds = {
    "Spring": pygame.transform.scale(pygame.image.load("back_printemps.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    "Summer": pygame.transform.scale(pygame.image.load("back_été.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    "Autumn": pygame.transform.scale(pygame.image.load("back_automne.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    "Winter": pygame.transform.scale(pygame.image.load("back_hiver.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
}

seasons = ["Spring", "Summer", "Autumn", "Winter"]
season_index = 0
current_season = seasons[season_index]

# Create red filter when the player hit a baddie.
red_filter = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
red_filter.set_alpha(120)
red_filter.fill((255, 0, 0))

# Set up the fonts.
font = pygame.font.Font("8bit_font.ttf", 48)
menu_title_font = pygame.font.Font("8bit_font.ttf", 300)
menu_button_font = pygame.font.Font("8bit_font.ttf", 150)
character_select_font = pygame.font.Font("8bit_font.ttf", 100)
character_select_title_font = pygame.font.Font("8bit_font.ttf", 215)
season_font = pygame.font.Font("8bit_font.ttf", 100)
gameover_title_font = pygame.font.Font("8bit_font.ttf", 400)
gameover_font = pygame.font.Font("8bit_font.ttf", 70)

season_colors = {"Spring": (9,101,76),
                "Summer": (15,102,109),
                "Autumn": (169,48,19),
                "Winter": (28,118,145)}

# Set up sounds.
gameOverSound = pygame.mixer.Sound("gameover.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")
click_sound_menu = pygame.mixer.Sound("click_menu.mp3")
hover_sound_menu = pygame.mixer.Sound("hover_sound.mp3")
coin_collected_sound = pygame.mixer.Sound("coin.mp3")
hourglass_collected_sound = pygame.mixer.Sound("hourglass.mp3")

# Set up images.
NinjaImages = {"run_right" : scale_proportionally(pygame.image.load("ninja_run_right.png").convert_alpha(), PLAYERHEIGHT),
                "run_left" : scale_proportionally(pygame.image.load("ninja_run_left.png").convert_alpha(), PLAYERHEIGHT),
               "jump_right" : scale_proportionally(pygame.image.load("ninja_jump_right.png").convert_alpha(), PLAYERHEIGHT),
               "jump_left" : scale_proportionally(pygame.image.load("ninja_jump_left.png").convert_alpha(), PLAYERHEIGHT),
               "stoic": scale_proportionally(pygame.image.load("ninja_stoic.png").convert_alpha(), PLAYERHEIGHT)}

AdventurerImages = {"run_right" : scale_proportionally(pygame.image.load("adventurer_run_right.png").convert_alpha(), PLAYERHEIGHT),
                "run_left" : scale_proportionally(pygame.image.load("adventurer_run_left.png").convert_alpha(), PLAYERHEIGHT),
               "jump_right" : scale_proportionally(pygame.image.load("adventurer_jump_right.png").convert_alpha(), PLAYERHEIGHT),
               "jump_left" : scale_proportionally(pygame.image.load("adventurer_jump_left.png").convert_alpha(), PLAYERHEIGHT),
               "stoic": scale_proportionally(pygame.image.load("adventurer_stoic.png").convert_alpha(), PLAYERHEIGHT)}

KnightImages = {"run_right" : scale_proportionally(pygame.image.load("knight_run_right.png").convert_alpha(), PLAYERHEIGHT),
                "run_left" : scale_proportionally(pygame.image.load("knight_run_left.png").convert_alpha(), PLAYERHEIGHT),
               "jump_right" : scale_proportionally(pygame.image.load("knight_jump_right.png").convert_alpha(), PLAYERHEIGHT),
               "jump_left" : scale_proportionally(pygame.image.load("knight_jump_left.png").convert_alpha(), PLAYERHEIGHT),
               "stoic": scale_proportionally(pygame.image.load("knight_stoic.png").convert_alpha(), PLAYERHEIGHT)}

playerImages = NinjaImages

playerImage = playerImages["stoic"]
playerRect = playerImage.get_rect()

baddieImages = {"Spring": pygame.image.load("thorn.png").convert_alpha(),
                "Summer": pygame.image.load("flame.png").convert_alpha(),
                "Autumn": pygame.image.load("leaf.png").convert_alpha(),
                "Winter": pygame.image.load("ice.png").convert_alpha()}
baddieImage = baddieImages[current_season]

heartImage = pygame.image.load("heart.png").convert_alpha()
heartImage = pygame.transform.scale(heartImage, (80, 80))

coinImage = pygame.image.load("coin.png").convert_alpha()
hourglassImage = pygame.image.load("hourglass.png").convert_alpha()

platformImages = {
    "Spring": pygame.image.load("platform_spring.png").convert_alpha(),
    "Summer": pygame.image.load("platform_summer.png").convert_alpha(),
    "Autumn": pygame.image.load("platform_autumn.png").convert_alpha(),
    "Winter": pygame.image.load("platform_winter.png").convert_alpha()
}
platformImage = platformImages[current_season]

floorImages = {
    "Spring": load_and_scale_floor("floor_spring.png"),
    "Summer": load_and_scale_floor("floor_summer.png"),
    "Autumn": load_and_scale_floor("floor_autumn.png"),
    "Winter": load_and_scale_floor("floor_winter.png")
}
FloorImage = floorImages[current_season]

# Show the Main Menu screen.
MainMenu()

topScore = 0
topDay = 0
while True:
    # Set up the start of the game.
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)

    PLAYERYSPEED = 0
    JUMPSLEFT = 2
    on_ground = False
    drop_down_platform = False
    quit_to_menu = False
    score = 0
    day = 0
    day_timer = 0
    season_index = 0
    lives = 3
    
    baddies = []
    baddieAddCounter = 0

    coins = []
    coinAddCounter = 0

    hourglasses = []
    hourglassAddCounter = 0
    slowTime = False
    slowTimer = 0

    platforms = []
    platformAddCounter = 0

    moveLeft = moveRight = False

    stopMenuMusic()
    pygame.mixer.music.load("music_game.wav")
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.
        
        day_timer += 1 # Increase days.
        if slowTime:
            if day_timer >= 40:
                day += 1
                day_timer = 0
        else:
            if day_timer >= 20:
                day += 1
                day_timer = 0
        
        # Change background (season) based on number of days (cycle of seasons).
        if day == 0:
            BACKGROUNDIMAGE = backgrounds[current_season]
            baddieImage = baddieImages[current_season]
            platformImage = platformImages[current_season]
            floorImage = floorImages[current_season]

        if day % 90 == 0 and day != 0 and NEXTBACKGROUNDIMAGE is None:
            season_index = (season_index + 1) % len(seasons)
            current_season = seasons[season_index]
            baddieImage = baddieImages[current_season]
            platformImage = platformImages[current_season]
            floorImage = floorImages[current_season]
            NEXTBACKGROUNDIMAGE = backgrounds[current_season]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                    playerImage = playerImages["run_left"]
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                    playerImage = playerImages["run_right"]
                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 3
                    drop_down_platform = True
                if event.key == K_SPACE and JUMPSLEFT > 0:
                    PLAYERYSPEED = -JUMPPOWER
                    JUMPSLEFT -= 1
                    on_ground = False
                if event.key == K_ESCAPE:
                    click_sound_menu.play()
                    quit_to_menu = True
                    break

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 1
                    drop_down_platform = False

        # Change player image based on movement and jumping.
        if not on_ground:
            if moveLeft:
                playerImage = playerImages["jump_left"]
            elif moveRight:
                playerImage = playerImages["jump_right"]
            else:
                playerImage = playerImages["jump_right"]
        else:
            if moveLeft:
                playerImage = playerImages["run_left"]
            elif moveRight:
                playerImage = playerImages["run_right"]
            else:
                playerImage = playerImages["stoic"]

        # Add new baddies at the right of the screen.
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            spawn_range = 150
            baddieMinY = max(0, playerRect.centery - spawn_range)
            baddieMaxY = min(WINDOWHEIGHT - baddieSize, playerRect.centery + spawn_range)
            baddieY = random.randint(baddieMinY, baddieMaxY)
            newBaddie = {"rect": pygame.Rect(WINDOWWIDTH, baddieY, baddieSize, baddieSize),
                        "speed": random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        "surface": pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Add coins to rise score.
        coinAddCounter += 1
        if coinAddCounter == ADDNEWCOINRATE:
            coinAddCounter = 0
            coinSize = 75
            newCoin = {"rect": pygame.Rect(WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - coinSize), coinSize, coinSize),
                        "speed": 5,
                        "surface":pygame.transform.scale(coinImage, (coinSize, coinSize)),
                        }

            coins.append(newCoin)
        
        # Add hourglasses to slow time.
        hourglassAddCounter += 1
        if hourglassAddCounter == ADDNEWHOURGLASSRATE:
            hourglassAddCounter = 0
            hourglassWidth = 45
            hourglassHeight = 55
            newHourglass = {"rect": pygame.Rect(WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - hourglassHeight), hourglassWidth, hourglassHeight),
                        "speed": 5,
                        "surface":pygame.transform.scale(hourglassImage, (hourglassWidth, hourglassHeight)),
                        }
            hourglasses.append(newHourglass)
        
        # Add platforms at the right of the screen.
        platformAddCounter += 1
        if platformAddCounter == ADDNEWPLATFORMRATE:
            platformAddCounter = 0
            platform_width = random.randint(PLATFORMMINWIDTH, PLATFORMMAXWIDTH)
            platform_X = WINDOWWIDTH
            platform_Y = random.randint(WINDOWHEIGHT // 2, WINDOWHEIGHT - FLOORHEIGHT - 50)
            image_rect = pygame.Rect(platform_X, platform_Y, platform_width, PLATFORMHEIGHT)
            hitbox_rect = pygame.Rect(image_rect.left, image_rect.top + PLATFORM_HITBOX_OFFSET_Y, image_rect.width, image_rect.height - PLATFORM_HITBOX_OFFSET_Y)
            
            newPlatform = {"rect": image_rect,
                           "hitbox" : hitbox_rect,
                           "speed": PLATFORMSPEED,
                           "surface": pygame.transform.scale(platformImage, (platform_width, PLATFORMHEIGHT)),
                          }
            platforms.append(newPlatform)

        # Apply gravity to the player.
        PLAYERYSPEED += GRAVITY
        playerRect.y += PLAYERYSPEED

        # Collision of the player with platforms.
        for p in platforms :
            if not drop_down_platform and playerRect.colliderect(p["hitbox"]):
                if PLAYERYSPEED > 0 and playerRect.bottom < p["hitbox"].bottom:
                    playerRect.bottom = p["hitbox"].top
                    PLAYERYSPEED = 0
                    on_ground = True
                    JUMPSLEFT = 2
        
        # Collision of the player with the floor.
        floor_collision_y = WINDOWHEIGHT - FLOORHEIGHT + FLOOR_HITBOX_OFFSET_Y
        if playerRect.bottom >= floor_collision_y:
            playerRect.bottom = floor_collision_y
            PLAYERYSPEED = 0
            on_ground = True
            JUMPSLEFT = 2

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        # Move the baddies to the left.
        for b in baddies:
            if not slowTime:
                b["rect"].move_ip(-b["speed"],0)
            elif slowTime:
                b["rect"].move_ip(-1, 0)
        
        # Move the coins to the left.
        for c in coins:
            if not slowTime:
                c["rect"].move_ip(-c["speed"],0)
            elif slowTime:
                c["rect"].move_ip(-1, 0)
        
        # Move the hourglasses to the left.
        for h in hourglasses:
            if not slowTime:
                h["rect"].move_ip(-h["speed"],0)
            elif slowTime:
                h["rect"].move_ip(-1, 0)

        # Move the platforms to the left.
        for p in platforms:
            if not slowTime:
                p["rect"].move_ip(-p["speed"], 0)
                p["hitbox"].move_ip(-p["speed"], 0)
            elif slowTime:
                p["rect"].move_ip(-1, 0)
                p["hitbox"].move_ip(-1, 0)

        # Delete baddies that have gone past the left of the screen.
        for b in baddies[:]:
            if b["rect"].right < 0:
                baddies.remove(b)
        
        # Delete coins that have gone past the left of the screen.
        for c in coins[:]:
            if c["rect"].right < 0:
                coins.remove(c)
        
        # Delete hourglasses that have gone past the left of the screen.
        for h in hourglasses[:]:
            if h["rect"].right < 0:
                hourglasses.remove(h)
        
        # Delete platforms that have gone past the left of the screen.
        for p in platforms[:]:
            if p["rect"].right < 0:
                platforms.remove(p)

        # Draw the game world on the window.     
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

        # Draw the floor.
        floor_width = floorImage.get_width()
        for x in range(0, WINDOWWIDTH + floor_width, floor_width):
             windowSurface.blit(floorImage, (x, WINDOWHEIGHT - FLOORHEIGHT))

        # Draw the score, top score, current season, days, top days and remaining lives (hearts).
        drawText("Score : %s" % (score), font, windowSurface, 10, 0, color = season_colors[current_season])
        drawText("Top Score : %s" % (topScore), font, windowSurface, 10, 40, color = season_colors[current_season])
        drawText("Top Days : %s" % (topDay), font, windowSurface, 10, 80, color = season_colors[current_season])
        drawText(f"{current_season} | {day} days", season_font, windowSurface, WINDOWWIDTH/2, 40, center = True, color = season_colors[current_season])
        for i in range(lives):
            x = WINDOWWIDTH - (i + 1) * (heartImage.get_width() + 10)
            y = 10
            windowSurface.blit(heartImage, (x,y))

        # Draw the player"s rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b["surface"], b["rect"])

        # Draw each coins.
        for c in coins:
            windowSurface.blit(c["surface"], c["rect"])
        
        # Draw each hourglasses.
        for h in hourglasses:
            windowSurface.blit(h["surface"],h["rect"])
        
        # Draw each platforms.
        for p in platforms:
            windowSurface.blit(p["surface"], p["rect"])

        pygame.display.update()

        # Check if any of the baddies have hit the player amd if so, remove it and decrease a life.
        if playerHasHitBaddie(playerRect, baddies) is not None:
            lives -= 1
            baddies.remove(playerHasHitBaddie(playerRect, baddies))
            hit_sound.play()
    
            windowSurface.blit(red_filter, (0, 0))
            pygame.display.update()
            pygame.time.wait(50)

            if lives <= 0:
                if score > topScore:
                    topScore = score # set new top score
                if day > topDay:
                    topDay = day # set new top day
                current_season = seasons[0]
                BACKGROUNDIMAGE = backgrounds[current_season]
                NEXTBACKGROUNDIMAGE = None
                BACKGROUND_ALPHA = 0
                break
        
        # Check if player has collected any coin and if so, remove it and increase score.
        if playerHasCollectedCoin(playerRect, coins) is not None:
            coins.remove(playerHasCollectedCoin(playerRect, coins))
            coin_collected_sound.play()
            score += 100
        
        # Check if player has collected any hourglass and if so, remove it and slow time for a period.
        if playerHasCollectedHourglass(playerRect, hourglasses) is not None:
            hourglasses.remove(playerHasCollectedHourglass(playerRect, hourglasses))
            hourglass_collected_sound.play()
            pygame.mixer.music.pause()
            slowTime = True
        
        # Managing slow time.
        if slowTime:
            slowTimer += 1
            if slowTimer >= 125:
                slowTime = False
                slowTimer = 0
                hourglass_collected_sound.stop()
                pygame.mixer.music.unpause()
        
        # Check if any baddie has hit a platform and if so, remove it.
        hit_baddie = baddieHasHitPlatform(platforms, baddies)
        if hit_baddie is not None:
            baddies.remove(hit_baddie)

        mainClock.tick(FPS)
        
        if quit_to_menu:
            current_season = seasons[0]
            break

    # Stop the game and show the Game Over screen.
    if quit_to_menu:
            pygame.mixer.music.stop()
            MainMenu()
            continue
    elif quit_to_menu == False:
        pygame.mixer.music.stop()
        
        gameOverSound.play(fade_ms = 1500)

        windowSurface.blit(GAMEOVER_BACKGROUND, (0, 0))
        drawText("GAME OVER", gameover_title_font, windowSurface, (WINDOWWIDTH/2), 220, (15, 8, 5), center = True)   
        drawText("Enter if you dare to play again...", gameover_font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT / 2), color = (255, 255, 255), center = True)
        drawText("If you are not brave enough escape...", gameover_font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/1.4), color = (255, 255, 255), center = True)
        pygame.display.update()
        result = waitForPlayerToPressKey()
        gameOverSound.stop()
        if result == "menu":
            MainMenu()
            continue
        continue
