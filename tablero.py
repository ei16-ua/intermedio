# Representa el sudoku
class Tablero:    
    def __init__(self, archivo):
        self.tam=9           
        self.tablero=leer(archivo)        
         
    def __str__(self):
        salida=""
        for f in range(self.tam):            
            for c in range(self.tam):
                salida += self.tablero[f][c]                
            salida += "\n"
        return salida
       
    def reset(self):
        for f in range(self.tam):
            for c in range(self.tam):
                self.tablero[f][c]='0'      
       
   
    
    def getCelda(self, fila, col):
        return self.tablero[fila][col]
    
    def setCelda(self, fila, col, val):
        self.tablero[fila][col]=val
        
    def getTablero(self):
        return self.tablero
    
        
def leer(archivo):
    tablero=[]
    
    try:  
        fich=open(archivo, "r")
        
        fila=-1
        for cadena in fich:            
            fila=fila+1            
            tablero.append([])            
            valores=cadena.split() 
            for i in range(9):                
                if valores[i] == '0':                    
                    tablero[fila].append('0')
                else:
                    tablero[fila].append(valores[i])
                
    except:
        print ("Error de fichero")
        fich.close()
    
    fich.close()
   
    return (tablero)
    
    
