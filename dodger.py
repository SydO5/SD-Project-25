import pygame, random, sys
from pygame.locals import *

# ==============================
# --- CONSTANTES GLOBALES ---
# ==============================

BLANC = (255, 255, 255)
BLEU = (60, 130, 200)
BLEU_CLAIR = (90, 160, 230)
GRIS = (40, 40, 40)

pygame.init()
ECRAN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
LARGEUR, HAUTEUR = ECRAN.get_size()
pygame.display.set_caption("Dodger - Menu Principal")
POLICE_TITRE = pygame.font.Font(None, int(HAUTEUR / 7))
POLICE_BOUTON = pygame.font.Font(None, int(HAUTEUR / 15))


# ==============================
# --- CLASSE BOUTON ---
# ==============================
class Bouton:
    def __init__(self, texte, x, y, action=None):
        self.texte = texte
        self.action = action
        self.font_normal = pygame.font.Font(None, int(HAUTEUR / 15))
        self.font_hover = pygame.font.Font(None, int(HAUTEUR / 13))
        self.x = x
        self.y = y

    def dessiner(self, ecran, survol):
        font = self.font_hover if survol else self.font_normal
        couleur = (255, 255, 255) if survol else (220, 220, 220)
        texte_surface = font.render(self.texte, True, couleur)
        texte_rect = texte_surface.get_rect(center=(self.x, self.y))
        ecran.blit(texte_surface, texte_rect)

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
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return b
    return None

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

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

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
playerImage = pygame.image.load('player.png')
playerImage = pygame.transform.scale(playerImage, (80, 80))
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) - 50)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2) - 200 , (WINDOWHEIGHT / 2) )
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
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
                        terminate()

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

# ==============================
# --- MENU PRINCIPAL ---
# ==============================
def menu_principal():
    clock = pygame.time.Clock()

    # ---- Image de fond ----
    try:
        fond = pygame.image.load("menu_background.jpeg").convert()
        fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))
    except:
        fond = pygame.Surface((LARGEUR, HAUTEUR))
        fond.fill((30, 30, 30))

    # ---- Titre et boutons ----
    titre_font = pygame.font.Font(None, int(HAUTEUR / 6))
    boutons = [
        Bouton("JOUER", LARGEUR // 2, int(HAUTEUR * 0.5), "jouer"),
        Bouton("QUITTER", LARGEUR // 2, int(HAUTEUR * 0.65), "quitter"),
    ]

    while True:
        ECRAN.blit(fond, (0, 0))

        souris_x, souris_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for bouton in boutons:
                    font_hover = bouton.font_hover
                    texte_surface = font_hover.render(bouton.texte, True, (255, 255, 255))
                    texte_rect = texte_surface.get_rect(center=(bouton.x, bouton.y))
                    if texte_rect.collidepoint(souris_x, souris_y):
                        return bouton.action

        # ---- Affichage des boutons ----
        for bouton in boutons:
            texte_rect = bouton.font_normal.render(bouton.texte, True, (255, 255, 255)).get_rect(center=(bouton.x, bouton.y))
            survol = texte_rect.collidepoint((souris_x, souris_y))
            bouton.dessiner(ECRAN, survol)

        pygame.display.flip()
        clock.tick(60)

# ==============================
# --- LANCEMENT ---
# ==============================
if __name__ == "__main__":
    while True:
        choix = menu_principal()
        if choix == "jouer":
            jouer_dodger()
        elif choix == "quitter":
            pygame.quit()
            sys.exit()
