from frequencia import contar_frequencias, mostrar_frequencias
from codificacao import construir_arvore, gerar_codigos, mostrar_codigos, mostrar_arvore
from io_arquivo import compactar, descompactar

def existe_arquivo(caminho):
    try:
        f = open(caminho, 'rb')
        f.close()
        return True
    except:
        return False

def menu():
    caminho = None
    dados = None
    while True:
        print('\n')
        print('1) Carregar arquivo')
        print('2) Ver Tabela de Frequências')
        print('3) Visualizar Árvore de Huffman')
        print('4) Ver Tabela de Códigos (Binário)')
        print('5) Compactar Arquivo')
        print('6) Descompactar Arquivo (.huff)')
        print('7) Sair')
        opc = input('Escolha uma opção: ').strip()
        if opc == '1':
            path = input('Digite o caminho do arquivo: ').strip()
            if existe_arquivo(path):
                f = open(path, 'rb')
                buf = f.read()
                f.close()
                print("Arquivo '%s' carregado com sucesso (%d bytes)." % (path, len(buf)))
                caminho = path
                dados = buf
            else:
                print('Erro: Arquivo não encontrado.')
                caminho = None
                dados = None
        elif opc == '2':
            if dados is not None:
                freqs = contar_frequencias(dados)
                mostrar_frequencias(freqs)
            else:
                print('Aviso: Nenhum arquivo carregado. Use a opção 1 primeiro.')
        elif opc == '3':
            if dados is not None:
                freqs = contar_frequencias(dados)
                raiz = construir_arvore(freqs)
                mostrar_arvore(raiz, 0)
            else:
                print('Aviso: Nenhum arquivo carregado. Use a opção 1 primeiro.')
        elif opc == '4':
            if dados is not None:
                freqs = contar_frequencias(dados)
                raiz = construir_arvore(freqs)
                codigos = gerar_codigos(raiz)
                mostrar_codigos(codigos)
            else:
                print('Aviso: Nenhum arquivo carregado. Use a opção 1 primeiro.')
        elif opc == '5':
            if caminho is not None:
                compactar(caminho)
            else:
                print('Aviso: Nenhum arquivo carregado. Use a opção 1 primeiro.')
        elif opc == '6':
            s = input('Digite o caminho do arquivo .huff: ').strip()
            descompactar(s)
        elif opc == '7':
            print('Saindo do sistema...')
            break
        else:
            print('Opção inválida, tente novamente.')
