import os
from time import sleep
path = input("Escreva o caminho de seu arquivo '.c': ")


while (os.path.exists(path) == False or not os.path.splitext(path)[1] == '.c'):
    if (os.path.exists(path+".c")):
        print("oi")
        path = f'{path}.c'
        break
    print("Caminho inválido!")
    path = input("Escreva o caminho de seu arquivo '.c': ")

print("Encontrado com sucesso!")

# pega a data de modificação do arquivo
timestamp_inicial = os.path.getmtime(path)

while (True):
   # aguarda 3 segundos antes de mexer novamente
    print("Verificando modificações...")
    sleep(3)

    if (timestamp_inicial != os.path.getmtime(path)):
        print("Achei! Tentando compilar arquivo '.C'...")
        status = os.system(f"gcc {path} -o {os.path.splitext(path)[0]}")
        if (status == 0):
            print("Compilação bem sucedida!", end="\n\n")
        else:
            print("Não foi possível compilar, há erros no código!", end="\n\n")
        timestamp_inicial = os.path.getmtime(path)
