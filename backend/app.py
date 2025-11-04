from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import errorcode
import os
import time

# --- Configuração dinâmica (usa variáveis de ambiente do Render/Railway) ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "35272114"),
    "database": os.getenv("DB_NAME", "cadastro_db"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# --- Função para garantir o banco/tabela (opcional no deploy) ---
def ensure_database():
    try:
        cnx = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )
        cursor = cnx.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.close()
        cnx.close()

        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("✅ Banco e tabela verificados com sucesso!")
    except mysql.connector.Error as err:
        print("⚠️ Erro ao verificar banco:", err)

# --- Função utilitária de conexão ---
def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

# --- App Flask ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"mensagem": "API Flask + Railway funcionando 🚀"})

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

# --- Execução local ---
if __name__ == '__main__':
    ensure_database()
    app.run(host='0.0.0.0', port=5000)