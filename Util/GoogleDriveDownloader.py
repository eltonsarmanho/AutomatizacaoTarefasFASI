import pandas as pd
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

from Util import CredentialsEncoder


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações
SCOPES = ["https://www.googleapis.com/auth/drive"]
credentials_string = os.getenv("GOOGLE_CREDENTIALS")

base64_credentials = CredentialsEncoder.convertJsonToBase64(credentials_string)
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

def mover_anexos(links_anexos, folder_path, ROOT_FOLDER_ID):
    """
    Move os anexos para a pasta correspondente, criando múltiplos níveis de subpastas se necessário.

    :param links_anexos: Lista de links dos anexos a serem movidos.
    :param folder_path: Caminho da pasta no formato "Folder/SubFolder1/SubFolder2".
    :param ROOT_FOLDER_ID: ID da pasta raiz no Google Drive.
    """
    # Divide o caminho em múltiplas pastas
    pastas = folder_path.split("/")

    # Começa a busca/criação a partir da ROOT_FOLDER_ID
    current_folder_id = ROOT_FOLDER_ID

    # Percorre cada nível da estrutura e garante que a pasta existe
    for pasta in pastas:
        current_folder_id = encontrar_ou_criar_pasta(pasta, current_folder_id)

    # Após garantir que a estrutura existe, move os anexos para a última pasta criada
    for link in links_anexos:
        if "id=" in link:
            file_id = link.split("id=")[-1]
            try:
                # Atualiza o local do arquivo para a pasta correta
                drive_service.files().update(
                    fileId=file_id,
                    addParents=current_folder_id,
                    removeParents=ROOT_FOLDER_ID,
                    fields="id, parents"
                ).execute()
                print(f"✅ Anexo movido para {folder_path}: {file_id}")
            except Exception as e:
                print(f"❌ Erro ao mover anexo {file_id}: {e}")

def encontrar_ou_criar_pasta(nome_pasta, parent_id):
    """
    Verifica se a pasta existe dentro do parent_id. Se não existir, cria uma nova.
    Retorna o ID da pasta.
    """
    query = f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{nome_pasta}'"
    response = drive_service.files().list(q=query, fields="files(id, name)").execute()
    
    pastas = response.get("files", [])
    if pastas:
        return pastas[0]["id"]  # Retorna ID da pasta se já existir
    
    # Criar pasta caso não exista
    pasta_metadata = {
        "name": nome_pasta,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }
    pasta = drive_service.files().create(body=pasta_metadata, fields="id").execute()
    return pasta["id"]