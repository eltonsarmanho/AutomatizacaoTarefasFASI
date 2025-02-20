import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv
import os
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# Configuração da API do Google
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_FILE = "Keys/credentials.json"  # Baixe do Google Cloud Console

creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Acessar a planilha de respostas do Google Forms
SHEET_ID =os.getenv("SHEET_ID") 
sheet = client.open_by_key(SHEET_ID).sheet1

# Obter todas as respostas
respostas = sheet.get_all_records()
df = pd.DataFrame(respostas)

# Salvar em CSV local (opcional)
#df.to_csv("respostas.csv", index=False)

print(df)
