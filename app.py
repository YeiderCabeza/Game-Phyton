import pygame
import sys
import os
import random
import math

pygame.init()

# Dimensiones de la pantalla
screen_with = 800
screen_height = 600
screen = pygame.display.set_mode((screen_with, screen_height))

# Ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


fondo = resource_path('assets/images/background.png')
background = pygame.image.load(fondo)

icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(icon)

sonido = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(sonido)

imgjugador = resource_path('assets/images/space-invaders.png')
playerimg = pygame.image.load(imgjugador)

bala = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(bala)

gameover_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(gameover_font, 60)

fuente = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(fuente, 32) #tamaño de la fuente


# ---- TITULO ----
pygame.display.set_caption("DEMO")
pygame.display.set_icon(icon)
# #loopses un argumento entero opcional, que es 0 por defecto, que indica cuántas veces repetir la música.
# La música se repite indefinidamente si este argumento se establece en -1.
# pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

# Posicion del jugador
playerX, playerY = 370, 470
playerX_change, playerY_change  = 0, 0

# lista para almacenar la posicion de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
#la cantidad de enemigos
no_of_enemies = 10

# variables para guardar la posiciones de los enemigos
for i in range(no_of_enemies):
    enemy1 = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))
    enemy2 = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))

    # rango de la posicion para el enemigo en X(horizontal) Y(vertical)
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(5) #velocidad en la que aparecen
    enemyY_change.append(20) # posiciones a la que baja 

# Variables para guardar la posiciones de la bala
    #forma normal 
    # bulletX = 0
    # bulletY = 480
    # bulletX_change = 0
    # bulletY_change = 10
    
    # #forma sencilla de escribir el codigo
    bulletX, bulletY = 0, 480 
    bulletX_change, bulletY_change = 0, 10
    bullet_state = "ready"

    # puntuacion
    puntos = 0
    def Mostrar_puntos():
        puntos_valor = font.render("Puntos " + str(puntos), True, (255, 255, 255)) #color de la letra
        screen.blit(puntos_valor, (10, 10)) #posicion del texto en la pantalla

    # mostra en pantalla al player
    def player(x, y):
        screen.blit(playerimg, (x, y))

    def enemy(x, y):
        screen.blit(enemyimg[i], (x, y))
        
#---------------------------------------------------------------------------------------------------------------------
    # funcion para disparar
    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10) )

    # funcion para compra si ha habido un choque
    def iscollission(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
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
        global puntos
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global collision
        global bullet_state

        in_game = True
        while in_game:
            #majeja eventos actualiza y renderiza
         #limpia la pantalla
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0)) #posicion de la imagen de fondo

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()#cerrar el juego
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

            # se actualiza la posicion del jugador
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
                    puntos += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i])

            if bulletY < 0:
                bulletY = 454
                bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            Mostrar_puntos()
            pygame.display.update()
            clock.tick(120)

gameloop()
