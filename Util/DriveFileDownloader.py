import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "Keys/credentials.json"
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)

# Listar arquivos na pasta do Google Drive
FOLDER_ID = "1XK6I_EB7Lt33DM5LMO8AF8F1aiZtucD4kWWfsJgEnPv1kv2o3aijT86_IRmyUiZrFcT3Lq5q"
PASTA_LOCAL = "Arquivos"

def listar_arquivos():
    results = drive_service.files().list(q=f"'{FOLDER_ID}' in parents", fields="files(id, name)").execute()
    return results.get("files", [])

def baixar_arquivo(file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)
    caminho_arquivo = os.path.join(PASTA_LOCAL, file_name)  # Caminho correto
    with open(caminho_arquivo, "wb") as f:
        f.write(request.execute())

# Listar e baixar arquivos
arquivos = listar_arquivos()
for arquivo in arquivos:
    baixar_arquivo(arquivo["id"], arquivo["name"])
    print(f"Baixado: {arquivo['name']}")
