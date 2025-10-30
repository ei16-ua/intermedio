import sys
import time
import copy
from tablero import Tablero
from variable import Variable
from backtracking import resolver as resolver_bt, resolver_mrv as resolver_bt_mrv
from forward_checking import resolver as resolver_fc, resolver_mrv as resolver_fc_mrv
from ac3 import ejecutar_ac3


def crear_tablero_vars(tablero):
    vars_mat = []
    for i in range(9):
        fila = []
        for j in range(9):
            val = tablero.getCelda(i, j)
            fila.append(Variable(i, j, val))
        vars_mat.append(fila)
    return vars_mat


def vars_a_solucion(tablero_vars):
    return [''.join(str(var.valor) for var in fila) for fila in tablero_vars]


def imprimir_solucion(solucion, titulo):
    print(f"\n{titulo}")
    print("-" * 21)
    for i, fila in enumerate(solucion):
        if i in (3, 6):
            print("------+-------+------")
        line = " ".join([
            " ".join(fila[0:3]),
            " ".join(fila[3:6]),
            " ".join(fila[6:9])
        ])
        print(line)


def ejecutar_algoritmo(nombre, resolver_func, tablero_vars):
    inicio = time.time()
    copia = copy.deepcopy(tablero_vars)
    exito, valores, variables = resolver_func(copia, 0, 0)
    tiempo = (time.time() - inicio) * 1000  # ms
    if exito:
        solucion = vars_a_solucion(copia)
        return True, solucion, tiempo, valores, variables
    else:
        return False, None, tiempo, valores, variables


def ejecutar_ac3_mas_algoritmo(nombre, resolver_func, tablero_original):
    tablero_vars = crear_tablero_vars(tablero_original)
    if not ejecutar_ac3(tablero_vars):
        return False, None, 0, 0, 0, True  # inconsistente

    inicio = time.time()
    exito, valores, variables = resolver_func(tablero_vars, 0, 0)
    tiempo = (time.time() - inicio) * 1000
    if exito:
        solucion = vars_a_solucion(tablero_vars)
        return True, solucion, tiempo, valores, variables, False
    else:
        return False, None, tiempo, valores, variables, False


def main():
    mapas = [f"m{i}.txt" for i in range(1, 7)]
    print("📊 PRUEBAS COMPLETAS: BK, FC, con/sin MRV, con/sin AC3")
    print("=" * 70)

    for mapa in mapas:
        print(f"\n\n🧪 === {mapa} ===")
        try:
            tablero = Tablero(mapa)
        except Exception as e:
            print(f"  ❌ Error al cargar {mapa}: {e}")
            continue

        tablero_vars = crear_tablero_vars(tablero)

        # --- 1. BK (sin MRV) ---
        exito1, sol1, t1, v1, var1 = ejecutar_algoritmo("BK", resolver_bt, tablero_vars)

        # --- 2. BK + MRV ---
        exito2, sol2, t2, v2, var2 = ejecutar_algoritmo("BK+MRV", resolver_bt_mrv, tablero_vars)

        # --- 3. FC (sin MRV) ---
        exito3, sol3, t3, v3, var3 = ejecutar_algoritmo("FC", resolver_fc, tablero_vars)

        # --- 4. FC + MRV ---
        exito4, sol4, t4, v4, var4 = ejecutar_algoritmo("FC+MRV", resolver_fc_mrv, tablero_vars)

        # --- 5. AC3 + BK+MRV ---
        exito5, sol5, t5, v5, var5, inc5 = ejecutar_ac3_mas_algoritmo("AC3+BK", resolver_bt_mrv, tablero)

        # --- 6. AC3 + FC+MRV ---
        exito6, sol6, t6, v6, var6, inc6 = ejecutar_ac3_mas_algoritmo("AC3+FC", resolver_fc_mrv, tablero)

        # Mostrar solución (usamos FC+MRV como representante si existe)
        solucion_mostrada = False
        for sol in [sol4, sol6, sol2, sol1, sol3, sol5]:
            if sol is not None:
                imprimir_solucion(sol, f"✅ Solución de {mapa}")
                solucion_mostrada = True
                break
        if not solucion_mostrada:
            print("  ❌ Ningún algoritmo encontró solución.")

        # --- Tabla de resultados ---
        print(f"\n📈 Resultados de rendimiento:")
        print(f"{'Algoritmo':<16} {'Tiempo (ms)':<12} {'Valores':<10} {'Variables':<10} {'Estado':<10}")
        print("-" * 65)

        def fmt_row(nombre, exito, t, v, var, inconsistente=False):
            if inconsistente:
                estado = "INCONSISTENTE"
                return f"{nombre:<16} {'-':<12} {'-':<10} {'-':<10} {estado:<10}"
            elif not exito:
                estado = "FALLÓ"
                return f"{nombre:<16} {t:<12.2f} {v:<10} {var:<10} {estado:<10}"
            else:
                return f"{nombre:<16} {t:<12.2f} {v:<10} {var:<10} {'OK':<10}"

        print(fmt_row("BK", exito1, t1, v1, var1))
        print(fmt_row("BK+MRV", exito2, t2, v2, var2))
        print(fmt_row("FC", exito3, t3, v3, var3))
        print(fmt_row("FC+MRV", exito4, t4, v4, var4))
        if inc5:
            print(fmt_row("AC3+BK+MRV", False, 0, 0, 0, True))
        else:
            print(fmt_row("AC3+BK+MRV", exito5, t5, v5, var5))
        if inc6:
            print(fmt_row("AC3+FC+MRV", False, 0, 0, 0, True))
        else:
            print(fmt_row("AC3+FC+MRV", exito6, t6, v6, var6))

    print("\n✅ Todas las pruebas han finalizado.")


if __name__ == "__main__":
    main()