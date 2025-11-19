"""
Módulo de operações de I/O para compactar e descompactar arquivos (.huff)
"""
import struct
from frequencia import contar_frequencias
from codificacao import construir_arvore, gerar_codigos, bits_para_bytes, ler_bit

def existe_arquivo(caminho):
    try:
        f = open(caminho, 'rb')
        f.close()
        return True
    except:
        return False

def pega_nome_saida(caminho):
    # Remove extensão se houver
    base = caminho
    ponto = -1
    for i in range(len(caminho)):
        if caminho[i] == '.':
            ponto = i
    if ponto != -1:
        base = caminho[:ponto]
    return base

def compactar(caminho):
    if not existe_arquivo(caminho):
        print("Erro: Arquivo não encontrado.")
        return
    f = open(caminho, 'rb')
    dados = f.read()
    f.close()
    if len(dados) == 0:
        print("Aviso: O arquivo está vazio.")
        return
    freqs = contar_frequencias(dados)
    raiz = construir_arvore(freqs)
    codigos = gerar_codigos(raiz)
    bits = ""
    for b in dados:
        bits += codigos[b]
    payload_bytes, qtd_bits = bits_para_bytes(bits)
    saida = caminho + ".huff"
    out = open(saida, 'wb')
    out.write(b"HUFF")
    out.write(struct.pack('<I', len(freqs)))
    for par in freqs:
        s, freq = par
        out.write(struct.pack('B', s))
        out.write(struct.pack('<Q', freq))
    out.write(struct.pack('<Q', qtd_bits))
    out.write(payload_bytes)
    out.close()
    print("Sucesso! Arquivo compactado gerado: %s" % saida)
    print("Detalhes: %d bytes de payload, total de %d bits." % (len(payload_bytes), qtd_bits))

def descompactar(caminho):
    if not existe_arquivo(caminho):
        print("Erro: Arquivo não encontrado.")
        return
    f = open(caminho, 'rb')
    magic = f.read(4)
    if magic != b"HUFF":
        print("Erro: Arquivo inválido (assinatura 'HUFF' não encontrada).")
        f.close()
        return
    num_simbolos = struct.unpack('<I', f.read(4))[0]
    freqs = []
    for _ in range(num_simbolos):
        simb = struct.unpack('B', f.read(1))[0]
        freq = struct.unpack('<Q', f.read(8))[0]
        freqs.append((simb, freq))
    qtd_bits = struct.unpack('<Q', f.read(8))[0]
    payload = f.read()
    f.close()
    raiz = construir_arvore(freqs)
    if raiz is None:
        print("Aviso: Arquivo não contém símbolos.")
        return
    atual = raiz
    saida_bytes = []
    for i in range(qtd_bits):
        bit = ler_bit(payload, i)
        if bit == 1:
            atual = atual.dir
        else:
            atual = atual.esq
        if atual.eh_folha():
            saida_bytes.append(atual.simbolo)
            atual = raiz
    base = pega_nome_saida(caminho)
    # Decide extensão
    tem_ponto = False
    for c in caminho:
        if c == '.':
            tem_ponto = True
    nome_saida = base + "_recuperado"
    if not tem_ponto:
        nome_saida += ".bin"
    else:
        nome_saida += ".txt"
    out = open(nome_saida, 'wb')
    out.write(bytes(saida_bytes))
    out.close()
    print("Sucesso! Arquivo descompactado: %s" % nome_saida)
    print("%d bytes recuperados." % len(saida_bytes))
