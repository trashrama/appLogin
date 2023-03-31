import hashlib
import json
import re

# aprender a mexer em regex


def validarEmail(email):
    return re.match(r'[\w\.+-]+@([\w-]+\.)', email)


def validarLogin(login):
    return re.match(r'^[a-zA-Z0-9_.-]{3,20}$', login)


def validarNome(nome):
    return re.match(r'^[a-zA-Z\s]{2,}(?: [a-zA-Z\s]+)*$', nome)


def verificarDuplicado(campo, login):
    try:
        with open("dados.json", 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            print("oi")
            for dicionario in dados:
                if dicionario[f'{campo}'].upper() == login.upper():
                    print(f"Esse {campo} já está registrado!")
                    return False
            return True
    except:
        return False


def verificarDados():
    try:
        with open("dados.json", 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            final = dados[-1]
            id_cont = final['id']
        return id_cont, dados, True
    except:
        return 0, [], False


def gravarDados(id, nome, email, login, senha, lista_dados):
    # precisa verificar se existe um dado com o mesmo login ou mesmo email
    dic = {
        'id': id,
        'nome_completo': nome,
        'email': email,
        'login': login,
        'senha': senha
    }

    lista_dados.append(dic)

    with open("dados.json", 'w', encoding='utf-8') as arquivo:
        json.dump(lista_dados, arquivo, indent=4, ensure_ascii=False)
    print("Dados adicionados!\n")


def verificarLogin(temDados, login, hash):
    aux_lista_dados = []
    ehEmail = False
    if not (validarEmail(login) == None):
        ehEmail = True

    if (temDados):
        achou = False
        with open("dados.json", 'r', encoding='utf-8') as arquivo:
            aux_lista_dados = json.load(arquivo)
            for dic in aux_lista_dados:
                if ehEmail:
                    logar_arq = dic['email']
                else:
                    logar_arq = dic['login']

                hash_senha = dic['senha']

                if (logar_arq.upper() == login.upper()):
                    if (hash == hash_senha):
                        print("Login bem sucedido!")
                        achou = True
                        break
                    else:
                        print("Senha Incorreta.")
                        break
                if not (achou):
                    print("Não existe nenhum usuário com este login.\n")
    else:
        print("Não existem usuários no sistema. \n")


op = 0

while (op != 3):

    id_cont, lista_dados, temDados = verificarDados()

    print("----- LOGIN -----")
    print("[1] Criar Usuário")
    print("[2] Logar no Sistema")
    print("[3] Sair do sistema")

    op = input("Digite sua opção: ")
    if (op.isnumeric()):
        op = int(op)
        if op == 1:
            nome = input("Digite seu nome completo: ")
            while (validarNome(nome) == None):
                print("INVÁLIDO: Digite seu nome completo")
                nome = input("Digite seu nome completo: ")

            email = input("Digite seu email: ")
            if not (verificarDuplicado('email', email)):
                while (validarEmail(email) == None):
                    print("INVÁLIDO: Digite um e-mail válido!")
                    email = input("Digite seu email: ")

            login = input("Digite seu login: ")
            if not (verificarDuplicado('login', login)):
                while (validarLogin(login) == None):
                    print("INVÁLIDO: Digite um login válido")
                    login = input("Digite seu login: ")

                hash_senha = hashlib.sha512(
                    str(input("Digite sua senha: ")).encode("UTF-8")).hexdigest()
                gravarDados(id=id_cont+1, nome=nome.upper(),
                            email=email.casefold(), login=login.upper(), senha=hash_senha, lista_dados=lista_dados)

        elif (op == 2):
            login = input("Digite seu login ou e-mail: ")
            hash_senha = hashlib.sha512(
                str(input("Digite sua senha: ")).encode("UTF-8")).hexdigest()
            verificarLogin(temDados, login.upper(), hash_senha)

        elif (op == 3):
            print("Saindo...")

        else:
            print("Opção não reconhecida\n")

    else:
        print("Opção não reconhecida\n")
