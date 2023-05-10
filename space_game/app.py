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
        # toma el centro de la imagen 
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30
        
        self.listaDisparo= []
        self.vida = True
        self.velocidad = 20
        # print (self.rect)
    
    def movimientoderecha(self):
         self.rect.right += self.velocidad 
         self.movimiento()
         
    def movimientoizqierda(self):
        self.rect.left -= self.velocidad
        self.movimiento()
     
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
        miproyectil = proyectil(x,y)# enviamos las cordenadas a proyrctil
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

class invasor(pygame.sprite.Sprite):
    def __init__(self,posx, posy):
        pygame.sprite.Sprite.__init__(self)
        
        self.imgMarcianoA = pygame.image.load('space_game/assets/marcianoA.jpg')
        self.imgMarcianoB = pygame.image.load('space_game/assets/marcianoB.jpg')
        self.listaEnemigos = [self.imgMarcianoA, self.imgMarcianoB]
        self.posImagen = 0
        
        self.imagenInvasor = self.listaEnemigos[self.posImagen]
        self.rect = self.imagenInvasor.get_rect()
       
        self.listadisparo = []
        self.velocidad = 20
        self.rect.top = posy
        self.rect.left = posx
        
        self.tiempoCambio = 1 
        
    def dibujar(self, superficie):
        self.imagenInvasor = self.listaEnemigos[self.posImagen]
        superficie.blit(self.imagenInvasor, self.rect)
          
    def comportamiento (self, tiempo): 
        # self.posImagen = int(tiempo % 2)
        if self.tiempoCambio == tiempo:
            self.posImagen += 1
            self.tiempoCambio +=1
            
            if self.posImagen > len(self.listaEnemigos)-1:
                self.posImagen = 0
       
def SpaceGame():
    pygame.init()
    pantalla = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Game")
    background= pygame.image.load("space_game/assets/Fondo.jpg")
    
    jugador = navespacial()
    enemigo = invasor(100,100)
    # demoproyectil = proyectil(ancho/2, alto-30) se envia al init de protetil
    enjuego = True
    reloj = pygame.time.Clock()
    
    
    
    while True:
        
        reloj.tick(180)
        tiempo = int(pygame.time.get_ticks()/1000)
        # jugador.movimiento()
        # demoproyectil.trayetoria()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if enjuego== True:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == K_LEFT:
                        jugador.movimientoizqierda()
                        
                    elif evento.key == K_RIGHT:
                        jugador.movimientoderecha()  
                        
                    elif evento.key == K_s:
                        # jugador.disparar()
                        # toma la posicion el jugador y la envia al jugador.disparar/proyectil/trayectoria
                        x,y = jugador.rect.center
                        jugador.disparar(x,y)
        
        pantalla.blit(background,(0,0))
        enemigo.comportamiento(tiempo)# le enviamos el tiempo 
        jugador.dibujar(pantalla)
        enemigo.dibujar(pantalla)
        
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