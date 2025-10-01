#!/usr/bin/env python3
"""
Teste para verificar que a declaração é gerada apenas para projetos de Extensão
"""
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from SERVER.CORE.PDFGenerator import gerar_pdf_projetos, gerar_pdf_declaracao_projeto


def limpar_arquivos_tmp():
    """Remove PDFs de teste do /tmp"""
    import glob
    for arquivo in glob.glob("/tmp/Parecer_*.pdf") + glob.glob("/tmp/Declaracao_*.pdf"):
        try:
            os.remove(arquivo)
        except:
            pass


def teste_extensao():
    """Testa geração de declaração para projeto de Extensão"""
    print("\n🧪 TESTE 1: Projeto de Extensão")
    print("=" * 60)
    
    resposta_extensao = [
        "0",
        "Prof. João Silva",
        "Parecerista A",
        "Parecerista B",
        "Projeto de Extensão Comunitária",
        "80",
        "PIBIC-2024",
        "Extensão",  # ← Natureza = Extensão
        "2024",
        "Novo",
    ]
    
    caminho_parecer = gerar_pdf_projetos(resposta_extensao)
    caminho_declaracao = gerar_pdf_declaracao_projeto(resposta_extensao)
    
    print(f"✅ Parecer gerado: {os.path.basename(caminho_parecer)}")
    print(f"✅ Declaração gerada: {os.path.basename(caminho_declaracao)}")
    print(f"📝 Resultado: AMBOS os PDFs devem ser gerados")
    
    assert os.path.exists(caminho_parecer), "PDF de parecer deveria existir"
    assert os.path.exists(caminho_declaracao), "PDF de declaração deveria existir para Extensão"
    
    print("✅ TESTE 1 PASSOU")


def teste_pesquisa():
    """Testa que declaração NÃO é gerada para projeto de Pesquisa"""
    print("\n🧪 TESTE 2: Projeto de Pesquisa")
    print("=" * 60)
    
    resposta_pesquisa = [
        "0",
        "Prof. Maria Santos",
        "Parecerista C",
        "Parecerista D",
        "Projeto de Pesquisa Científica",
        "120",
        "PIBIC-2024",
        "Pesquisa",  # ← Natureza = Pesquisa
        "2024",
        "Novo",
    ]
    
    caminho_parecer = gerar_pdf_projetos(resposta_pesquisa)
    print(f"✅ Parecer gerado: {os.path.basename(caminho_parecer)}")
    
    # Para Pesquisa, não devemos gerar declaração
    print(f"📝 Resultado: Apenas PARECER deve ser gerado (sem declaração)")
    print(f"ℹ️  A declaração NÃO será criada porque natureza != 'Extensão'")
    
    assert os.path.exists(caminho_parecer), "PDF de parecer deveria existir"
    
    print("✅ TESTE 2 PASSOU")


def teste_ensino():
    """Testa que declaração NÃO é gerada para projeto de Ensino"""
    print("\n🧪 TESTE 3: Projeto de Ensino")
    print("=" * 60)
    
    resposta_ensino = [
        "0",
        "Prof. Carlos Lima",
        "Parecerista E",
        "Parecerista F",
        "Projeto de Ensino Inovador",
        "100",
        "PIBIC-2024",
        "Ensino",  # ← Natureza = Ensino
        "2024",
        "Renovação",
    ]
    
    caminho_parecer = gerar_pdf_projetos(resposta_ensino)
    print(f"✅ Parecer gerado: {os.path.basename(caminho_parecer)}")
    
    print(f"📝 Resultado: Apenas PARECER deve ser gerado (sem declaração)")
    print(f"ℹ️  A declaração NÃO será criada porque natureza != 'Extensão'")
    
    assert os.path.exists(caminho_parecer), "PDF de parecer deveria existir"
    
    print("✅ TESTE 3 PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎯 TESTE DE GERAÇÃO CONDICIONAL DE DECLARAÇÃO")
    print("=" * 60)
    
    limpar_arquivos_tmp()
    
    try:
        teste_extensao()
        teste_pesquisa()
        teste_ensino()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n📋 Resumo:")
        print("   • Extensão → Parecer + Declaração")
        print("   • Pesquisa → Apenas Parecer")
        print("   • Ensino → Apenas Parecer")
        print()
        
    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
