import pygame, random, sys
from pygame.locals import *

# ==============================
# --- CONSTANTES GLOBALES ---
# ==============================
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60

PLAYERMOVERATE = 8
JUMPPOWER = 20
GRAVITY = 1

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 5
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 30

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


# ==============================
# --- JEU DODGER ---
# ==============================
def jouer_dodger():
    pygame.display.set_caption("Dodger")

    windowSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WINDOWWIDTH, WINDOWHEIGHT = windowSurface.get_size()
    mainClock = pygame.time.Clock()

    try:
        BACKGROUNDIMAGE = pygame.image.load("back_printemps.png")
    except:
        BACKGROUNDIMAGE = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        BACKGROUNDIMAGE.fill((150, 220, 150))

    BACKGROUNDIMAGE = pygame.transform.scale(BACKGROUNDIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

    backgrounds = {
        "printemps": pygame.transform.scale(pygame.image.load("back_printemps.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
        "ete": pygame.transform.scale(pygame.image.load("back_été.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
        "automne": pygame.transform.scale(pygame.image.load("back_automne.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
        "hiver": pygame.transform.scale(pygame.image.load("back_hiver.png"), (WINDOWWIDTH, WINDOWHEIGHT)),
    }

    font = pygame.font.SysFont(None, 48)

    try:
        gameOverSound = pygame.mixer.Sound("gameover.wav")
        pygame.mixer.music.load("background.mid")
    except:
        gameOverSound = None

    playerImage = pygame.image.load("player.png")
    playerRect = playerImage.get_rect()
    baddieImage = pygame.image.load("baddie.png")

    def drawText(text, font, surface, x, y):
        textobj = font.render(text, True, TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def playerHasHitBaddie(playerRect, baddies):
        for b in baddies:
            if playerRect.colliderect(b["rect"]):
                return True
        return False

    def waitForPlayerToPressKey():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "menu"
                    return "jouer"

    # --- Écran de départ ---
    windowSurface.fill(BACKGROUNDCOLOR)
    drawText("Dodger", font, windowSurface, (WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) - 50)
    drawText("Appuie sur une touche pour commencer", font, windowSurface, (WINDOWWIDTH / 2) - 300, (WINDOWHEIGHT / 2))
    pygame.display.update()
    choix = waitForPlayerToPressKey()
    if choix == "menu":
        return

    topScore = 0
    while True:
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
        PLAYERYSPEED = 0
        JUMPSLEFT = 2
        GRAVITY = 1
        baddies = []
        baddieAddCounter = 0
        score = 0
        moveLeft = moveRight = False
        reverseCheat = slowCheat = False
        BACKGROUNDIMAGE = backgrounds["printemps"]

        if gameOverSound:
            pygame.mixer.music.play(-1, 0.0)

        while True:
            score += 1

            if score == 500:
                BACKGROUNDIMAGE = backgrounds["ete"]
            if score == 1000:
                BACKGROUNDIMAGE = backgrounds["automne"]
            if score == 1500:
                BACKGROUNDIMAGE = backgrounds["hiver"]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_z:
                        reverseCheat = True
                    if event.key == K_x:
                        slowCheat = True
                    if event.key in [K_LEFT, K_a]:
                        moveLeft = True
                        moveRight = False
                    if event.key in [K_RIGHT, K_d]:
                        moveRight = True
                        moveLeft = False
                    if event.key in [K_DOWN, K_s]:
                        GRAVITY = 3
                    if event.key == K_SPACE and JUMPSLEFT > 0:
                        PLAYERYSPEED = -JUMPPOWER
                        JUMPSLEFT -= 1
                if event.type == KEYUP:
                    if event.key in [K_LEFT, K_a]:
                        moveLeft = False
                    if event.key in [K_RIGHT, K_d]:
                        moveRight = False
                    if event.key in [K_DOWN, K_s]:
                        GRAVITY = 1
                    if event.key in [K_z, K_x]:
                        reverseCheat = slowCheat = False
                        score = 0

            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                newBaddie = {
                    "rect": pygame.Rect(WINDOWWIDTH, random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                    "speed": random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                    "surface": pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                }
                baddies.append(newBaddie)

            PLAYERYSPEED += GRAVITY
            playerRect.y += PLAYERYSPEED

            if playerRect.bottom >= WINDOWHEIGHT:
                playerRect.bottom = WINDOWHEIGHT
                PLAYERYSPEED = 0
                JUMPSLEFT = 2

            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)

            for b in baddies:
                if not reverseCheat and not slowCheat:
                    b["rect"].move_ip(-b["speed"], 0)
                elif reverseCheat:
                    b["rect"].move_ip(5, 0)
                elif slowCheat:
                    b["rect"].move_ip(-1, 0)
            baddies = [b for b in baddies if b["rect"].right > 0]

            windowSurface.blit(BACKGROUNDIMAGE, (0, 0))
            drawText(f"Score: {score}", font, windowSurface, 10, 0)
            drawText(f"Top Score: {topScore}", font, windowSurface, 10, 40)
            windowSurface.blit(playerImage, playerRect)
            for b in baddies:
                windowSurface.blit(b["surface"], b["rect"])
            pygame.display.update()

            if playerHasHitBaddie(playerRect, baddies):
                if score > topScore:
                    topScore = score
                break

            mainClock.tick(FPS)

        if gameOverSound:
            pygame.mixer.music.stop()
            gameOverSound.play()

        drawText("GAME OVER", font, windowSurface, (WINDOWWIDTH / 2) - 150, (WINDOWHEIGHT / 2) - 50)
        drawText("Appuie sur une touche pour rejouer (ESC pour menu)", font, windowSurface, (WINDOWWIDTH / 2) - 350, (WINDOWHEIGHT / 2))
        pygame.display.update()

        choix = waitForPlayerToPressKey()
        if choix == "menu":
            return
        if gameOverSound:
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
