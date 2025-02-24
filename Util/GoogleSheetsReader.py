import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv
import os
from Util import CredentialsEncoder
from googleapiclient.discovery import build

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do Google
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Carregar credenciais do Google Cloud da variável de ambiente
credentials_string = os.getenv("GOOGLE_CREDENTIALS")

base64_credentials = CredentialsEncoder.convertJsonToBase64(credentials_string)
credentials_dict = CredentialsEncoder.convertBase64ToJson(base64_credentials)

# Criar credenciais para autenticação
creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)
client = gspread.authorize(creds)

# Acessar a planilha de respostas do Google Forms
SHEET_ID = os.getenv("SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

# Obter todas as respostas
respostas = sheet.get_all_records()
df = pd.DataFrame(respostas)

# Salvar em CSV local (opcional)
df.to_csv("respostas.csv", index=False)

print(df)
