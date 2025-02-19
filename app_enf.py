from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Habilita CORS para todas as origens (recomendado para desenvolvimento)
CORS(app)

# Função para inserir dados do enfermeiro no banco de dados
def inserir_dados_enfermeiro(leito, gerenciado, curativos, risco, reconciliacao, reabilitacao):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2018',
            database='cardiologia'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            inserir = """
            INSERT INTO form_enfermeiro (leito, gerenciado, curativos, risco, reconciliacao, reabilitacao)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            dados = (leito, gerenciado, curativos, risco, reconciliacao, reabilitacao)
            cursor.execute(inserir, dados)
            conexao.commit()
            return True
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return False
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Endpoint para receber e processar os dados do enfermeiro
@app.route('/enviar_enf', methods=['POST'])
def enviar_dados_enfermeiro():
    try:
        # Obtém os dados do corpo da requisição
        data = request.json

        leito = data.get('leito')
        gerenciado = data.get('gerenciado')
        curativos = data.get('curativos')
        risco = data.get('risco')
        reconciliacao = data.get('reconciliacao')
        reabilitacao = data.get('reabilitacao')

        # Verifica se todos os dados foram recebidos
        if not all([leito, gerenciado, curativos, risco, reconciliacao, reabilitacao]):
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

        # Chama a função para inserir no banco de dados
        if inserir_dados_enfermeiro(leito, gerenciado, curativos, risco, reconciliacao, reabilitacao):
            return jsonify({'message': 'Dados inseridos com sucesso para enfermeiro!'}), 200
        else:
            return jsonify({'message': 'Erro ao inserir dados do enfermeiro!'}), 500
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=False)
