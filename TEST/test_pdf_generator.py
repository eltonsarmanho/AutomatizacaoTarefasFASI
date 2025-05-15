import os;
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from SERVER.CORE.PDFGenerator import gerar_pdf_projetos

# Teste com um título longo que ultrapassaria as margens
resposta_teste = [
    "0",  # índice 0 não utilizado
    "Elton Sarmanho Siqueira",  # docente
    "Allan Barbosa Costa",  # parecerista_1
    "Carlos dos Santos Portela",  # parecerista_2
    "Dashboard Interativo com IA e Sistema Preditivo para Recomendação de Estratégias de Ensino Baseado em Análise de Desempenho Acadêmico",  # projeto (título longo)
    "0",  # carga_horaria
    "PIBIC-PRODOUTOR",  # edital
    "Pesquisa",  # natureza
    "2024",  # ano_edital
    "Novo"  # solicitacao
]

# Gerar o PDF
caminho_pdf = gerar_pdf_projetos(resposta_teste)
print(f"PDF gerado com sucesso: {caminho_pdf}")
