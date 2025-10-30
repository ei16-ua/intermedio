# backtracking.py
#Contiene la función de algoritmo Backtracking

def _es_consistente_con_valor(tablero_vars, fila, col, valor):
    for j in range(9):
        if j != col and tablero_vars[fila][j].valor == valor:
            return False

    for i in range(9):
        if i != fila and tablero_vars[i][col].valor == valor:
            return False
        
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if (i != fila or j != col) and tablero_vars[i][j].valor == valor:
                return False
    return True

def resolver(tablero_vars, contador_valores=0, contador_variables=0):
    for i in range(9):
        for j in range(9):
            if not tablero_vars[i][j].fija and tablero_vars[i][j].valor == 0:
                var = tablero_vars[i][j]
                contador_variables += 1
                for valor in var.dominio[:]:
                    contador_valores += 1
                    if _es_consistente_con_valor(tablero_vars, i, j, valor):
                        var.valor = valor
                        solucion_encontrada, contador_valores, contador_variables = resolver(tablero_vars, contador_valores, contador_variables)
                        if solucion_encontrada:
                            return True, contador_valores, contador_variables
                        var.valor = 0
                return False, contador_valores, contador_variables
    return True, contador_valores, contador_variables

def seleccionar_variable_mrv(tablero_vars):
    min_dominio = float('inf')
    mejor_i, mejor_j = None, None
    for i in range(9):
        for j in range(9):
            var = tablero_vars[i][j]
            if not var.fija and var.valor == 0:
                if len(var.dominio) < min_dominio:
                    min_dominio = len(var.dominio)
                    mejor_i, mejor_j = i, j
                    if min_dominio == 1:
                        break
        if min_dominio == 1:
            break
    if mejor_i is None:
        return None, None
    return mejor_i, mejor_j

def resolver_mrv(tablero_vars, contador_valores=0, contador_variables=0):
    pos = seleccionar_variable_mrv(tablero_vars)
    if pos[0] is None:
        return True, contador_valores, contador_variables
    i, j = pos
    var = tablero_vars[i][j]
    contador_variables += 1
    for valor in var.dominio[:]:
        contador_valores += 1
        if _es_consistente_con_valor(tablero_vars, i, j, valor):
            var.valor = valor
            solucion_encontrada, cv, cva = resolver_mrv(tablero_vars, contador_valores, contador_variables)
            if solucion_encontrada:
                return True, cv, cva
            var.valor = 0
    return False, contador_valores, contador_variables