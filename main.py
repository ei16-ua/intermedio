#########################################################################
# CURSO 25-25
# PRACTICA 1 DE SISTEMAS INTELIGENTES: RESOLUCION DE SUDOKUS
#########################################################################   

import pygame
import copy
from tablero import *
from pygame.locals import *
import sys

from variable import Variable
from backtracking import resolver as resolver_bt
from forward_checking import resolver as resolver_fc

GREY=(220,220,220)
NEGRO=(10,10,10)
GRIS_ACTIVO=(245,245,245)
GRIS_NORMAL=(169,169,169)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_DERECHO=125 #ancho del margen derecho entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
N=9 # número de filas del sudoku
VACIA='0'

#########################################################################
# Detecta si se pulsa un botón
#########################################################################   
def pulsaBoton(pos, boton):
    if boton.collidepoint(pos[0], pos[1]):    
        return True
    else:
        return False

#########################################################################
# Pintar un boton
#########################################################################   
def pintarBoton(screen, fuenteBot, boton, mensaje):
    if boton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, GRIS_ACTIVO, boton, 0)        
    else:
        pygame.draw.rect(screen, GRIS_NORMAL, boton, 0)
        
    texto=fuenteBot.render(mensaje, True, NEGRO)
    screen.blit(texto, (boton.x+(boton.width-texto.get_width())/2, boton.y+(boton.height-texto.get_height())/2))         

#########################################################################
# Pintar el sudoku
#########################################################################         
def pintarTablero(screen, fuenteSud, tablero, copTab):
    pygame.draw.rect(screen, GREY, [0, 0, N*(TAM+MARGEN)+MARGEN, N*(TAM+MARGEN)+MARGEN],0)
    for fil in range(9):
        for col in range(9):
            if tablero is None or tablero.getCelda(fil, col)==VACIA :
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)            
            else:
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                if tablero.getCelda(fil, col)==copTab.getCelda(fil, col):
                    color=NEGRO
                else:
                    color=GRIS_NORMAL                 
                texto= fuenteSud.render(tablero.getCelda(fil, col), True, color)            
                screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])
    
    #dibujar línea de cuadrícula     
    pygame.draw.line(screen, GRIS_NORMAL, (MARGEN, 3*(TAM+MARGEN)+2), (9*(TAM+MARGEN),3*(TAM+MARGEN)+2), 5)
    pygame.draw.line(screen, GRIS_NORMAL, (MARGEN, 6*(TAM+MARGEN)+2), (9*(TAM+MARGEN),6*(TAM+MARGEN)+2), 5)    
    pygame.draw.line(screen, GRIS_NORMAL, (3*(TAM+MARGEN)+2,MARGEN), (3*(TAM+MARGEN)+2,9*(TAM+MARGEN)), 5)
    pygame.draw.line(screen, GRIS_NORMAL, (6*(TAM+MARGEN)+2, MARGEN), (6*(TAM+MARGEN)+2,9*(TAM+MARGEN)), 5)
    pygame.draw.rect(screen, GRIS_NORMAL, [MARGEN, MARGEN, N*(TAM+MARGEN), N*(TAM+MARGEN)],5)


#########################################################################  
# Principal
#########################################################################
def main():    
    
    pygame.init()
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='m1.txt'
    else:
        file=sys.argv[-1]
    
    anchoVentana=N*(TAM+MARGEN)+MARGEN_DERECHO
    altoVentana= N*(TAM+MARGEN)+2*MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Sudoku") 
    
    fuenteBot=pygame.font.Font(None, 30)
    fuenteSud= pygame.font.Font(None, 70)
    
    botLoad=pygame.Rect(anchoVentana-95, 75, 70, 50)    
    botBK=pygame.Rect(anchoVentana-95, 203, 70, 50)
    botFC=pygame.Rect(anchoVentana-95, 333, 70, 50)
    botAC3=pygame.Rect(anchoVentana-95, 463, 70, 50)
    
    game_over=False
    tablero=None
    copTab=None
    
    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición                               
                pos=pygame.mouse.get_pos()
                if pulsaBoton(pos, botLoad):                                      
                    tablero=Tablero(file)
                    copTab=copy.deepcopy(tablero)                                    
                if pulsaBoton(pos, botBK):                    
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:
                        print("BK")

                    tablero_vars = []
                    for i in range(9):
                        fila_vars = []
                        for j in range(9):
                            val_inicial = tablero.getCelda(i, j)
                            fila_vars.append(Variable(i, j, val_inicial))
                        tablero_vars.append(fila_vars)

                    # 2. Llamar al algoritmo de backtracking (desde backtracking.py)
                    exito, contador_valores_final, contador_variables_final = resolver_bt(tablero_vars, 0, 0)
                    if exito:
                        print(f"Solución encontrada por Backtracking.")
                        print(f"  - Valores probados: {contador_valores_final}")
                        print(f"  - Variables exploradas: {contador_variables_final}")
                        for i in range(9):
                            for j in range(9):
                                if not tablero_vars[i][j].fija:  
                                    tablero.setCelda(i, j, str(tablero_vars[i][j].valor))
                    else:
                        print(f"No se encontró solución por Backtracking.")
                        print(f"  - Valores probados: {contador_valores_final}")
                        print(f"  - Variables exploradas: {contador_variables_final}")
                elif pulsaBoton(pos, botFC):                    
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:
                        print("FC")

                        tablero_vars = []
                        for i in range(9):
                            fila_vars = []
                            for j in range(9):
                                val_inicial = tablero.getCelda(i, j)
                                fila_vars.append(Variable(i, j, val_inicial))
                            tablero_vars.append(fila_vars)
                        
                        exito, contador_valores_final, contador_variables_final = resolver_fc(tablero_vars, 0, 0)
                        if exito:
                            print(f"Solución encontrada por Forward Checking.")
                            print(f"  - Valores probados: {contador_valores_final}")
                            print(f"  - Variables exploradas: {contador_variables_final}")
                            for i in range(9):
                                for j in range(9):
                                    if not tablero_vars[i][j].fija:  # Solo actualizar las no fijas
                                        tablero.setCelda(i, j, str(tablero_vars[i][j].valor))
                        else:
                            print(f"No se encontró solución por Forward Checking.")
                            print(f"  - Valores probados: {contador_valores_final}")
                            print(f"  - Variables exploradas: {contador_variables_final}")
                elif pulsaBoton(pos, botAC3):
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:                        
                        print("AC3")                        
                        #aquí llamar al AC3    
               
        #limpiar pantalla
        screen.fill(GREY)
        #pintar cuadrícula del sudoku  
        pintarTablero(screen, fuenteSud, tablero, copTab)                   
        #pintar botones        
        pintarBoton(screen, fuenteBot, botLoad, "Load")
        pintarBoton(screen, fuenteBot, botBK, "BK")
        pintarBoton(screen, fuenteBot, botFC, "FC")
        pintarBoton(screen, fuenteBot, botAC3, "AC3")        
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
 
