# backtracking.py
#Contiene la función de algoritmo Backtracking

def _es_consistente_con_valor(tablero_vars, fila, col, valor):
    """
    asas
    Verifica si un valor es consistente con las asignaciones actuales 
        en la fila, columna y subcuadrícula de (fila, col).
    :param tablero_vars: Matriz 9x9 de objetos Variable.
    :param fila: Fila de la variable a comprobar.
    :param col: Columna de la variable a comprobar.
    :param valor: Valor a probar.
    :return: True si es consistente, False en caso contrario.
    """
    for j in range(9):
        if j != col and tablero_vars[fila][j].valor == valor:
            return False

    for i in range(9):
        if i != fila and tablero_vars[i][col].valor == valor:
            return False
        
    # Comprobar subcuadrícula 3x3
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if (i != fila or j != col) and tablero_vars[i][j].valor == valor:
                return False
    return True

def resolver(tablero_vars, contador_valores=0, contador_variables=0):
    """
    Algoritmo de Backtracking para resolver el CSP del Sudoku.
    :param tablero_vars: Matriz 9x9 de objetos Variable.
    :param contador_valores: Número de valores probados hasta ahora.
    :param contador_variables: Número de variables seleccionadas para asignar hasta ahora.
    :return: (True, contador_valores_final, contador_variables_final) si encuentra 
            una solución, (False, contador_valores_final, contador_variables_final) 
            en caso contrario.
    """
    for i in range(9):
        for j in range(9):
            if not tablero_vars[i][j].fija and tablero_vars[i][j].valor == 0:
                var = tablero_vars[i][j]
                contador_variables += 1
                for valor in var.dominio[:]:
                    contador_valores += 1
                    if _es_consistente_con_valor(tablero_vars, i, j, valor):
                        var.set_valor(valor)
                        solucion_encontrada, contador_valores, contador_variables = resolver(tablero_vars, contador_valores, contador_variables)
                        if solucion_encontrada:
                            return True, contador_valores, contador_variables
                        var.reset_valor()
                return False, contador_valores, contador_variables
    return True, contador_valores, contador_variables