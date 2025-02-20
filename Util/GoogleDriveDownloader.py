from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os
import pandas as pd

# Configurações
SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "Keys/credentials.json"
PASTA_LOCAL = "Arquivos"
CSV_FILE = "respostas.csv"

# Criar a pasta de destino se não existir
if not os.path.exists(PASTA_LOCAL):
    os.makedirs(PASTA_LOCAL)

# Autenticar na API do Google Drive
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)

def baixar_arquivo_google_drive(link_drive):
    """Baixa um arquivo do Google Drive se ainda não estiver salvo localmente."""
    if not link_drive or not isinstance(link_drive, str):
        print("❌ Link inválido ou não encontrado!")
        return

    if "id=" not in link_drive:
        print("❌ Formato do link inválido!")
        return

    file_id = link_drive.split("id=")[-1]

    # Obter detalhes do arquivo
    arquivo = drive_service.files().get(fileId=file_id).execute()
    nome_arquivo = arquivo["name"]
    caminho_arquivo = os.path.join(PASTA_LOCAL, nome_arquivo)

    # Verificar se o arquivo já existe
    if os.path.exists(caminho_arquivo):
        #print(f"⚠️ Arquivo já existe: {nome_arquivo}")
        return

    # Baixar o arquivo
    request = drive_service.files().get_media(fileId=file_id)
    with open(caminho_arquivo, "wb") as file:
        file.write(request.execute())

    print(f"✅ Arquivo baixado: {nome_arquivo}")

def baixar_arquivos_do_csv():
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


# ✅ Executar o script
if __name__ == "__main__":
    baixar_arquivos_do_csv()
