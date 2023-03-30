import os
import getpass
import socket
from datetime import datetime


def pegaData(tupla):
    return tupla[2]


def tuplaDiretorio(diretorios):
    lista_dir = []
    for diretorio in diretorios:

        dt = datetime.fromtimestamp(os.path.getmtime(diretorio))
        perm = verPermissoes(diretorio)

        lista_dir.append((diretorio, os.path.getsize(diretorio), dt, perm))
    return lista_dir


def verPermissoes(item):
    r = "r" if os.access(item, os.R_OK) else '-'
    w = "w" if os.access(item, os.W_OK) else '-'
    x = "x" if os.access(item, os.X_OK) else '-'
    d = "d" if os.path.isdir(item) else '-'

    return f"{d}{r}{w}{x}"


def ls(item, tam, param):  # item[0] nome, item[1] tamanho...

    end = "\n"
    if (param):
        # se for ls -l ou -d ele poe um espaço pra ficar bonitinho e n quebrar a linha
        if ('l' in param or 'd' in param):
            end = ""

    print("{:<{}}".format(item[0], tam), end=end)

    if (param):  # se tem itens na minha lista de parametros..
        if ('l' in param):     # vou tentar replicar um ls -l
            l(item, param)


def l(item, param):
    perm = item[-1]
    dt = item[2]
    tamanho = item[1]
    if ('b' in param):  # divide pra ficar kb e um tamanho mais legivel
        tamanho = int(tamanho / 1024)
    print(" | {:08d}".format(tamanho), end="")
    print(" | {:02d}/{:02d}/{} | {:02d}:{:02d}".format(dt.day,
          dt.month, dt.year, dt.hour, dt.second), end="")
    print(f" | {perm}", end="")
    print(" |")


diretorios = os.listdir(".")
lista_dir = tuplaDiretorio(diretorios)
usuario = getpass.getuser()
pc = socket.gethostname()
diretorio_atual = os.getcwd()

lista_param = ['d', 'X', 'r', 't', 'd', 'l', 'b']


while (True):
    inp = input(f"{usuario}☢{pc}: {diretorio_atual} ~~► ").strip()
    inp = inp.split(" -")
    comando = inp.pop(0)
    # pra tratar tanto ls -ld e ls -l -d, concateno todos os meus parametros em uma string e depois so pecorro..
    param = "".join(parametro for parametro in inp)

    tipo = "a"

    if ("ls" == comando or ('ls' in comando and comando[3] == '.') and param in lista_param):
        # pegar o tamanho maximo so dos nomes nas tuplas
        reverse = False
        tam = max(len(item[0]) for item in lista_dir)

        if (param):  # se tem itens na minha lista de parametros..
            for parametro in param:  # acho que é mais jogo fazer um for pra percorrer do que verificar se está in param, já que se eu fizesse isso eu meio que faria um for pra cada vez que eu fosse verificar 1 parametro especifico, e aqui eu uso o for somente uma vez mas de forma que eu consigo pegar cada parametro q eu quero.
                if parametro == 'd':  # listar so os diretorios
                    tipo = "d"
                if parametro == 'X':  # organizar por ordem alfabetica
                    if (lista_dir):
                        lista_dir.sort()
                if parametro == 'r':  # organizar reversamente
                    if (lista_dir):
                        reverse = True
                        lista_dir.sort(reverse=reverse)
                if parametro == 't':
                    if (lista_dir):  # organizar por data de modificacao
                        lista_dir = sorted(
                            lista_dir, key=pegaData, reverse=reverse)

        if (lista_dir):
            for tupla in lista_dir:

                if (tipo == 'd'):
                    if (os.path.isdir(tupla[0])):
                        ls(tupla, tam, param)
                else:
                    ls(tupla, tam, param)

        else:
            print("[Diretório vazio!]")
        print("")

        if ('l' in param):

            total = 0
            for raiz, dirs, arqs in os.walk('.'):
                total += len(arqs) + len(dirs)
            print(f"total {total}")
    else:
        print("[Comando inválido!]")
