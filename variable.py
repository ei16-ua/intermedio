class Variable:
    def __init__(self, fila, col, valor_inicial='0'):
        self.fila = fila
        self.col = col
        if valor_inicial != '0':
            self.valor = int(valor_inicial)
            self.dominio = [self.valor]
            self.fija = True
        else:
            self.valor = 0
            self.dominio = list(range(1, 10))
            self.fija = False

    def set_valor(self, val):
        self.valor = val
        if not self.fija:
            self.dominio = [val]

    def reset_valor(self):
        if not self.fija:
            self.valor = 0

    def __deepcopy__(self, memo):
        nueva = Variable.__new__(Variable)
        nueva.fila = self.fila
        nueva.col = self.col
        nueva.fija = self.fija
        nueva.valor = self.valor
        nueva.dominio = list(self.dominio)
        return nueva