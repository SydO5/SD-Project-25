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

PLAYERMOVERATE = 8
JUMPPOWER = 25
GRAVITY = 1
PLAYERHEIGHT = 200

BADDIEMINSIZE = 50
BADDIEMAXSIZE = 100
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 30


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
        if playerRect.colliderect(b['rect']):
            return b
    return None

# Draw text on the surface.
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
    hovered_play = False
    hovered_select = False
    hovered_settings = False
    hovered_quit = False

    while True:
        pygame.mouse.set_visible(True)

        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText('Season Escape', menu_title_font, windowSurface, (WINDOWWIDTH/2), 125, (60,42,83), center = True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        play_button = Button("Play", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.45), menu_button_font)
        select_button = Button("Select Character", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.60), menu_button_font)
        settings_button = Button("Settings", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.75), menu_button_font)
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
                if rect_quit.collidepoint(mouse_x, mouse_y):
                    terminate()

        pygame.display.update()
        mainClock.tick(60)

#Create character selection menu
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
        drawText('Select your Destiny', character_select_title_font, windowSurface, (WINDOWWIDTH/2), 125, (254, 237, 181), center = True)

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

# Set up pygame, the window, and the mouse cursor.
pygame.init()

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
pygame.display.set_caption('Dodger')

# Set up the background image for the menu.
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load("back_menu.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT))

#Set up the background image for gameover.
GAMEOVER_BACKGROUND = pygame.transform.scale(pygame.image.load("back_gameover.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT))

# Scale the background image to fit the screen.
BACKGROUNDIMAGE = pygame.transform.scale(BACKGROUNDIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

#Make dictionnary with backgrounds adjusted to screen size
backgrounds = {
    "printemps": pygame.transform.scale(pygame.image.load("back_printemps.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    "ete": pygame.transform.scale(pygame.image.load("back_été.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    "automne": pygame.transform.scale(pygame.image.load("back_automne.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
    "hiver": pygame.transform.scale(pygame.image.load("back_hiver.png").convert(), (WINDOWWIDTH, WINDOWHEIGHT)),
}

# Create red filter for when player is hit
red_filter = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
red_filter.set_alpha(120)
red_filter.fill((255, 0, 0))

# Set up the fonts.
font = pygame.font.Font("8bit_font.ttf", 48)
menu_title_font = pygame.font.Font("8bit_font.ttf", 300)
menu_button_font = pygame.font.Font("8bit_font.ttf", 150)
character_select_font = pygame.font.Font("8bit_font.ttf", 100)
character_select_title_font = pygame.font.Font("8bit_font.ttf", 215)
gameover_title_font = pygame.font.Font("8bit_font.ttf", 400)
gameover_font = pygame.font.Font("8bit_font.ttf", 70)


# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.mp3')
pygame.mixer.music.load('background.mid')
hit_sound = pygame.mixer.Sound('hit.mp3')
click_sound_menu = pygame.mixer.Sound('click_menu.mp3')
hover_sound_menu = pygame.mixer.Sound('hover_sound.mp3')

# Set up images.
NinjaImages = {"run_right" : scale_proportionally(pygame.image.load('ninja_run_right.png').convert_alpha(), PLAYERHEIGHT),
                "run_left" : scale_proportionally(pygame.image.load('ninja_run_left.png').convert_alpha(), PLAYERHEIGHT),
               "jump_right" : scale_proportionally(pygame.image.load('ninja_jump_right.png').convert_alpha(), PLAYERHEIGHT),
               "jump_left" : scale_proportionally(pygame.image.load('ninja_jump_left.png').convert_alpha(), PLAYERHEIGHT),
               "stoic": scale_proportionally(pygame.image.load('ninja_stoic.png').convert_alpha(), PLAYERHEIGHT)}

AdventurerImages = {"run_right" : scale_proportionally(pygame.image.load('adventurer_run_right.png').convert_alpha(), PLAYERHEIGHT),
                "run_left" : scale_proportionally(pygame.image.load('adventurer_run_left.png').convert_alpha(), PLAYERHEIGHT),
               "jump_right" : scale_proportionally(pygame.image.load('adventurer_jump_right.png').convert_alpha(), PLAYERHEIGHT),
               "jump_left" : scale_proportionally(pygame.image.load('adventurer_jump_left.png').convert_alpha(), PLAYERHEIGHT),
               "stoic": scale_proportionally(pygame.image.load('adventurer_stoic.png').convert_alpha(), PLAYERHEIGHT)}

KnightImages = {"run_right" : scale_proportionally(pygame.image.load('knight_run_right.png').convert_alpha(), PLAYERHEIGHT),
                "run_left" : scale_proportionally(pygame.image.load('knight_run_left.png').convert_alpha(), PLAYERHEIGHT),
               "jump_right" : scale_proportionally(pygame.image.load('knight_jump_right.png').convert_alpha(), PLAYERHEIGHT),
               "jump_left" : scale_proportionally(pygame.image.load('knight_jump_left.png').convert_alpha(), PLAYERHEIGHT),
               "stoic": scale_proportionally(pygame.image.load('knight_stoic.png').convert_alpha(), PLAYERHEIGHT)}

playerImages = NinjaImages

playerImage = playerImages["stoic"]
playerRect = playerImage.get_rect()

baddieImages = {"printemps": pygame.image.load('thorn.png').convert_alpha(),
                "ete": pygame.image.load('flame.png').convert_alpha(),
                "automne": pygame.image.load('leaf.png').convert_alpha(),
                "hiver": pygame.image.load('ice.png').convert_alpha()}

baddieImage = baddieImages["printemps"]

# Show the "Start" screen.
MainMenu()

topScore = 0
while True:
    # Set up the start of the game.
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    PLAYERYSPEED = 0
    JUMPSLEFT = 2
    on_ground = False
    quit_to_menu = False
    baddies = []
    baddieAddCounter = 0
    score = 0
    lives = 3
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    pygame.mixer.music.play(-1, 0.0)

    

    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.
        
        # Change background (season) based on score
        if score == 1:
            BACKGROUNDIMAGE = backgrounds["printemps"]
            baddieImage = baddieImages["printemps"]
        if score == 500 and NEXTBACKGROUNDIMAGE is None:
            baddieImage = baddieImages["ete"]
            NEXTBACKGROUNDIMAGE = backgrounds["ete"]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0
        if score == 1000 and NEXTBACKGROUNDIMAGE is None:
            baddieImage = baddieImages["automne"]
            NEXTBACKGROUNDIMAGE = backgrounds["automne"]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0
        if score == 1500 and NEXTBACKGROUNDIMAGE is None:
            baddieImage = baddieImages["hiver"]
            NEXTBACKGROUNDIMAGE = backgrounds["hiver"]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
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
                if event.key == K_SPACE and JUMPSLEFT > 0:
                    PLAYERYSPEED = -JUMPPOWER
                    JUMPSLEFT -= 1
                    on_ground = False
                if event.key == K_ESCAPE:
                    click_sound_menu.play()
                    quit_to_menu = True
                    break

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                    

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 1

        #Change play image based on movement and jumping
        # Choisir l'image du joueur selon mouvement et saut
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

        # Add new baddies at the left of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)


        # Apply gravity to the player.
        PLAYERYSPEED += GRAVITY
        playerRect.y += PLAYERYSPEED

        #So player can't fall below the floor.
        if playerRect.bottom >= WINDOWHEIGHT:
            playerRect.bottom = WINDOWHEIGHT
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
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(-b['speed'],0)
            elif reverseCheat:
                b['rect'].move_ip(5, 0)
            elif slowCheat:
                b['rect'].move_ip(-1, 0)

        # Delete baddies that have gone past the left of the screen.
        for b in baddies[:]:
            if b['rect'].right < 0:
                baddies.remove(b)

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

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Lives: %s' % (lives), font, windowSurface, 10, 80)

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
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
                break

        mainClock.tick(FPS)
        
        if quit_to_menu:
            break

    # Stop the game and show the "Game Over" screen.
    if quit_to_menu:
            pygame.mixer.music.stop()
            MainMenu()
            continue
    elif quit_to_menu == False:
        pygame.mixer.music.stop()
        gameOverSound.play(fade_ms = 1500)

        windowSurface.blit(GAMEOVER_BACKGROUND, (0, 0))
        drawText('GAME OVER', gameover_title_font, windowSurface, (WINDOWWIDTH/2), 220, (15, 8, 5), center = True)   
        drawText('Enter if you dare to play again...', gameover_font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT / 2), color = (255, 255, 255), center = True)
        drawText('If you are not brave enough escape...', gameover_font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/1.4), color = (255, 255, 255), center = True)
        pygame.display.update()
    
        result = waitForPlayerToPressKey()
        gameOverSound.stop()
        if result == "menu":
            MainMenu()
            continue
        continue
