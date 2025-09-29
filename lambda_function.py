import json
import threading
import os
from SERVER.CORE import GoogleDriveDownloader, SendEmail


def lambda_handler(event, context):
    """
    Função principal que o AWS Lambda irá executar.
    """
    try:
        # O API Gateway passa os dados do POST no corpo ('body') do evento.
        # O corpo é uma string JSON, então precisamos fazer o parse.
        dados = json.loads(event.get('body', '{}'))

        if not dados:
            return {
                'statusCode': 400,
                'body': json.dumps({"status": "erro", "mensagem": "Nenhum dado recebido!"})
            }

        print(f"📥 Nova resposta recebida: {dados}")

        # Extrair dados recebidos
        form_id = dados.get("form_id")
        resposta = dados.get("resposta", [])

        # Roteamento baseado no form_id
        if form_id == "ACC":
            runACC(resposta)
        elif form_id == "PROJETOS":
            runProjetos(resposta=resposta)
        elif form_id == "TCC":
            runTCC(resposta=resposta)
        elif form_id == "TCC_DOCUMENTO":
            runTCC_DOCUMENTO(resposta=resposta)
        elif form_id == "ESTAGIO":
            runEstagio(resposta=resposta)
        elif form_id == "PlanoEnsino":
            runPlanoEnsino(resposta=resposta)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({"status": "erro", "mensagem": "Formulário desconhecido!"})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({"status": "sucesso", "mensagem": "Dados recebidos e processamento iniciado!"})
        }

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"status": "erro", "mensagem": str(e)})
        }

# As suas funções 'run' permanecem as mesmas
def runPlanoEnsino(resposta):
    links_anexos = resposta[3].split(", ")
    ROOT_FOLDER_ID = os.getenv("PLANO_ENSINO_FOLDER_ID")
    pasta_destino = f"{resposta[2]}"
    email_thread = threading.Thread(target=SendEmail.enviar_email_plano_ensino, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    email_thread.start()
    drive_thread.start()
    email_thread.join()
    drive_thread.join()

def runEstagio(resposta):
    links_anexos = resposta[8].split(", ")
    ROOT_FOLDER_ID = os.getenv("ESTAGIO_FOLDER_ID")
    pasta_destino = f"{resposta[7]}/{resposta[3]}/{resposta[1]}";
    email_thread = threading.Thread(target=SendEmail.enviar_email_estagio, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    email_thread.start()
    drive_thread.start()
    email_thread.join()
    drive_thread.join()

def runTCC_DOCUMENTO(resposta):
    links_anexos = resposta[8].split(", ")
    ROOT_FOLDER_ID = os.getenv("TCC_FOLDER_ID")
    pasta_destino = f"{resposta[7]}/{resposta[3]}/{resposta[1]}";
    email_thread = threading.Thread(target=SendEmail.enviar_email_tcc_documento, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    email_thread.start()
    drive_thread.start()
    email_thread.join()
    drive_thread.join()

def runACC(resposta):
    links_anexos = resposta[5].split(", ")
    ROOT_FOLDER_ID = os.getenv("ACC_FOLDER_ID")
    pasta_destino = f"{resposta[4]}/{resposta[2]}";
    email_thread = threading.Thread(target=SendEmail.enviar_email_acc, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    email_thread.start()
    drive_thread.start()
    email_thread.join()
    drive_thread.join()

def runTCC(resposta):
    email_thread = threading.Thread(target=SendEmail.enviar_email_tcc, args=(resposta,))
    email_thread.start()
    email_thread.join()

def runProjetos(resposta):
    links_anexos = resposta[10].split(", ")
    ROOT_FOLDER_ID =  os.getenv("PROJETOS_FOLDER_ID")
    pasta_destino = f"{resposta[6]}/{resposta[8]}/{resposta[1]}/{resposta[9]}";
    email_thread = threading.Thread(target=SendEmail.enviar_email_projetos, args=(resposta,))
    drive_thread = threading.Thread(target=GoogleDriveDownloader.mover_anexos,args=(links_anexos,pasta_destino,ROOT_FOLDER_ID))
    email_thread.start()
    drive_thread.start()
    email_thread.join()
    drive_thread.join()