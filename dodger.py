import pygame, random, sys
from pygame.locals import *

# --- CONSTANTES ---
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
BACKGROUNDIMAGE = pygame.image.load("back_printemps.png")
FPS = 60

PLAYERMOVERATE = 8
JUMPPOWER = 20
GRAVITY = 1

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 30

# --- FONCTIONS ---
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
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# --- INITIALISATION ---
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Arrière-plans
BACKGROUNDIMAGE = pygame.transform.scale(BACKGROUNDIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
backgrounds = {
    "printemps": pygame.transform.scale(pygame.image.load("back_printemps.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "ete": pygame.transform.scale(pygame.image.load("back_été.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "automne": pygame.transform.scale(pygame.image.load("back_automne.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    "hiver": pygame.transform.scale(pygame.image.load("back_hiver.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
}

# Police
font = pygame.font.SysFont(None, 48)

# Sons
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')
orbImage = pygame.image.load('orb.png')

# --- IMAGES DE PLATEFORMES ---
platformImages = [
    pygame.image.load("printemps.png"),
    pygame.image.load("ete.png"),
    pygame.image.load("automne.png"),
    pygame.image.load("hiver.png")
]

# --- ÉCRAN DE DÉMARRAGE ---
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) - 50)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2) - 200 , (WINDOWHEIGHT / 2))
pygame.display.update()
waitForPlayerToPressKey()

# --- JEU PRINCIPAL ---
topScore = 0
while True:
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)
    PLAYERYSPEED = 0
    JUMPSLEFT = 2
    on_ground = False
    baddies = []
    baddieAddCounter = 0
    score = 0
    moveLeft = moveRight = False
    reverseCheat = slowCheat = False
    pygame.mixer.music.play(-1, 0.0)

    # --- ORBES ---
    orbSize = 30
    orbs = []
    ADDNEWORBRATE = 400
    orbAddCounter = 0
    orbEffectTimer = 0
    particles = []

    # --- PLATEFORMES ---
    platforms = []
    ADDNEWPLATFORMRATE = 200
    platformAddCounter = 0

    # --- SOL PERMANENT ---
    floor_rect = pygame.Rect(0, WINDOWHEIGHT - 50, WINDOWWIDTH, 50)

    while True:
        score += 1
        
        # Changement de fond selon score
        if score == 1:
            BACKGROUNDIMAGE = backgrounds["printemps"]
        if score == 500:
            BACKGROUNDIMAGE = backgrounds["ete"]
        if score == 1000:
            BACKGROUNDIMAGE = backgrounds["automne"]
        if score == 1500:
            BACKGROUNDIMAGE = backgrounds["hiver"]

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                if event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                if event.key in (K_DOWN, K_s):
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
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                if event.key in (K_RIGHT, K_d):
                    moveRight = False
                if event.key in (K_DOWN, K_s):
                    GRAVITY = 1

        # --- GÉNÉRATION DES ENNEMIS ---
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {
                'rect': pygame.Rect(WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - baddieSize - 50), baddieSize, baddieSize),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))
            }
            baddies.append(newBaddie)

        # --- GÉNÉRATION DES ORBES ---
        orbAddCounter += 1
        if orbAddCounter >= ADDNEWORBRATE:
            orbAddCounter = 0
            newOrb = {
                'rect': pygame.Rect(
                    random.randint(0, WINDOWWIDTH - orbSize),
                    random.randint(100, WINDOWHEIGHT - 200),
                    orbSize, orbSize
                ),
                'surface': pygame.transform.scale(orbImage, (orbSize, orbSize))
            }
            orbs.append(newOrb)

        # --- GÉNÉRATION DES PLATEFORMES ---
        platformAddCounter += 1
        if platformAddCounter >= ADDNEWPLATFORMRATE:
            platformAddCounter = 0
            platformImage = random.choice(platformImages)
            platformWidth = 200
            platformHeight = 40
            newPlatform = {
                'rect': pygame.Rect(
                    WINDOWWIDTH,
                    random.randint(WINDOWHEIGHT - 350, WINDOWHEIGHT - 150),
                    platformWidth,
                    platformHeight
                ),
                'surface': pygame.transform.scale(platformImage, (platformWidth, platformHeight))
            }
            platforms.append(newPlatform)

        # --- GRAVITÉ & COLLISIONS ---
        PLAYERYSPEED += GRAVITY
        playerRect.y += PLAYERYSPEED
        on_ground = False

        # Collision avec plateformes
        for p in platforms:
            if playerRect.colliderect(p['rect']) and PLAYERYSPEED >= 0:
                if playerRect.bottom <= p['rect'].bottom:
                    playerRect.bottom = p['rect'].top
                    PLAYERYSPEED = 0
                    JUMPSLEFT = 2
                    on_ground = True

        # Collision avec le sol
        if playerRect.colliderect(floor_rect):
            playerRect.bottom = floor_rect.top
            PLAYERYSPEED = 0
            JUMPSLEFT = 2
            on_ground = True

        # --- MOUVEMENT JOUEUR ---
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        # --- MOUVEMENT ENNEMIS & PLATEFORMES ---
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(-b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(5, 0)
            elif slowCheat:
                b['rect'].move_ip(-1, 0)
        for b in baddies[:]:
            if b['rect'].right < 0:
                baddies.remove(b)

        for p in platforms:
            p['rect'].move_ip(-5, 0)
        for p in platforms[:]:
            if p['rect'].right < 0:
                platforms.remove(p)

        # --- COLLISION AVEC LES ORBES ---
        for o in orbs[:]:
            if playerRect.colliderect(o['rect']):
                orbs.remove(o)
                GRAVITY = 0.4
                BADDIEMINSPEED = 2
                BADDIEMAXSPEED = 4
                orbEffectTimer = pygame.time.get_ticks()

        # --- FIN EFFET ORBE ---
        if orbEffectTimer and pygame.time.get_ticks() - orbEffectTimer > 5000:
            GRAVITY = 1
            BADDIEMINSPEED = 5
            BADDIEMAXSPEED = 8
            orbEffectTimer = 0
            particles.clear()

        # --- AFFICHAGE ---
        windowSurface.blit(BACKGROUNDIMAGE, (0, 0))

        for o in orbs:
            windowSurface.blit(o['surface'], o['rect'])
        for p in platforms:
            windowSurface.blit(p['surface'], p['rect'])
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        pygame.draw.rect(windowSurface, (50, 200, 50), floor_rect)  # Sol permanent (vert)
        windowSurface.blit(playerImage, playerRect)
        for p in particles:
            pygame.draw.circle(windowSurface, (100, 150, 255), (int(p[0][0]), int(p[0][1])), int(p[2]))

        drawText(f'Score: {score}', font, windowSurface, 10, 0)
        drawText(f'Top Score: {topScore}', font, windowSurface, 10, 40)
        pygame.display.update()

        # --- COLLISION AVEC ENNEMIS ---
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)

    # --- GAME OVER ---
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 2) - 150, (WINDOWHEIGHT / 2) - 50)
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 2) - 250, (WINDOWHEIGHT / 2))
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()


