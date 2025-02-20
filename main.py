import csv
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import threading
import Util.SendEmail as SendEmail

# Carregar variáveis de ambiente (evita expor credenciais no código)
load_dotenv()



app = Flask(__name__)

@app.route('/test_email', methods=['GET'])
def test_email():
    resposta_teste = ["2025-02-20", "Opção 1", "Opção 2", 42,11]
    SendEmail.enviar_email(resposta_teste)
    return "E-mail enviado!"


@app.route('/webhook', methods=['POST'])
def receber_dados():
    """Recebe os dados do Google Forms, salva no CSV, baixa anexos e envia e-mail."""
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({"status": "erro", "mensagem": "Nenhum dado recebido!"}), 400
        
        print(f"📥 Nova resposta recebida: {dados}")

        # Extrair dados recebidos
        resposta = dados.get("resposta", [])        
            

        # Criar threads para executar funções em paralelo
        email_thread = threading.Thread(target=SendEmail.enviar_email, args=(resposta,))
        #drive_thread = threading.Thread(target=GoogleDriveDownloader.baixar_arquivos_do_csv)

        # Iniciar as threads
        email_thread.start()
        #drive_thread.start()

        # Aguardar ambas as threads terminarem
        email_thread.join()
        #drive_thread.join()

        return jsonify({"status": "sucesso", "mensagem": "Dados salvos e e-mail enviado!"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
