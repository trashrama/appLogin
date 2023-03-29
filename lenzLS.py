import os

lista_dir = os.listdir(".")
print(lista_dir)

while (True):
    ent, param = map(str, input("---> ").strip().split(" "))
    print(ent, param)
    # if ("ls" in ent and ent[0] == 'l'):
    #     # for item in lista_dir:
    #     #     if ("." in item):
    #     #         print(f"{item} | {'arquivo'}")
    #     #     else:
    #     #         print(f"{item} | {'diretorio'}")

    # else:
    #     print("[Comando inválido!]")


