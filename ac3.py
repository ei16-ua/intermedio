def _obtener_vecinos(fila, col):
    """Devuelve lista de (f, c) que están en misma fila, columna o subcuadrícula."""
    vecinos = set()
    # Misma fila
    for j in range(9):
        if j != col:
            vecinos.add((fila, j))
    # Misma columna
    for i in range(9):
        if i != fila:
            vecinos.add((i, col))
    # Subcuadrícula
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if (i, j) != (fila, col):
                vecinos.add((i, j))
    return list(vecinos)

def _revisar(tablero_vars, Xi, Xj):
    """
    Revisa el arco (Xi -> Xj): elimina de dominio de Xi cualquier valor que no tenga soporte en Xj.
    Devuelve True si se eliminó al menos un valor del dominio de Xi.
    """
    i1, j1 = Xi
    i2, j2 = Xj
    var_i = tablero_vars[i1][j1]
    var_j = tablero_vars[i2][j2]

    if var_i.fija or var_j.fija:
        return False

    dominio_nuevo = []
    revisado = False

    for x in var_i.dominio:
        # ¿Existe al menos un y en dominio de Xj tal que x != y?
        if any(x != y for y in var_j.dominio):
            dominio_nuevo.append(x)
        else:
            revisado = True  # x no tiene soporte → se elimina

    if revisado:
        var_i.dominio = dominio_nuevo

    return revisado

def ejecutar_ac3(tablero_vars):
    """
    Ejecuta el algoritmo AC3 sobre el tablero.
    :param tablero_vars: Matriz 9x9 de objetos Variable.
    :return: True si no hay dominios vacíos (consistente), False si hay inconsistencia.
    """
    # Inicializar cola Q con todos los arcos (Xi, Xj) donde Xi y Xj están restringidos
    cola = []
    for i in range(9):
        for j in range(9):
            if not tablero_vars[i][j].fija:
                vecinos = _obtener_vecinos(i, j)
                for (ni, nj) in vecinos:
                    cola.append(((i, j), (ni, nj)))

    while len(cola) > 0:
        # Seleccionar y borrar el primer arco de la cola (FIFO)
        (Xi, Xj) = cola.pop(0)
        if _revisar(tablero_vars, Xi, Xj):
            i, j = Xi
            if len(tablero_vars[i][j].dominio) == 0:
                return False  # Inconsistencia
            # Añadir arcos (Xk, Xi) para todos los vecinos Xk de Xi (excepto Xj)
            vecinos_Xi = _obtener_vecinos(i, j)
            for Xk in vecinos_Xi:
                if Xk != Xj and not tablero_vars[Xk[0]][Xk[1]].fija:
                    cola.append((Xk, Xi))

    return True