import pygame, random, sys
from pygame.locals import *

# Set up some constants.
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
BACKGROUNDIMAGE = pygame.image.load("back_printemps.png")
NEXTBACKGROUNDIMAGE = None
BACKGROUND_ALPHA = 0
BACKGROUND_FADE_SPEED = 60
FPS = 60

PLAYERMOVERATE = 8
JUMPPOWER = 25
GRAVITY = 1

BADDIEMINSIZE = 30
BADDIEMAXSIZE = 50
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 30


#Set up functions.
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    MainMenu()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return b
    return None

def drawText(text, font, surface, x, y, color = TEXTCOLOR):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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

# Create main menu with start and quit button.
def MainMenu():
    hovered_play = False
    hovered_quit = False

    while True:
        pygame.mouse.set_visible(True)

        windowSurface.blit(MENU_BACKGROUND, (0,0))
        drawText('Season Escape', menu_title_font, windowSurface, (WINDOWWIDTH/300), 0, (254, 237, 181))
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        play_button = Button("Play", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.45), menu_button_font)
        quit_button = Button("Quit", WINDOWWIDTH//2, int(WINDOWHEIGHT*0.9), menu_button_font)
        
        rect_play_normal = play_button.draw(windowSurface, (60,42,83))
        rect_quit_normal = quit_button.draw(windowSurface, (254, 237, 181))

        hover_play = rect_play_normal.collidepoint(mouse_x, mouse_y)
        hover_quit = rect_quit_normal.collidepoint(mouse_x, mouse_y)

        if hover_play and not hovered_play:
            hover_sound_menu.play()
        if hover_quit and not hovered_quit:
            hover_sound_menu.play()
        
        hovered_play = hover_play
        hovered_quit = hover_quit

        rect_play = play_button.draw(windowSurface, (60,42,83), (204,99,104), hover_play)
        rect_quit = quit_button.draw(windowSurface, (254, 237, 181), (204,99,104), hover_quit)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if rect_play.collidepoint(mouse_x, mouse_y):
                    click_sound_menu.play()
                    return
                if rect_quit.collidepoint(mouse_x, mouse_y):
                    terminate()

        pygame.display.update()
        mainClock.tick(60)

# Set up pygame, the window, and the mouse cursor.
pygame.init()

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
pygame.display.set_caption('Dodger')

# Set up the background image for the menu.
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load("back_menu.png"), (WINDOWWIDTH, WINDOWHEIGHT))

# Scale the background image to fit the screen.
BACKGROUNDIMAGE = pygame.transform.scale(BACKGROUNDIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

#Make dictionnary with backgrounds adjusted to screen size
backgrounds = {
    "printemps": pygame.transform.scale(pygame.image.load("back_printemps.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "ete": pygame.transform.scale(pygame.image.load("back_été.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "automne": pygame.transform.scale(pygame.image.load("back_automne.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "hiver": pygame.transform.scale(pygame.image.load("back_hiver.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
}

# Create red filter for when player is hit
red_filter = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
red_filter.set_alpha(120)
red_filter.fill((255, 0, 0))

# Set up the fonts.
font = pygame.font.SysFont(None, 48)
menu_title_font = pygame.font.Font("8bit_font.ttf", 300)
menu_button_font = pygame.font.Font("8bit_font.ttf", 150)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
hit_sound = pygame.mixer.Sound('hit.mp3')
click_sound_menu = pygame.mixer.Sound('click_menu.mp3')
hover_sound_menu = pygame.mixer.Sound('hover_sound.mp3')

# Set up images.
playerImage = pygame.image.load('ninja_run.png')
playerImage = pygame.transform.scale(playerImage, (110, (110*7/5) ))
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# Show the "Start" screen.
MainMenu()

topScore = 0
while True:
    # Set up the start of the game.
    pygame.mouse.set_visible(False)
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    PLAYERYSPEED = 0
    JUMPSLEFT = 2
    on_ground = False
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
        if score == 500 and NEXTBACKGROUNDIMAGE is None:
            NEXTBACKGROUNDIMAGE = backgrounds["ete"]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0
        if score == 1000 and NEXTBACKGROUNDIMAGE is None:
            NEXTBACKGROUNDIMAGE = backgrounds["automne"]
            fade_surface = NEXTBACKGROUNDIMAGE.copy()
            fade_surface.set_alpha(0)
            BACKGROUND_ALPHA = 0
        if score == 1500 and NEXTBACKGROUNDIMAGE is None:
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
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 3
                if event.key == K_SPACE and JUMPSLEFT > 0:
                    PLAYERYSPEED = -JUMPPOWER
                    JUMPSLEFT -= 1

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        MainMenu()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_DOWN or event.key == K_s:
                    GRAVITY = 1

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

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2) - 150, (WINDOWHEIGHT / 2) - 50)
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 2) - 250, (WINDOWHEIGHT / 2))
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()