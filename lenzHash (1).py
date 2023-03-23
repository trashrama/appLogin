
import hashlib


def gravarDados(login, hash):
    f = open("sdvvzrugv.txt", 'a+')
    f.seek(0)
    linhas = f.readlines()
    if len(linhas) != 0:
        for item in linhas:
            conj = item.replace("\n", "").split(":")
            login_arq = conj[0]
            if (login_arq == login):
                print("Já existe um usuário registrado")
            else:
                f.writelines(f"{login}:{hash}\n")
    else:
        f.writelines(f"{login}:{hash}\n")
    print("Usuário criado com sucesso!")
    f.close()


def verificarLogin(login, hash):
    f = open("sdvvzrugv.txt", 'a+')

    f.seek(0)
    linhas = f.readlines()

    if len(linhas) != 0:
        for item in linhas:
            conj = item.replace("\n", "").split(":")
            login_arq = conj[0].upper()
            hash_arq = conj[1]
            if (login_arq == login):
                if (hash == hash_arq):
                    print("Login bem sucedido!")
                    break
                print("Senha Incorreta.")
                break
            print("Não existe nenhum usuário com este login.")
    else:
        print("Não existem usuários no sistema")

    f.close()


op = 0

while (op != 3):

    print("----- LOGIN -----")
    print("[1] Criar Usuário")
    print("[2] Logar no Sistema")
    print("[3] Sair do sistema")

    op = int(input("Digite sua opção:"))
    if op == 1:
        login = input("Digite seu login: ")
        hash_senha = hashlib.sha512(
            str(input("Digite sua senha: ")).encode("UTF-8")).hexdigest()
        gravarDados(login.upper(), hash_senha)

    elif (op == 2):
        login = input("Digite seu login: ")
        hash_senha = hashlib.sha512(
            str(input("Digite sua senha: ")).encode("UTF-8")).hexdigest()
        verificarLogin(login.upper(), hash_senha)

    elif (op == 3):
        print("Saindo...")

    else:
        print("Opção não reconhecida")
