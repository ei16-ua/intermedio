# variable.py
# Contiene la clase Variable utilizada en los algoritmos CSP

class Variable:
    def __init__(self, fila, col, valor_inicial='0'):
        self.fila = fila
        self.col = col
        if valor_inicial != '0':
            self.valor = int(valor_inicial)
            self.dominio = [int(valor_inicial)]
            self.fija = True
        else:
            self.valor = 0  # 0 significa vacío
            self.dominio = list(range(1, 10))
            self.fija = False

    def set_valor(self, val):
        """Asigna un valor y lo pone como único en el dominio."""
        self.valor = val
        if not self.fija:
            self.dominio = [val]

    def reset_valor(self):
        """Resetea el valor a 0 y restaura el dominio si no es fija."""
        if not self.fija:
            self.valor = 0
            #self.dominio = list(range(1, 10))