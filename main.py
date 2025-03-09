import pandas as pd
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

from Util import CredentialsEncoder


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
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