# Importações controladas para evitar problemas no AWS Lambda
from .SendEmail import *
from .GoogleDriveDownloader import *

# PDFGenerator tem dependências que podem causar problemas no Lambda
# Será importado apenas quando necessário dentro das funções