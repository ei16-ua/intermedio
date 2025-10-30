def _obtener_vecinos(i, j):
    vecinos = set()
    for c in range(9):
        if c != j:
            vecinos.add((i, c))
    for r in range(9):
        if r != i:
            vecinos.add((r, j))
    inicio_fila, inicio_col = 3 * (i // 3), 3 * (j // 3)
    for r in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_col, inicio_col + 3):
            if (r, c) != (i, j):
                vecinos.add((r, c))
    return list(vecinos)

def _revisar(tablero_vars, Xi, Xj):
    i1, j1 = Xi
    i2, j2 = Xj
    var_i = tablero_vars[i1][j1]
    var_j = tablero_vars[i2][j2]

    if var_i.fija:
        return False

    eliminado = False
    nuevo_dominio = []

    if var_j.fija:
        vj = var_j.valor
        for x in var_i.dominio:
            if x != vj:
                nuevo_dominio.append(x)
            else:
                eliminado = True
    else:
        for x in var_i.dominio:
            if any(y != x for y in var_j.dominio):
                nuevo_dominio.append(x)
            else:
                eliminado = True

    if eliminado:
        var_i.dominio = nuevo_dominio

    return eliminado

def ejecutar_ac3(tablero_vars):
    cola = []
    for i in range(9):
        for j in range(9):
            if not tablero_vars[i][j].fija:
                for vecino in _obtener_vecinos(i, j):
                    cola.append(((i, j), vecino))

    while cola:
        (Xi, Xj) = cola.pop(0)
        if _revisar(tablero_vars, Xi, Xj):
            i, j = Xi
            if len(tablero_vars[i][j].dominio) == 0:
                return False
            for Xk in _obtener_vecinos(i, j):
                if Xk != Xj and not tablero_vars[Xk[0]][Xk[1]].fija:
                    cola.append((Xk, Xi))
    return True