from menu import menu
from io_arquivo import compactar, descompactar
import sys


def main():
    args = sys.argv
    if len(args) >= 3:
        cmd = args[1].lower()
        arquivo = args[2]
        if cmd in ('c', 'compress', 'compactar'):
            compactar(arquivo)
        elif cmd in ('d', 'decompress', 'descompactar'):
            descompactar(arquivo)
        else:
            print('Uso via terminal: python3 compactador.py [c|d] <arquivo>')
    else:
        menu()


if __name__ == '__main__':
    main()
