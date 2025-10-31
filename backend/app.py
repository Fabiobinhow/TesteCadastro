from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode
import os
import time

# Config de conexão (já com os dados fornecidos)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "35272114",
    "database": "cadastro_db"
}

def ensure_database():
    # Conecta sem database para criar o DB se necessário
    cnx = None
    for attempt in range(3):
        try:
            cnx = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            break
        except mysql.connector.Error as err:
            print("Erro ao conectar ao MySQL:", err)
            time.sleep(1)
    if cnx is None:
        raise RuntimeError("Não foi possível conectar ao MySQL. Verifique se o serviço está rodando e as credenciais.")

    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DB_CONFIG['database']))
    cursor.close()
    cnx.close()

    # Agora cria a tabela se não existir
    cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = cnx.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        email VARCHAR(100)
    )""")
    cnx.commit()
    cursor.close()
    cnx.close()

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

app = Flask(__name__)
CORS(app)

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    if not nome or not email:
        return jsonify({'erro': 'nome e email são obrigatórios'}), 400

    cnx = get_conn()
    cursor = cnx.cursor()
    cursor.execute('INSERT INTO usuarios (nome, email) VALUES (%s, %s)', (nome, email))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    cnx = get_conn()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(usuarios)

if __name__ == '__main__':
    print('Verificando banco de dados e tabelas...')
    ensure_database()
    print('Iniciando o backend Flask em http://127.0.0.1:5000')
    app.run(debug=True)
