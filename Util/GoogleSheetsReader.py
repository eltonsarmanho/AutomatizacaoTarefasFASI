import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from Util import CredentialsEncoder

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do Google
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Carregar credenciais do Google Cloud da variável de ambiente
#credentials_string = os.getenv("GOOGLE_CREDENTIALS")
#base64_credentials = CredentialsEncoder.convertJsonToBase64(credentials_string)
base64_credentials = os.getenv("GOOGLE_CLOUD_CREDENTIALS_FASI_BASE64")
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
