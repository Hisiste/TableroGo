import pygame
from pygame.locals import *
from sys import exit

import clases as go

mainClock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
pygame.display.set_caption("GO")

font = pygame.font.SysFont(None, 40)

click = False
quit_ = False

mesa_fondo = pygame.image.load('Entrega_final/Fondo.png')
mesa_fondo = pygame.transform.scale(mesa_fondo, (1000,1000))

# Función para colocar texto en pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def main_menu():
    click = False

    # Colocación de botones al menú
    bot_Iniciar = pygame.Rect(400, 400, 200, 100)
    bot_Instr   = pygame.Rect(400, 550, 200, 100)
    bot_Quit    = pygame.Rect(400, 700, 200, 100)

    # Creamos los objetos y dentro del `while` solamente los dibujamos :3.

    while True:
        screen.blit(mesa_fondo,(0,0))
                
        # Obteniendo las coordenadas del mouse
        mx, my = pygame.mouse.get_pos()
        
        if click:
            if bot_Iniciar.collidepoint((mx, my)):
                game()
            if bot_Instr.collidepoint((mx, my)):
                instr()
            if bot_Quit.collidepoint((mx, my)):
                pygame.quit()
                exit()

        pygame.draw.rect(screen, (255, 255, 255), bot_Iniciar)
        draw_text('Iniciar', font, (0, 0, 0), screen, 455, 440)
        pygame.draw.rect(screen, (255, 255, 255), bot_Instr)
        draw_text('Intrucciones', font, (0, 0, 0), screen, 415, 590)
        pygame.draw.rect(screen, (255, 255, 255), bot_Quit)
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

    while running:
        screen.blit(mesa_fondo, (0,0))
        draw_text('Selecciona el tamaño del tablero', font, (255, 255, 255), screen, 255, 100)
        
        # Obteniendo las coordenadas del mouse
        mx, my = pygame.mouse.get_pos()
        
        # Botones de selección de tablero
        bot_x9  = pygame.Rect(300, 400, 100, 100)
        bot_x13 = pygame.Rect(450, 400, 100, 100)
        bot_x19 = pygame.Rect(600, 400, 100, 100)
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

                
        pygame.draw.rect(screen, (255, 255, 255), bot_x9)
        draw_text('9x9', font, (0, 0, 0), screen, 325, 435)
        pygame.draw.rect(screen, (255, 255, 255), bot_x13)
        draw_text('13x13', font, (0, 0, 0), screen, 460, 435)
        pygame.draw.rect(screen, (255, 255, 255), bot_x19)
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

def dibujar_tablero(screen, size):
    if size == 9:
        dimension = 94
    elif size == 13:
        dimension = 62.5
    elif size == 19:
        dimension = 41.7
    else:
        raise ValueError("El tablero no tiene un tamaño válido.")
    
    for i in range(size-1):
        for j in range(size-1):
            x = i * dimension + 124.8
            y = j * dimension + 124.8
            s = pygame.Rect(x, y, dimension, dimension)
            pygame.draw.rect(screen,(0, 0, 0),s,2)

# def dame_espacios(screen, size):
def dame_espacios(size: int, dimension: float):
    offset = 124.8
    rects = go.np.full((size, size), None)
    for i in range(size):
        for j in range(size):
            x = i * dimension + offset - dimension/2
            y = j * dimension + offset - dimension/2
            s = pygame.Rect(x, y, dimension, dimension)
            # pygame.draw.rect(screen,(255, 0, 0),s,2)
            rects[i, j] = s

    return rects

def dibuja_en_xy(screen, figs: go.np.ndarray, x: int, y: int, size: int, dimension: float):
    offset = 124.8
    point = go.np.array((x, y)) - (offset - dimension/2)
    point = point / dimension

    if all(point < size) and all(point > 0):
        point = go.np.floor(point)
        point = go.np.int64(point)

        # pygame.draw.rect(screen, (255, 0, 0), figs[point[0], point[1]], 2)
        return figs[point[0], point[1]]

def busca_casilla(x: int, y: int, size: int, dimension: float):
    offset = 124.8
    point = go.np.array((x, y)) - (offset - dimension/2)
    point = point / dimension

    if all(point < size) and all(point > 0):
        point = go.np.floor(point)
        point = go.np.int64(point)

        return point
    else:
        return None

def partida(tablero: int):
    par = True
    offset = 124.8
    
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

    mi_tablero = go.Tablero_Go(tablero)

    negra_a_poner  = pygame.image.load(file_ficha_negra)
    negra_a_poner  = pygame.transform.scale(negra_a_poner,  (int(dimension), int(dimension)))
    negra_a_poner.set_alpha(128)
    negra_puesta   = pygame.image.load(file_ficha_negra)
    negra_puesta   = pygame.transform.scale(negra_puesta,  (int(dimension), int(dimension)))

    blanca_a_poner = pygame.image.load(file_ficha_blanca)
    blanca_a_poner = pygame.transform.scale(blanca_a_poner, (int(dimension), int(dimension)))
    blanca_a_poner.set_alpha(128)
    blanca_puesta  = pygame.image.load(file_ficha_blanca)
    blanca_puesta  = pygame.transform.scale(blanca_puesta, (int(dimension), int(dimension)))

    tab = pygame.image.load(file_tablero)
    tab = pygame.transform.scale(tab, (800,800))

    rectangulos = dame_espacios(tablero, dimension)
    click = False
    jugador = go.BLACK

    while par:
        draw_text('Partida en curso', font, (255, 255, 255), screen, 390, 50)  
        screen.blit(tab, (100,100))
        # dibujar_tablero(screen, tablero)

        # Obteniendo las coordenadas del mouse
        mx, my = pygame.mouse.get_pos()
        casilla = busca_casilla(mx, my, tablero, dimension)
        
        if casilla is not None:
            rect = rectangulos[casilla[0], casilla[1]]

            if mi_tablero.esEspacioValido(casilla[0], casilla[1], jugador):
                if jugador == go.BLACK:
                    screen.blit(negra_a_poner, (rect.left, rect.top))
                else:
                    screen.blit(blanca_a_poner, (rect.left, rect.top))
                
                if click:
                    mi_tablero.ponerFicha()
                    jugador = not jugador

        for idx, (col, list_positions) in enumerate(mi_tablero.dibujarTablero()):
            for i, j in list_positions:
                x = i * dimension + offset - dimension/2
                y = j * dimension + offset - dimension/2

                if col == go.BLACK:
                    screen.blit(negra_puesta,  (x, y))
                else:
                    screen.blit(blanca_puesta, (x, y))

                draw_text(f"{idx}", font, (255, 255, 255), screen, x +
                        dimension/3, y + dimension/4)
       
        click = False

        for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               exit()
           if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   par = False 
           if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                   click = True
                   
        pygame.display.update()
        mainClock.tick(60)
                    
main_menu()
