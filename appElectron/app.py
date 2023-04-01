from flask import Flask, request, jsonify, render_template, redirect
import json
import re
import hashlib


def verificarDados():
    try:
        with open("dados.json", 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            final = dados[-1]
            id_cont = final['id']
        return id_cont, dados, True
    except:
        return 0, [], False


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
            for dicionario in dados:
                if dicionario[f'{campo}'].upper() == login.upper():
                    print("{} {}".format(dicionario[f'{campo}'], login))
                    print(f"Esse {campo} já está registrado!")
                    return True  # é duplicado
            return False
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
                        return True
                    else:
                        print("Senha Incorreta.")
                        break
                if not (achou):
                    print("Não existe nenhum usuário com este login.\n")
    else:
        print("Não existem usuários no sistema. \n")


app = Flask(__name__)
id_cont, lista_dados, temDados = verificarDados()


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/erro",)
def erro():
    return render_template('erro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['password']

        # aqui você pode usar Python para validar o email
        # e retornar uma mensagem de sucesso ou erro

        hash_senha = hashlib.sha512(senha.encode("UTF-8")).hexdigest()
        if (verificarLogin(temDados, login.upper(), hash_senha)):
            return render_template("./deucerto.html")
        else:
            return render_template('./erro.html')
    return render_template('./login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['password']

        email = request.form['email']
        login = request.form['login']
        if (request.form['conf-password'] == senha):
            if temDados:
                if (verificarDuplicado('email', email)) or (verificarDuplicado('login', login)):
                    return render_template('./erro.html')

            hash_senha = hashlib.sha512(senha.encode("UTF-8")).hexdigest()
            gravarDados(id=id_cont+1, nome=nome.upper(),
                        email=email.casefold(), login=login.upper(), senha=hash_senha, lista_dados=lista_dados)
            return redirect("/login")
        else:
            return redirect("/erro")

    return render_template('./register.html')


if __name__ == '__main__':
    app.run(debug=True)
