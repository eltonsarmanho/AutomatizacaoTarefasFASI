import pandas as pd
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import time
import random
import traceback
from Util import CredentialsEncoder


# Carregar variáveis de ambiente do arquivo .env
load_dotenv(override=True)
# Configurações
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Carregar credenciais do Google Cloud da variável de ambiente
#credentials_string = os.getenv("GOOGLE_CREDENTIALS")
#base64_credentials = CredentialsEncoder.convertJsonToBase64(credentials_string)
base64_credentials = os.getenv("GOOGLE_CLOUD_CREDENTIALS_FASI_BASE64")
credentials_dict = CredentialsEncoder.convertBase64ToJson(base64_credentials)

# Criar credenciais para autenticação
creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)


def baixar_arquivo_google_drive(link_drive):
    """Baixa um arquivo do Google Drive se ainda não estiver salvo localmente."""
    if not link_drive or not isinstance(link_drive, str):
        print("❌ Link inválido ou não encontrado!")
        return

    if "id=" not in link_drive:
        print("❌ Formato do link inválido!")
        return
    
    PASTA_LOCAL = "Arquivos"

    # Criar a pasta de destino se não existir
    if not os.path.exists(PASTA_LOCAL):
        os.makedirs(PASTA_LOCAL)

    file_id = link_drive.split("id=")[-1]

    # Obter detalhes do arquivo
    arquivo = drive_service.files().get(fileId=file_id).execute()
    nome_arquivo = arquivo["name"]
    caminho_arquivo = os.path.join(PASTA_LOCAL, nome_arquivo)

    # Verificar se o arquivo já existe
    if os.path.exists(caminho_arquivo):
        #print(f"Arquivo já existe: {nome_arquivo}")
        return

    # Baixar o arquivo
    request = drive_service.files().get_media(fileId=file_id)
    with open(caminho_arquivo, "wb") as file:
        file.write(request.execute())

    print(f"✅ Arquivo baixado: {nome_arquivo}")

def baixar_arquivos_do_csv(CSV_FILE = "respostas.csv"):
    """Lê um CSV e baixa os arquivos listados na coluna 'Link do Arquivo'."""
    caminho_completo = os.path.abspath(CSV_FILE)

    if not os.path.exists(caminho_completo):
        print("❌ Arquivo CSV não encontrado!")
        return

    df = pd.read_csv(caminho_completo)

    if "Link do Arquivo" not in df.columns:
        print("❌ Coluna 'Link do Arquivo' não encontrada no CSV!")
        return

    for index, row in df.iterrows():
        link_drive = row["Link do Arquivo"]
        baixar_arquivo_google_drive(link_drive)

def retry_api_call(func, retries=3, delay_base=2):
    """
    Executa uma função com tentativas de repetição e backoff exponencial.
    """
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            wait_time = (delay_base ** attempt) + random.uniform(0, 1)
            print(f"⚠️ Tentativa {attempt+1} falhou. Aguardando {wait_time:.2f}s antes de tentar novamente...")
            time.sleep(wait_time)
    print("❌ Todas as tentativas falharam.")
    return None

def mover_anexos(links_anexos, folder_path, ROOT_FOLDER_ID):
    """
    Move os anexos para a pasta correspondente, garantindo que a estrutura de pastas exista.
    """
    pastas = folder_path.split("/")
    current_folder_id = ROOT_FOLDER_ID

    for pasta in pastas:
        current_folder_id = encontrar_ou_criar_pasta(pasta, current_folder_id)

    if not current_folder_id:
        print("❌ Erro: A pasta final não foi encontrada/criada corretamente!")
        return

    for link in links_anexos:
        if "id=" in link:
            file_id = link.split("id=")[-1]

            try:
                # 🔒 Garantir permissão de edição ao serviço
                def garantir_permissao():
                    return drive_service.permissions().create(
                        fileId=file_id,
                        body={
                            "role": "writer",
                            "type": "user",
                            "emailAddress": "contaufpafasi@servicoweb-453121.iam.gserviceaccount.com"
                        },
                        sendNotificationEmail=False
                    ).execute()

                retry_api_call(garantir_permissao)

                # 📂 Obter pasta atual do arquivo
                def get_file_info():
                    return drive_service.files().get(fileId=file_id, fields="id, parents").execute()

                arquivo_info = retry_api_call(get_file_info)
                if not arquivo_info:
                    print(f"❌ Falha ao obter informações do arquivo {file_id}")
                    continue

                parents_atual = arquivo_info.get("parents", [])

                # 🔄 Mover arquivo para a nova pasta
                def move_file():
                    return drive_service.files().update(
                        fileId=file_id,
                        addParents=current_folder_id,
                        removeParents=",".join(parents_atual),
                        fields="id, parents"
                    ).execute()

                result = retry_api_call(move_file)
                if result:
                    print(f"✅ Anexo movido para {folder_path}: {file_id}")
                else:
                    print(f"❌ Falha ao mover o anexo {file_id}")

                time.sleep(0.2)

            except Exception as e:
                print(f"❌ Erro inesperado ao mover anexo {file_id}: {e}")
                traceback.print_exc()



def encontrar_ou_criar_pasta(nome_pasta, parent_id):
    """
    Verifica se a pasta já existe dentro do parent_id. Se não existir, cria uma nova e retorna o ID.
    """
    query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{nome_pasta}'"
    response = drive_service.files().list(q=query, fields="files(id, name)").execute()
    
    pastas = response.get("files", [])
    if pastas:
        #print(f"📁 Pasta '{nome_pasta}' encontrada! ID: {pastas[0]['id']}")
        return pastas[0]["id"]

    #print(f"📂 Criando pasta '{nome_pasta}' dentro de {parent_id}...")
    
    try:
        # Criar pasta caso não exista
        pasta_metadata = {
            "name": nome_pasta,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }
        pasta = drive_service.files().create(body=pasta_metadata, fields="id").execute()
        #print(f"✅ Pasta '{nome_pasta}' criada! ID: {pasta['id']}")
        return pasta["id"]

    except Exception as e:
        print(f"❌ Erro ao criar pasta '{nome_pasta}': {e}")
        return None