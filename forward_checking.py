# forward_checking.py
# Contiene la función de algoritmo Forward Checking

from backtracking import _es_consistente_con_valor

def _propagar_dominios(tablero_vars, fila, col, valor_asignado):
    dominios_eliminados = {}
    consistent = True

    for j in range(9):
        if not tablero_vars[fila][j].fija and tablero_vars[fila][j].valor == 0:
            if valor_asignado in tablero_vars[fila][j].dominio:
                if (fila, j) not in dominios_eliminados:
                     dominios_eliminados[(fila, j)] = []
                dominios_eliminados[(fila, j)].append(valor_asignado)
                tablero_vars[fila][j].dominio.remove(valor_asignado)
                if len(tablero_vars[fila][j].dominio) == 0:
                    consistent = False
                    break

    if not consistent:
        return dominios_eliminados, consistent

    for i in range(9):
        if not tablero_vars[i][col].fija and tablero_vars[i][col].valor == 0:
            if valor_asignado in tablero_vars[i][col].dominio:
                if (i, col) not in dominios_eliminados:
                     dominios_eliminados[(i, col)] = []
                dominios_eliminados[(i, col)].append(valor_asignado)
                tablero_vars[i][col].dominio.remove(valor_asignado)
                if len(tablero_vars[i][col].dominio) == 0:
                    consistent = False
                    break

    if not consistent:
        return dominios_eliminados, consistent
    
    # Comprobar subcuadrícula 3x3
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for r in range(inicio_fila, inicio_fila + 3):
        for s in range(inicio_col, inicio_col + 3):
            if not tablero_vars[r][s].fija and tablero_vars[r][s].valor == 0:
                if valor_asignado in tablero_vars[r][s].dominio:
                    if (r, s) not in dominios_eliminados:
                         dominios_eliminados[(r, s)] = []
                    dominios_eliminados[(r, s)].append(valor_asignado)
                    tablero_vars[r][s].dominio.remove(valor_asignado)
                    if len(tablero_vars[r][s].dominio) == 0:
                        consistent = False
                        break
        if not consistent:
            break

    return dominios_eliminados, consistent


def _restaurar_dominios(tablero_vars, dominios_eliminados):
    for (f, c), vals in dominios_eliminados.items():
        for v in vals:
            if v not in tablero_vars[f][c].dominio:
                tablero_vars[f][c].dominio.append(v)

def resolver(tablero_vars, contador_valores=0, contador_variables=0):
    for i in range(9):
        for j in range(9):
            #not tablero_vars[i][j].fija and
            if  tablero_vars[i][j].valor == 0:
                var_actual = tablero_vars[i][j]
                contador_variables += 1
                # Iterar sobre una copia del dominio ACTUAL (reducido por AC3 o podas previas)
                for valor in var_actual.dominio[:]:
                    contador_valores += 1
                    if _es_consistente_con_valor(tablero_vars, i, j, valor):
                        # Asignar SOLO el valor, NO modificar el dominio de la variable actual
                        var_actual.valor = valor
                        dominios_eliminados, consistent = _propagar_dominios(tablero_vars, i, j, valor)
                        if consistent:
                            solucion_encontrada, contador_valores, contador_variables = resolver(tablero_vars, contador_valores, contador_variables)
                            if solucion_encontrada:
                                return True, contador_valores, contador_variables
                        # Restaurar dominios de variables futuras
                        _restaurar_dominios(tablero_vars, dominios_eliminados)
                        # Desasignar la variable actual
                        var_actual.valor = 0
                return False, contador_valores, contador_variables
    return True, contador_valores, contador_variables


from backtracking import seleccionar_variable_mrv

def resolver_mrv(tablero_vars, contador_valores=0, contador_variables=0):
    pos = seleccionar_variable_mrv(tablero_vars)
    if pos[0] is None:
        return True, contador_valores, contador_variables
    i, j = pos
    var = tablero_vars[i][j]
    contador_variables += 1
    for valor in var.dominio[:]:
        contador_valores += 1
        var.valor = valor
        dominios_eliminados, consistent = _propagar_dominios(tablero_vars, i, j, valor)
        if consistent:
            solucion_encontrada, cv, cva = resolver_mrv(tablero_vars, contador_valores, contador_variables)
            if solucion_encontrada:
                return True, cv, cva
        _restaurar_dominios(tablero_vars, dominios_eliminados)
        var.valor = 0
    return False, contador_valores, contador_variables