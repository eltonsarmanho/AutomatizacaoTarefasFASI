pareceristas = {
    "Allan Barbosa Costa": "allancosta@ufpa.br",
    "Elton Sarmanho Siqueira": "eltonss@ufpa.br",
    "Carlos dos Santos Portela": "csp@ufpa.br",
    "Fabricio de Souza Farias": "fabriciosf@ufpa.br",
    "Ulisses Weyl da Cunha Costa": "ulissesweyl@gmail.com",
    "Leonardo Nunes Gonçalves": "leo.widgeon16@gmail.com",
    "Keventon Rian Guimarães Gonçalves": "keventonguimaraesufpa@gmail.com"
}

nome = "Keventon Rian Guimarães Gonçalves"


from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Recuperar os pareceristas do .env
pareceristas_env = os.getenv("PARECERISTAS")

# Converter para um dicionário
pareceristas = dict(item.split(":") for item in pareceristas_env.split(","))
email = pareceristas.get(nome, "Email não encontrado")
print(email)
print(pareceristas)