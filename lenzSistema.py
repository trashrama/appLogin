import hashlib
import json
import re

# aprender a mexer em regex

id_cont = 0

def validarEmail(email):
    return re.match(r'[\w\.+-]+@([\w-]+\.)', email)


def validarLogin(login):
    return re.match(r'^[a-zA-Z0-9_.-]{3,20}$', login)


def validarNome(nome):
    return re.match(r'^[a-zA-Z\s]{2,}(?: [a-zA-Z\s]+)*$', nome)


def gravarDados(id, nome, email, login, senha):
    dic = {
            'id':id,
            'nome_completo':nome,
            'email':email,
            'login':login,
            'senha':senha
        }
    
    #try:
    with open("dados.json",'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        final = dados[-1]
        id_cont = final['id']
        print(id_cont)
                
        #não há elementos no arquivo json.
    #except json.decoder.JSONDecodeError:
        dados = []
    
    dados.append(dic)
    with open("dados.json",'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)






# def verificarLogin(login, hash):
#     f = open("sdvvzrugv.txt", 'a+')

#     f.seek(0)
#     linhas = f.readlines()

#     if len(linhas) != 0:
#         for item in linhas:
#             conj = item.replace("\n", "").split(":")
#             login_arq = conj[0].upper()
#             hash_arq = conj[1]
#             if (login_arq == login):
#                 if (hash == hash_arq):
#                     print("Login bem sucedido!")
#                     break
#                 print("Senha Incorreta.")
#                 break
#             print("Não existe nenhum usuário com este login.")
#     else:
#         print("Não existem usuários no sistema")

#     f.close()

op = 0



while (op != 3):

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
                nome = input("Digite seu nome: ")

            login = input("Digite seu login: ")
            while (validarLogin(login) == None):
                print("INVÁLIDO: Digite um login válido")
                login = input("Digite seu login: ")

            email = input("Digite seu email: ")
            while (validarEmail(email) == None):
                print("INVÁLIDO: Digite um e-mail válido!")
                email = input("Digite seu email: ")
            hash_senha = hashlib.sha512(
                str(input("Digite sua senha: ")).encode("UTF-8")).hexdigest()
            gravarDados(id=id_cont+1, nome=nome.upper(), email=email.casefold(), login=login.upper(), senha=hash_senha)

        elif (op == 2):
            login = input("Digite seu login: ")
            hash_senha = hashlib.sha512(
                str(input("Digite sua senha: ")).encode("UTF-8")).hexdigest()
            # verificarLogin(login.upper(), hash_senha)

        elif (op == 3):
            print("Saindo...")

        else:
            print("Opção não reconhecida\n")

    else:
        print("Opção não reconhecida\n")
