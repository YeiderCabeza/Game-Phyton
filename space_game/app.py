import pygame, sys
from random import randint
from pygame.locals import *
pygame.init()

#colores funcionan en rgb
# color= (255,9,87)
color = pygame.Color(25,97,87)
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Game")

# creando figuras geometricas                               
# pygame.draw.line(pantalla,color,(20,40),(520,70),10)#punto inicial,punto final,ancho
# pygame.draw.circle(pantalla,color,(480,290),120)#punto inicial,radio
rectangulo =pygame.draw.rect(pantalla,color,(50,470,200,80))#punto inicial,largo,ancho
# pygame.draw.polygon(pantalla,color,( (40,50),(150,34),(240,340), (49,239) ))#cordenadas que se unen 
imagen= pygame.image.load("space_invaders/assets/images/space-invaders1.png")

fuente = pygame.font.Font('space_invaders/assets/fonts/comicbd.ttf', 32)
texto = fuente.render("texto en pantalla",0,color)

fuentesys = pygame.font.SysFont('Arial', 32)
textosys = fuentesys.render("texto en pantalla",0,color)



# posX = randint(0,129) 
# posY = randint(0,129)
posX,posY = 200, 100
velocidad = 1
blanco=(255,255,255)
derecha= True
aux = 1

#Recorre los eventos ya establecidos por pygame
while True:
    # el metodo get_tick devuelve un entero en milisegundos
   tiempo = pygame.time.get_ticks()/1000
   if aux==tiempo :
       aux+=1
       print (tiempo)
    
#    pantalla.fill(color)
   pantalla.fill(blanco)
   rectangulo_dos=pantalla.blit(imagen, (posX, posY)) #carga la img de la nave
   
   pygame.draw.rect(pantalla, color, rectangulo)
   rectangulo.left, rectangulo.top = pygame.mouse.get_pos()
   
   if rectangulo.colliderect(rectangulo_dos):
       velocidad= 0
       print("colisiono")
   
   for evento in pygame.event.get():
       if evento.type == QUIT:
           pygame.quit()
           sys.exit()
    #    elif evento.type ==pygame.KEYDOWN:
    #        if evento.key == K_LEFT:
    #            posX-=velocidad 
    #        elif evento.key == K_RIGHT:
    #            posX+=velocidad 
    #    elif evento.type ==pygame.KEYUP:
    #        if evento.key == K_LEFT:
    #            print(" izquierda liberada")
    #        elif evento.key == K_RIGHT:
    #            print(" derecha liberada")
   if derecha ==True:
       if posX<700:
           posX+=velocidad
           rectangulo_dos.left= posX
       else:
           derecha = False
   else:
       if posX>1:
           posX-=velocidad
           rectangulo_dos.left= posX
       else:
           derecha = True
#funcion para el mouse
#    posX, posY = pygame.mouse.get_pos()
#    posX = posX-43
#    posY = posY-40

#  COLOCAR TEXTO EN LA PANTALLA
#    
#    pantalla.blit(textosys,(300,400))

   contador = fuente.render("Time: " + str(tiempo),0,color)
   pantalla.blit(contador,(100,100))
   
   pygame.display.update()