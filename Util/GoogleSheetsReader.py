import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Configuração da API do Google
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_FILE = "Keys/credentials.json"  # Baixe do Google Cloud Console

creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Acessar a planilha de respostas do Google Forms
SHEET_ID = "1Y6QXrAQbVxf4H4fTEPnBaExqll2xAxEZgMjx-o_h-rU"
sheet = client.open_by_key(SHEET_ID).sheet1

# Obter todas as respostas
respostas = sheet.get_all_records()
df = pd.DataFrame(respostas)

# Salvar em CSV local (opcional)
#df.to_csv("respostas.csv", index=False)

print(df)
