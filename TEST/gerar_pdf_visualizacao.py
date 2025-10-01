#!/usr/bin/env python3
"""
Script para gerar PDFs de amostra para visualização
Demonstra a geração condicional de declaração apenas para projetos de Extensão
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
    
    # Exemplo 1: Projeto de Extensão (gera AMBOS os PDFs)
    resposta_extensao = [
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
    
    # Exemplo 2: Projeto de Pesquisa (gera APENAS Parecer)
    resposta_pesquisa = [
        "0",
        "Maria Silva Santos",
        "João Oliveira",
        "Ana Paula Costa",
        "Análise de Algoritmos de Machine Learning para Detecção de Fraudes",
        "160",
        "PIBIC-CNPq",
        "Pesquisa",  # natureza
        "2025",
        "Renovação",
    ]
    
    print("🔄 Gerando PDFs de exemplo...")
    print("=" * 70)
    print()
    
    # EXEMPLO 1: EXTENSÃO
    print("📌 EXEMPLO 1: Projeto de EXTENSÃO (Parecer + Declaração)")
    print("-" * 70)
    try:
        caminho_parecer = gerar_pdf_projetos(resposta_extensao)
        print(f"✅ Parecer: {caminho_parecer}")
    except Exception as e:
        print(f"❌ Erro ao gerar PDF de parecer: {e}")
    
    # Gerar declaração apenas para Extensão
    if resposta_extensao[7].strip().lower() == "extensão":
        try:
            caminho_declaracao = gerar_pdf_declaracao_projeto(resposta_extensao)
            print(f"✅ Declaração: {caminho_declaracao}")
        except Exception as e:
            print(f"❌ Erro ao gerar PDF de declaração: {e}")
    
    print()
    
    # EXEMPLO 2: PESQUISA
    print("📌 EXEMPLO 2: Projeto de PESQUISA (Apenas Parecer)")
    print("-" * 70)
    try:
        caminho_parecer2 = gerar_pdf_projetos(resposta_pesquisa)
        print(f"✅ Parecer: {caminho_parecer2}")
    except Exception as e:
        print(f"❌ Erro ao gerar PDF de parecer: {e}")
    
    # Não gera declaração para Pesquisa
    if resposta_pesquisa[7].strip().lower() == "extensão":
        try:
            caminho_declaracao2 = gerar_pdf_declaracao_projeto(resposta_pesquisa)
            print(f"✅ Declaração: {caminho_declaracao2}")
        except Exception as e:
            print(f"❌ Erro ao gerar PDF de declaração: {e}")
    else:
        print("ℹ️  Declaração NÃO gerada (natureza != Extensão)")
    
    print()
    print("=" * 70)
    print("✨ Concluído! Abra os arquivos para visualizar.")
    print()
    print("📋 Regra implementada:")
    print("   • Extensão → Parecer + Declaração")
    print("   • Pesquisa/Ensino/Outros → Apenas Parecer")


if __name__ == "__main__":
    gerar_pdfs_exemplo()
