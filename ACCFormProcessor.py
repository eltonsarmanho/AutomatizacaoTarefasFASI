import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import threading

from Util import GoogleDriveDownloader, SendEmail

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API do Google
SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "Keys/credentials.json"

# Autenticar na API
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
client = gspread.authorize(creds)

# ID da pasta "File Response"

app = Flask(__name__)

@app.route('/test_acc', methods=['GET'])
def test_email():
    # http://localhost:5000/test_acc
    resposta_teste = ["2025-02-20", "Opção 1", "Opção 2", 42,11]
    return "ACC enviado!"




@app.route('/webhook', methods=['POST'])
def receber_dados():
    """Recebe dados do formulário e organiza os anexos na pasta correta."""
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({"status": "erro", "mensagem": "Nenhum dado recebido!"}), 400

        print(f"📥 Nova resposta recebida: {dados}")

        # Extrair dados recebidos
        resposta = dados.get("resposta", [])
        nome = resposta[1]
        matricula = resposta[2]
        email = resposta[3]
        turma = resposta[4]
        links_anexos = resposta[5:]  # Lista de links dos anexos

    
        # Criar threads para executar funções em paralelo
        email_thread = threading.Thread(target=SendEmail.enviar_email_acc, args=(resposta,))
        drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos, turma, matricula,))

        # Iniciar as threads
        email_thread.start()
        drive_thread.start()

        # Aguardar ambas as threads terminarem
        email_thread.join()
        drive_thread.join()


        return jsonify({"status": "sucesso", "mensagem": "Dados salvos e anexos organizados!"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
