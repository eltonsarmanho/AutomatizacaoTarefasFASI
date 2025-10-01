#!/usr/bin/env python3
"""
Script para gerar PDFs de amostra para visualização
"""
import os
import sys

# Adicionar o diretório raiz ao path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from SERVER.CORE.PDFGenerator import (
    gerar_pdf_projetos,
    gerar_pdf_declaracao_projeto,
)


def gerar_pdfs_exemplo():
    """Gera PDFs de exemplo com dados fictícios"""
    
    # Dados de exemplo
    resposta_exemplo = [
        "0",  # índice 0 não utilizado
        "Elton Sarmanho Siqueira",  # docente
        "Allan Barbosa Costa",  # parecerista_1
        "Carlos dos Santos Portela",  # parecerista_2
        "Dashboard Interativo com IA e Sistema Preditivo para Recomendação de Estratégias de Ensino Baseado em Análise de Desempenho Acadêmico",  # titulo
        "120",  # carga_horaria
        "PIBIC-PRODOUTOR",  # edital
        "Extensão",  # natureza
        "2024",  # ano_edital
        "Novo",  # solicitacao
    ]
    
    print("🔄 Gerando PDFs de exemplo...")
    print()
    
    # Gerar PDF de parecer
    try:
        caminho_parecer = gerar_pdf_projetos(resposta_exemplo)
        print(f"✅ PDF de Parecer gerado:")
        print(f"   {caminho_parecer}")
        print()
    except Exception as e:
        print(f"❌ Erro ao gerar PDF de parecer: {e}")
        print()
    
    # Gerar PDF de declaração
    try:
        caminho_declaracao = gerar_pdf_declaracao_projeto(resposta_exemplo)
        print(f"✅ PDF de Declaração gerado:")
        print(f"   {caminho_declaracao}")
        print()
    except Exception as e:
        print(f"❌ Erro ao gerar PDF de declaração: {e}")
        print()
    
    print("✨ Concluído! Abra os arquivos para visualizar.")


if __name__ == "__main__":
    gerar_pdfs_exemplo()
