import os
import getpass
import socket
from colorama import Fore, Style, init
from datetime import datetime

init()


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

    print("{}{}{:<{}}{}".format(Style.BRIGHT,
          Fore.LIGHTBLUE_EX, item[0], tam, Style.RESET_ALL), end=end)

    if (param):  # se tem itens na minha lista de parametros..
        if ('l' in param):     # vou tentar replicar um ls -l
            l(item, tam, param)


def l(item, tam_str, param):
    perm = item[-1]
    dt = item[2]
    tamanho = item[1]
    padrao_tam = 'by'  # bytes

    # o parametro b é exclusivo pra um ls -l.. se vc usar fora até funciona professor mas só altera algo mesmo quando usado com ls -l.
    if ('b' in param):  # divide pra ficar mb e um tamanho mais legivel

        tamanho = tamanho / (1024*1024)
        padrao_tam = 'mb'  # megabytes
        # não é o ideal eu sei (realizar uma troca de tipo em uma variável que antes era int e estou formatando pra ser str), mas é só pra facilitar o processo xD
    tamanho = "{:.2f}".format(tamanho)

    print(" |{}{:^{}}{} ".format(Fore.LIGHTGREEN_EX,
                                 (tamanho+" "+padrao_tam), tam_str, Style.RESET_ALL), end="")
    print(" |{} {:02d}/{:02d}/{} {}|{} {:02d}:{:02d}{}".format(Fore.LIGHTCYAN_EX, dt.day,
          dt.month, dt.year, Style.RESET_ALL, Fore.LIGHTRED_EX, dt.hour, dt.second, Style.RESET_ALL), end="")
    print(f" |{Style.BRIGHT}{Fore.LIGHTYELLOW_EX} {perm}{Style.RESET_ALL}", end="")
    print(" |")


diretorios = os.listdir(".")
lista_dir = tuplaDiretorio(diretorios)
usuario = getpass.getuser()
pc = socket.gethostname()
diretorio_atual = os.getcwd()

lista_param = ['d', 'X', 'r', 't', 'd', 'l', 'b']


while (True):
    inp = input(
        f"{Style.BRIGHT}{Fore.MAGENTA}{usuario}☢{Fore.YELLOW}{pc}{Style.RESET_ALL}:{Fore.LIGHTMAGENTA_EX} {diretorio_atual}  {Style.RESET_ALL}~~► ").strip()
    inp = inp.split(" -")
    comando = inp.pop(0)
    # pra tratar tanto ls -ld e ls -l -d, concateno todos os meus parametros em uma string e depois so pecorro..
    param = "".join(parametro for parametro in inp)

    tipo = "a"

    if ("ls" == comando or ('ls' in comando and comando[3] == '.') and param in lista_param):
        # pegar o tamanho maximo so dos nomes nas tuplas
        reverse = False
        # pego o tamanho maximo das strings dos arquivos, e aplico em strings e valores que não tem uma largura fixa.
        tam = max(len(str(item)) for tupla in lista_dir for item in tupla)

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
            print(f"{Fore.RED}[Diretório vazio!]{Style.RESET_ALL}")
        print("")

        if ('l' in param):

            total = 0
            for raiz, dirs, arqs in os.walk('.'):
                total += len(arqs) + len(dirs)
            print(f"{Fore.LIGHTYELLOW_EX}total {total}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[Comando inválido!]{Style.RESET_ALL}")
