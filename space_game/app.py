import pygame, sys
from pygame.locals import *

#  variables globales
ancho = 900
alto = 480

class navespacial(pygame.sprite.Sprite):
    # clase para las naves 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenave =pygame.image.load("space_game/assets/nave.jpg")
        
        # posicion de la nave 
        #crea un nuevo rect con el tamaño de la imagen
        self.rect = self.imagenave.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30
        
        self.listaDisparo= []
        self.vida = True
        self.velocidad = 5
        # print (self.rect)
        
    def movimiento(self):
        if self.vida == True:
            if self.rect.left <=0:
                self.rect.left = 0
            elif self.rect.right>900: 
                self.rect.right =900
    
    # def movimiento(self):#Movimiento de la nave
    #     keys = pygame.key.get_pressed()
    #     #Movimiento a la izquierda
    #     if keys[K_a]:
    #         if self.rect.centerx>51:#Si el rectangulo x es mayor a 1 hacer
    #              self.rect.centerx -= self.velocidad
    #     #Movimiento a la derecha
    #     if keys[K_d]:
    #         if self.rect.centerx<851:#Si el rectangulo x es menor 890 hacer
    #             self.rect.centerx += self.velocidad 
    
    def disparar(self,x,y):
        # print("disparo")
        # creamos un objeto y lo guardamos en la listadedisparos
        miproyectil = proyectil(x,y)
        self.listaDisparo.append(miproyectil)
    
    def dibujar(self,superficie):
        superficie.blit(self.imagenave, self.rect)
          
class proyectil(pygame.sprite.Sprite):
    def __init__(self,posx, posy):
       pygame.sprite.Sprite.__init__(self)
       self.imagenProyectil = pygame.image.load('space_game/assets/disparoa.jpg')
       self.rect = self.imagenProyectil.get_rect()
       self.velocidadisparo = 1
       
       self.rect.top = posy
       self.rect.left = posx
       
    def trayetoria(self):
        self.rect.top = self.rect.top - self.velocidadisparo
        
    def dibujar(self, superficie):
        superficie.blit(self.imagenProyectil, self.rect)
        
       
def SpaceGame():
    pygame.init()
    pantalla = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Game")
    
    background= pygame.image.load("space_game/assets/Fondo.jpg")
    jugador = navespacial()
    demoproyectil = proyectil(ancho/2, alto-30)
    enjuego = True
    
    while True:
        
        jugador.movimiento()
        demoproyectil.trayetoria()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if enjuego== True:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == K_LEFT:
                        jugador.rect.left -= jugador.velocidad
                        
                    elif evento.key == K_RIGHT:
                        jugador.rect.right += jugador.velocidad   
                        
                    elif evento.key == K_s:
                        # jugador.disparar()
                        # toma la posicion el jugador y la envia al jugador.disparar/proyectil/trayectoria
                        x,y = jugador.rect.center
                        jugador.disparar(x,y)
        
        pantalla.blit(background,(0,0))
        jugador.dibujar(pantalla)
        # demoproyectil.dibujar(pantalla)
        
        if len(jugador.listaDisparo)>0:
            for x in jugador.listaDisparo:
                x.dibujar(pantalla)
                x.trayetoria()
                # elimina los disparos en la pantalla
                if x.rect.top < 100:
                    jugador.listaDisparo.remove(x)
                
        pygame.display.update()
        
SpaceGame()