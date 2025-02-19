from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

def inserir_dados_auxiliar(leito, glicemias, acamados, auxilios, banhos, tempo_banho, horario_banho):
    """Função para inserir dados do auxiliar de enfermagem no banco de dados"""
    try:
        # Conexão com o banco de dados MySQL
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2018',
            database='cardiologia'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()

            # Comando SQL para inserir os dados na tabela 'form_auxiliar'
            inserir = """
            INSERT INTO form_auxiliar (leito, glicemias, acamados, auxilios, banhos, tempo_banho, horario_banho)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            dados = (leito, glicemias, acamados, auxilios, banhos, tempo_banho, horario_banho)
            cursor.execute(inserir, dados)

            # Commit para salvar os dados na tabela
            conexao.commit()
            return True
    except Error as e:
        # Caso haja erro ao tentar conectar ou executar o comando
        print(f"Erro ao conectar ou inserir dados: {e}")
        return False
    finally:
        # Fechar a conexão e o cursor
        if conexao.is_connected():
            cursor.close()
            conexao.close()

@app.route('/enviar_aux', methods=['POST'])
def enviar_dados_auxiliar():
    """Endpoint para receber os dados via POST e enviar para a função de inserção"""
    try:
        # Recebe os dados do formulário enviados no corpo da requisição
        data = request.json

        # Captura os dados individualmente
        leito = data.get('leito')
        glicemias = data.get('glicemias')
        acamados = data.get('acamados')
        auxilios = data.get('auxilios')
        banhos = data.get('banhos')
        tempo_banho = data.get('tempoBanho')
        horario_banho = data.get('horarioBanho')

        # Verifica se todos os campos estão preenchidos
        if not all([leito, glicemias, acamados, auxilios, banhos, tempo_banho, horario_banho]):
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400

        # Tenta inserir os dados no banco de dados
        if inserir_dados_auxiliar(leito, glicemias, acamados, auxilios, banhos, tempo_banho, horario_banho):
            return jsonify({'message': 'Dados inseridos com sucesso para auxiliar de enfermagem!'}), 200
        else:
            return jsonify({'message': 'Erro ao inserir dados do auxiliar de enfermagem!'}), 500

    except Exception as e:
        # Em caso de erro ao processar a requisição
        return jsonify({'message': f'Erro: {str(e)}'}), 500

if __name__ == '__main__':
    # Rodando a aplicação Flask em modo de depuração
    app.run(debug=False)
