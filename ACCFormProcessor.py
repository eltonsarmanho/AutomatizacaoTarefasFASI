import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from flask import Flask, request, jsonify
import threading
from dotenv import load_dotenv
from Util import GoogleDriveDownloader, SendEmail

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(override=True)


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
        form_id = dados.get("form_id")  # Identifica qual formulário enviou os dados
        resposta = dados.get("resposta", [])
        
        if form_id == "ACC":
            runACC(resposta)
        elif form_id == "PROJETOS":
            runProjetos(resposta=resposta)
        elif form_id == "TCC": #Requerimento TCC
            runTCC(resposta=resposta)
        elif form_id == "TCC_DOCUMENTO": #Documento TCC 1 ou 2
            runTCC_DOCUMENTO(resposta=resposta)
        elif form_id == "ESTAGIO": 
            runEstagio(resposta=resposta)
        
        else:
            return jsonify({"status": "erro", "mensagem": "Formulário desconhecido!"}), 400



        return jsonify({"status": "sucesso", "mensagem": "Dados salvos e anexos organizados!"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

def runEstagio(resposta):
    nome = resposta[1]
    email = resposta[2]
    turma = resposta[3]
    matricula = resposta[4]
    orientador = resposta[5]
    titulo = resposta[6]
    componente_curricular = resposta[7]
    links_anexos = resposta[8].split(", ")  # Lista de links dos anexos
    ROOT_FOLDER_ID = os.getenv("ESTAGIO_FOLDER_ID")
    
    pasta_destino = f"{componente_curricular}/{turma}/{nome}";
    # Criar threads para executar funções em paralelo   
    email_thread = threading.Thread(target=SendEmail.enviar_email_estagio, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    # Iniciar as threads
    email_thread.start()
    drive_thread.start()
    # Aguardar ambas as threads terminarem
    email_thread.join()
    drive_thread.join()

def runTCC_DOCUMENTO(resposta):
    nome = resposta[1]
    email = resposta[2]
    turma = resposta[3]
    matricula = resposta[4]
    orientador = resposta[5]
    titulo = resposta[6]
    componente_curricular = resposta[7]
    links_anexos = resposta[8].split(", ")  # Lista de links dos anexos
    ROOT_FOLDER_ID = os.getenv("TCC_FOLDER_ID")
    
    pasta_destino = f"{componente_curricular}/{turma}/{nome}";
    # Criar threads para executar funções em paralelo   
    email_thread = threading.Thread(target=SendEmail.enviar_email_tcc_documento, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    # Iniciar as threads
    email_thread.start()
    drive_thread.start()
    # Aguardar ambas as threads terminarem
    email_thread.join()
    drive_thread.join()

def runACC(resposta):
    nome = resposta[1]
    matricula = resposta[2]
    email = resposta[3]
    turma = resposta[4]
    links_anexos = resposta[5].split(", ")  # Lista de links dos anexos
    ROOT_FOLDER_ID = os.getenv("ACC_FOLDER_ID")
    pasta_destino = f"{turma}/{matricula}";

    # Criar threads para executar funções em paralelo
    email_thread = threading.Thread(target=SendEmail.enviar_email_acc, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))

        # Iniciar as threads
    email_thread.start()
    drive_thread.start()

        # Aguardar ambas as threads terminarem
    email_thread.join()
    drive_thread.join()

def runTCC(resposta):
    nome = resposta[1]
    matricula = resposta[2]
    email = resposta[3]
    trabalho = resposta[4]
    modalidade = resposta[5]
    orientador = resposta[6]
    membro1 = resposta[7]
    membro2 = resposta[8]
    if len(resposta)>11:
        membro3 = resposta[9]
    resumo = resposta[10]
    palavras_chave = resposta[11]
    data = resposta[12]
    # Criar threads para executar funções em paralelo
    email_thread = threading.Thread(target=SendEmail.enviar_email_tcc, args=(resposta,))

        # Iniciar as threads
    email_thread.start()

        # Aguardar ambas as threads terminarem
    email_thread.join()

def runProjetos(resposta):
    docente = resposta[1]
    parecerista_1 = resposta[2]
    parecerista_2 = resposta[3]
    projeto = resposta[4]
    carga_horaria = resposta[5]
    edital = resposta[6]
    natureza = resposta[7]
    ano_edital = resposta[8]
    solicitacao = resposta[9]
    # Extrai os links corretamente
    links_anexos = resposta[10].split(", ")

    ROOT_FOLDER_ID =  os.getenv("PROJETOS_FOLDER_ID")
    pasta_destino = f"{edital}/{ano_edital}/{docente}/{solicitacao}";
    email_thread = threading.Thread(target=SendEmail.enviar_email_projetos, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))

        # Iniciar as threads
    email_thread.start()
    drive_thread.start()

        # Aguardar ambas as threads terminarem
    email_thread.join()
    drive_thread.join()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
