from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa o CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Habilita CORS para todas as origens (recomendado para desenvolvimento)
CORS(app)

def inserir_dados(leito, via, insulina, manha, peso, solicitante):
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
            INSERT INTO form_tec (leito, via, insulina, manha, peso, solicitante)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            dados = (leito, via, insulina, manha, peso, solicitante)
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

@app.route('/enviar', methods=['POST'])
def enviar_dados():
    try:
        data = request.json

        leito = data.get('leito')
        via = ', '.join(data.get('via'))
        insulina = data.get('insulina')
        manha = data.get('manha')
        peso = data.get('peso')
        solicitante = data.get('solicitante')

        if inserir_dados(leito, via, insulina, manha, peso, solicitante):
            return jsonify({'message': 'Dados inseridos com sucesso!'}), 200
        else:
            return jsonify({'message': 'Erro ao inserir dados!'}), 500
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=False)


