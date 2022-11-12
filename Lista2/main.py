import json
import sqlite3
from flask import Flask
from flask import render_template
from flask import jsonify, redirect
from flask import request

app = Flask(__name__)

con = sqlite3.connect('agenda.db', check_same_thread=False)

from datetime import date

@app.route('/')
def index():
    return redirect('/contatos', code=302)

@app.route("/contatos", methods=["GET"])
def getContatos():
    cursor = con.cursor()
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados)

@app.route("/contatos/<nome>", methods=["GET"])
def getNomeContatos(nome):
    try:
        cursor = con.cursor()
        comando_sql = "SELECT nome FROM contatos WHERE nome LIKE '%" + str(nome) +"%'"
        cursor.execute(comando_sql)
        dados = cursor.fetchall()
        return jsonify(dados)
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404

@app.route("/contatos/<empresa>", methods=["GET"])
def getEmpresaContatos(empresa):
    try:
        cursor = con.cursor()
        comando_sql = "SELECT empresa FROM contatos WHERE empresa LIKE '%" + str(empresa) +"%'"
        cursor.execute(comando_sql)
        dados = cursor.fetchall()
        return jsonify(dados)
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404

@app.route("/contatos/<email>", methods=["GET"])
def getEmailContatos(email):
    try:
        cursor = con.cursor()
        comando_sql = "SELECT email FROM contatos WHERE email LIKE '%" + str(email) +"%'"
        cursor.execute(comando_sql)
        dados = cursor.fetchall()
        return jsonify(dados)
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404


@app.route("/contatos", methods=["POST"])
def postContatos():
    try:
        cursor = con.cursor()
        comando_sql = "INSERT INTO contatos (nome, empresa, telefone, email) values ('"+request.get_json().get('nome')+"', '"+request.get_json().get('empresa')+"', '"+request.get_json().get('telefone')+"', '"+ request.get_json().get('email')+"')"
        cursor.execute(comando_sql)
        con.commit()
        return jsonify("Sucesso!"), 200
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404


@app.route("/contatos/<int:id>", methods=["PUT"])
def putContatos(id):
    try:
        cursor = con.cursor()
        comando_sql = f"UPDATE contatos SET nome = '"+request.get_json().get('nome')+"', empresa = '"+request.get_json().get('empresa')+"', telefone = '"+ request.get_json().get('telefone')+"', email = '"+ request.get_json().get('email')+"' WHERE id = "+ str(id) +""
        cursor.execute(comando_sql)
        con.commit()
        return jsonify("Sucesso!"), 200
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404

@app.route("/contatos/<int:id>", methods=["DELETE"])
def deleteContatos(id):
    try:
        cursor = con.cursor()
        comando_sql = f"DELETE FROM contatos WHERE id = " + str(id) + ""
        cursor.execute(comando_sql)
        con.commit()
        return jsonify("Sucesso!"), 200
    except sqlite3.OperationalError:
        return jsonify("Erro de execução de query!"), 404


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)