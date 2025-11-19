from arvore import No

# Constrói a árvore de Huffman
def construir_arvore(freqs):
    if not freqs or len(freqs) == 0:
        return None
    fila = []
    # O par é uma tupla (símbolo, frequência)
    #  transforma uma lista de frequencias em uma lista de nos folhas
    for par in freqs:
        s, f = par
        fila.append(No.novo_folha(s, f))
    while len(fila) > 1:
        # Ordena manualmente por freq, depois simbolo
        # bubble sort
        # se comparar none com inteiros Python dá erro

        # ordenar pelo menor freq
        # empates = menor símbolo primeiro
        # nós internos sempre vêm por último (pois usam símbolo 255)
        # Folha - simbolo = 0..255
        # Interno - simbolo = None → vira 255
        for i in range(len(fila)):
            for j in range(i+1, len(fila)):
                a = fila[i]
                b = fila[j]
                af = a.freq
                bf = b.freq
                asim = a.simbolo if a.simbolo is not None else 255
                bsim = b.simbolo if b.simbolo is not None else 255
                # Troque a e b se: a frequência de b for menor que a de a OU se as frequências forem iguais e o símbolo de b for menor.
                if (bf < af) or (bf == af and bsim < asim):
                    fila[i], fila[j] = fila[j], fila[i]
        a = fila.pop(0)
        b = fila.pop(0)
        # Junta os dois menores
        novo = No.novo_interno(a, b)
        fila.append(novo)
    return fila[0]

# Gera tabela de códigos: simbolo -> String de bits ('0' e '1')
def gerar_codigos(raiz):
    codigos = {}
    # percorre recursivamente a arvore ate chegar nas folhas
    def rec(n, prefix):
        if n.eh_folha():
            code = "0" if prefix == "" else prefix
            codigos[n.simbolo] = code
            return
        # ir para a esquerda - adiciona "0"               ir para a direita - adiciona "1"
        if n.esq is not None:
            rec(n.esq, prefix + "0")
        if n.dir is not None:
            rec(n.dir, prefix + "1")
    if raiz is not None:
        rec(raiz, "")
    return codigos


# { símbolo_ascii: "codigo_binario" }
def mostrar_codigos(cod):
    print("\nTabela de Códigos de Huffman:")
    # Ordena manualmente os codigos ascii 
    chaves = list(cod.keys())
    # bubble sort
    for i in range(len(chaves)):
        for j in range(i+1, len(chaves)):
            if chaves[j] < chaves[i]:
                chaves[i], chaves[j] = chaves[j], chaves[i]
    for k in chaves:
        if 32 <= k <= 126:
            ch = "'" + chr(k) + "'"
        else:
            ch = "0x%02X" % k
        print("%s: %s" % (ch, cod[k]))

# Converte string de caracteres '0'/'1' para vetor de bytes reais len(bits) na vdd mas de forma manual 
def bits_para_bytes(bits):
    total_bits = 0
    for _ in bits:
        total_bits += 1
    out = []
    cur = 0
    cnt = 0
    for ch in bits:
        cur = ((cur << 1) | (1 if ch == '1' else 0)) & 0xFF
        cnt += 1
        if cnt == 8:
            out.append(cur)
            cur = 0
            cnt = 0
    if cnt > 0:
        cur = (cur << (8 - cnt)) & 0xFF
        out.append(cur)
    # Converte para bytes
    b = bytearray()
    for v in out:
        b.append(v)
    return (bytes(b), total_bits)


# Lê um bit específico do payload (vetor de bytes compactados)
def ler_bit(payload, i):
    byte_idx = i // 8
    bit_idx = 7 - (i % 8)
    return (payload[byte_idx] >> bit_idx) & 1

# Mostra a árvore visualmente no terminal
def mostrar_arvore(no, nivel):
    if no is None:
        print("(árvore vazia)")
        return
    prefix = "  " * nivel
    if no.eh_folha():
        s = no.simbolo
        #ve se é um caractere imprimível ASCII
        if 32 <= s <= 126:
            ch = "'" + chr(s) + "'"
        else:
            ch = "0x%02X" % s
        print("%s- %s (freq=%d)" % (prefix, ch, no.freq))
    else:
        print("%s+ (freq=%d)" % (prefix, no.freq))
        # primeiro imprime a subárvore esquerda
        # dps direita
        mostrar_arvore(no.esq, nivel+1)
        mostrar_arvore(no.dir, nivel+1)
