import pygame
import time
import threading
# import math
from pygame.locals import *
from sys import exit
import clases as go

mainClock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("GO")
global segundos
global minutos
segundos = 0
minutos = 0

font = pygame.font.SysFont(None, 40)

click = False
quit_ = False

# Cargando elementos de imagen
mesa_fondo = pygame.image.load('Entrega_final/Fondo.jpg')
mesa_fondo = pygame.transform.scale(mesa_fondo, (1000, 1000))
bot_largo  = pygame.image.load('Entrega_final/Botón Largo.png')
bot_largo  = pygame.transform.scale(bot_largo, (200,100))
bot_corto  = pygame.image.load('Entrega_final/Botón corto.png')
bot_corto  = pygame.transform.scale(bot_corto, (100,100))

# Función para colocar texto en pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    click = False

    screen = pygame.display.set_mode((1000, 1000))

    # Creación de botones al menú
    bot_Iniciar = pygame.Rect(400, 400, 200, 100)
    bot_Instr   = pygame.Rect(400, 550, 200, 100)
    bot_Quit    = pygame.Rect(400, 700, 200, 100)

    # Creamos los objetos y dentro del `while` solamente los dibujamos :3.

    while True:

        # Dibujando los botones en la pantalla
        pygame.draw.rect(screen, (255, 255, 255), bot_Iniciar)
        pygame.draw.rect(screen, (255, 255, 255), bot_Instr)
        pygame.draw.rect(screen, (255, 255, 255), bot_Quit)
        screen.blit(mesa_fondo,(0,0))
                
        # Obteniendo las coordenadas del mouse
        mx, my = pygame.mouse.get_pos()
        
        # Creando los eventos de colisión y click

        if click:
            if bot_Iniciar.collidepoint((mx, my)):
                game()
            if bot_Instr.collidepoint((mx, my)):
                instr()
            if bot_Quit.collidepoint((mx, my)):
                pygame.quit()
                exit()

        # Colocando por encima de los botones sus imagenes y textos
        screen.blit(bot_largo,(400,400))
        draw_text('Iniciar', font, (0, 0, 0), screen, 455, 440)
        screen.blit(bot_largo,(400,550))
        draw_text('Intrucciones', font, (0, 0, 0), screen, 415, 590)
        screen.blit(bot_largo,(400,700))
        draw_text('Salir', font, (0, 0, 0), screen, 465,740)
        
        click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            
        pygame.display.update()
        mainClock.tick(60)

def game():
    running = True
    click = False

    screen = pygame.display.set_mode((1000, 1000))

    # Creando los botones de selección de tablero
    bot_x9  = pygame.Rect(300, 400, 100, 100)
    bot_x13 = pygame.Rect(450, 400, 100, 100)
    bot_x19 = pygame.Rect(600, 400, 100, 100)

    while running:
        
        # Obteniendo las coordenadas del mouse
        mx, my = pygame.mouse.get_pos()
        
        # Colocando los botones de selección de tablero
        pygame.draw.rect(screen, (255, 255, 255), bot_x9)
        pygame.draw.rect(screen, (255, 255, 255), bot_x13)
        pygame.draw.rect(screen, (255, 255, 255), bot_x19)
        screen.blit(mesa_fondo,(0,0))

        draw_text('Selecciona el tamaño del tablero', font, (255, 255, 255), screen, 255, 100)

        # Creando los eventos de colisión y de click

        if click:
            if bot_x9.collidepoint((mx, my)):
                tablero = 9
                partida(tablero)
            elif bot_x13.collidepoint((mx, my)):
                tablero = 13
                partida(tablero)
            elif bot_x19.collidepoint((mx, my)):
                tablero = 19
                partida(tablero)

                
        screen.blit(bot_corto,(300,400))
        draw_text('9x9', font, (0, 0, 0), screen, 325, 435)
        screen.blit(bot_corto,(450,400))
        draw_text('13x13', font, (0, 0, 0), screen, 460, 435)
        screen.blit(bot_corto,(600,400))
        draw_text('19x19', font, (0, 0, 0), screen, 610, 435)
        
        
        click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        pygame.display.update()
        mainClock.tick(60)

def instr():
    instructions = True
    
    while instructions:
        draw_text('INSTRUCCIONES DE GO', font, (255, 255, 255), screen, 350, 100)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    instructions = False
        
        pygame.display.update()
        mainClock.tick(60)


def dame_espacios(size: int, dimension: float, offset: float):
    rects = go.np.full((size, size), None)

    for i in range(size):
        for j in range(size):
            x = i * dimension + offset - dimension/2
            y = j * dimension + offset - dimension/2
            rects[i, j] = (x, y)

    return rects

def busca_casilla(x: int, y: int, size: int, dimension: float, offset: float):
    point = go.np.array((x, y)) - (offset - dimension/2)
    point = point / dimension

    if all(point < size) and all(point > 0):
        point = go.np.floor(point)
        point = go.np.int64(point)

        return point
    else:
        return None

def crono():
  global segundos
  global minutos
  segundos = int(segundos)
  minutos = int(minutos)
  if segundos == 59:
    segundos = 0
    minutos += 1
    return crono()
  else:
    segundos +=1
    time.sleep(1)
    return crono()

def partida(tablero: int):
    par        = True
    click      = False
    jugador    = go.BLACK
    offset     = 124.8
    casillaAnt = go.np.array([])
    ultimaFich = go.np.array([])
    
    # Creando un hilo que se encargue de mantener el cronómetro
    hilo = threading.Thread(target=crono, args=())
    hilo.start()
    
    mesa_fondo = pygame.image.load('Entrega_final/Fondo.jpg')
    mesa_fondo = pygame.transform.scale(mesa_fondo, (1500, 1000))
    screen     = pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
    bot_largo  = pygame.image.load('Entrega_final/Botón Largo.png')
    bot_largo  = pygame.transform.scale(bot_largo, (500,250))

    file_ficha_negra  = 'Entrega_final/Ficha negra.png'
    file_ficha_blanca = 'Entrega_final/Ficha blanca.png'

    if tablero == 9:
        file_tablero = 'Entrega_final/Tablero 9x9.png'
        dimension = 94
    elif tablero == 13:
        file_tablero = 'Entrega_final/Tablero 13x13.png'
        dimension = 62.5
    elif tablero == 19:
        dimension = 41.7
        file_tablero = 'Entrega_final/Tablero 19x19.png'
    else:
        raise AssertionError("El tablero no tiene un tamaño válido.")

    # Cargamos las imágenes de las fichas y el tablero, y escalamos conforme nos
    # convenga.
    negra_puesta   = pygame.image.load(file_ficha_negra)
    negra_puesta   = pygame.transform.scale(negra_puesta,  (int(dimension), int(dimension)))
    negra_a_poner  = negra_puesta.copy()
    negra_a_poner.set_alpha(128)

    blanca_puesta  = pygame.image.load(file_ficha_blanca)
    blanca_puesta  = pygame.transform.scale(blanca_puesta, (int(dimension), int(dimension)))
    blanca_a_poner = blanca_puesta.copy()
    blanca_a_poner.set_alpha(128)

    tab = pygame.image.load(file_tablero)
    tab = pygame.transform.scale(tab, (800,800))

    # Calculamos los espacios de las fichas en el tablero e inicializamos la
    # clase `Tablero_Go`.
    rectangulos = dame_espacios(tablero, dimension, offset)
    mi_tablero = go.Tablero_Go(tablero)

    while par:
        draw_text('Partida en curso', font, (255, 255, 255), screen, 390, 50)  
        screen.blit(mesa_fondo,(0,0))
        screen.blit(tab, (100,100))
        screen.blit(bot_largo,(950 ,100))
        # dibujar_tablero(screen, tablero)

        # Iniciando el cronómetro de la partida
        
        global segundos
        global minutos
        segundos = int(segundos)
        minutos = int(minutos)

        if segundos <= 9:
          segundos = '0' + str(segundos)
        else:
          segundos = str(segundos)

        if minutos <= 9:
          minutos  = '0' + str(minutos)
        else:
          minutos  = str(minutos)

        draw_text(str(minutos) + ' :', font, (255, 255, 255), screen, 1160, 125)
        draw_text(str(segundos), font, (255, 255, 255), screen, 1215, 125)

        # Obteniendo las coordenadas del mouse
        mx, my = pygame.mouse.get_pos()
        casilla = busca_casilla(mx, my, tablero, dimension, offset)
        
        # En caso de que el mouse esté sobre una casilla válida del tablero.
        if casilla is not None:
            # Veamos si la casilla es jugable. Esto es, el jugador puede poner
            # una ficha en la casilla donde está el mouse.
            if go.np.array_equal(casillaAnt, casilla) or mi_tablero.esEspacioValido(casilla[0], casilla[1], jugador):
                casillaAnt = casilla.copy()
                espacio = rectangulos[casilla[0], casilla[1]]

                if jugador == go.BLACK:
                    screen.blit(negra_a_poner,  (espacio[0], espacio[1]))
                else:
                    screen.blit(blanca_a_poner, (espacio[0], espacio[1]))
                
                # Si el jugador hizo click, ponemos la ficha en el tablero.
                if click:
                    mi_tablero.ponerFicha()
                    # Cambiamos de jugador
                    jugador = not jugador
                    ultimaFich = go.np.array([espacio[0], espacio[1]])

        # Dibujamos las fichas tomándolas directamente del tablero.
        for col, list_positions in mi_tablero.dibujarTablero():
            for i, j in list_positions:
                espacio = rectangulos[i, j]

                if col == go.BLACK:
                    screen.blit(negra_puesta,  (espacio[0], espacio[1]))
                else:
                    screen.blit(blanca_puesta, (espacio[0], espacio[1]))

                # draw_text(f"{idx}", font, (255, 255, 255), screen, x +
                        # dimension/3, y + dimension/4)

        # Dibujamos un rectángulo rojo sobre la última ficha que fue puesta en
        # el tablero.
        if len(ultimaFich) > 0:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(ultimaFich[0] +
                dimension/4, ultimaFich[1] + dimension/4, dimension/2, dimension/2), 2)

        click = False

        for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               exit()
           if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   par = False
                   game() 
           if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                   click = True

        pygame.display.update()
        mainClock.tick(60)
