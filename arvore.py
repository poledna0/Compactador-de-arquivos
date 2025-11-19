class No:
    # construtor
    def __init__(self, freq, simbolo=None, esq=None, dir=None):
        self.freq = freq
        self.simbolo = simbolo
        self.esq = esq
        self.dir = dir
# n recebe self automaticamente
    @staticmethod
    def novo_folha(sim, freq):
        return No(freq, sim, None, None)

# n recebe self automaticamente
    @staticmethod
    def novo_interno(esq, dir):
        return No(esq.freq + dir.freq, None, esq, dir)

    def eh_folha(self):
        return self.simbolo is not None
