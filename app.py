import pygame
import sys
import os
import random
import math

pygame.init()

# dimensiones de la pantalla
screen_with = 800
screen_height = 600
screen = pygame.display.set_mode((screen_with, screen_height))


# ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)

asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)

asset_playering = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(asset_playering)

asset_bullet = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bullet)

asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

asset_fonts = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_fonts, 32)


# ---- TITULO ----
pygame.display.set_caption("DEMO")
pygame.display.set_icon(icon)
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

# Posicion del jugador
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

# lista para almacenar la posicion de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

# variables para guardar la posiciones de los enemigos
for i in range(no_of_enemies):
    enemy1 = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))

    enemy2 = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))

    # posicion para el enemigo en X Y
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(5)
    enemyY_change.append(20)

    # variables para guardar la posiciones de la bala
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # puntuacion
    score = 0

    def show_score():
        score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))

    # mostra en pantalla al player
    def player(x, y):
        screen.blit(playerimg, (x, y))

    def enemy(x, y):
        screen.blit(enemyimg[i], (x, y))

    # funcion para disparar
    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))

    # funcion para compra si ha habido un choque
    def iscollission(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                             (math.pow(enemyY-bulletY, 2)))

        if distance < 27:
            return True
        else:
            return False

        # funcion para mostra GAME OVER
    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = over_text.get_rect(
            center=(int(screen_with/2), int(screen_height/2)))
        screen.blit(over_text, text_rect)

        # funcion principal del juego
    def gameloop():
        
        global score
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global collision
        global bullet_state

        in_game = True
        while in_game:
            screen.fill((0,0,0))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # maneja los movimiento del jugador
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                if event.type == pygame.KEYUP:
                        playerX_change = 0

            # se actualiza la posicion del jugaor
            playerX += playerX_change

            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736
            # BUCLE QUE SE EJECUTA PARA CADA ENEMIGO
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <=0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyX_change[i]

                # se comprueba si hay una colision entre una bala y un enemigo

                collision = iscollission(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i])

            if bulletY < 0:
                bulletY = 454
                bullet_state == "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score()

            pygame.display.update()

            clock.tick(120)

gameloop()
