# Conta frequências e retorna vetor ordenado por símbolo (para garantir ordem determinística)
def contar_frequencias(dados):
    mapa = {}
    for b in dados:
        if b in mapa:
            mapa[b] += 1
        else:
            mapa[b] = 1
    itens = []
    for k in mapa:
        itens.append((k, mapa[k]))
    # Ordena pelo símbolo
    for i in range(len(itens)):
        for j in range(i+1, len(itens)):
            if itens[j][0] < itens[i][0]:
                itens[i], itens[j] = itens[j], itens[i]
    return itens

def mostrar_frequencias(freqs):
    print("\nTabela de Frequências:")
    for par in freqs:
        s, f = par
        if 32 <= s <= 126:
            ch = "'" + chr(s) + "'"
        else:
            ch = "0x%02X" % s
        print("%s: %d" % (ch, f))
