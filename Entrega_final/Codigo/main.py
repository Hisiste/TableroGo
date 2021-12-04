import pygame
from pygame.locals import *
from sys import exit

mainClock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
pygame.display.set_caption("GO")

font = pygame.font.SysFont(None, 40)

click = False
quit_ = False

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

    mesa_fondo = pygame.image.load('Entrega_final/Fondo.png')
    mesa_fondo = pygame.transform.scale(mesa_fondo, (1000,1000))
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
        dimension = 63
    elif size == 19:
        dimension = 42
    else:
        raise ValueError("El tablero no tiene un tamaño válido.")
    
    for i in range(size-1):
        for j in range(size-1):
            x = i * dimension + 124.8
            y = j * dimension + 124.8
            s = pygame.Rect(x, y, dimension, dimension)
            pygame.draw.rect(screen,(0, 0, 0),s,2)
    

def partida(tablero):
    par = True
    
    tab = pygame.image.load('Entrega_final/Tablero.png')
    tab = pygame.transform.scale(tab, (800,800))

    while par:
        draw_text('Partida en curso', font, (255, 255, 255), screen, 390, 50)  
        screen.blit(tab, (100,100))
        dibujar_tablero(screen, tablero)
       
        for event in pygame.event.get():
           if event.type == QUIT:
               pygame.quit()
               exit()
           if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   par = False 
                   
        pygame.display.update()
        mainClock.tick(60)
                    
main_menu()
