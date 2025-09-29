#!/usr/bin/env python3
"""
Teste com dados REAIS do formulário TCC
Simula exatamente o que o Google Forms envia
"""

import requests
import json

# URL do endpoint
ENDPOINT_URL = "https://cfy3o2l4ck.execute-api.us-east-1.amazonaws.com/default/automatizacaoFasiWebhook"

def test_tcc_real_data():
    """Teste com dados reais exatamente como chegam do Google Forms"""
    print("🧪 TESTE COM DADOS REAIS - FORMULÁRIO TCC")
    print("=" * 60)
    
    # Dados exatos como chegam do Google Forms
    payload = {
        "form_id": "TCC",
        "resposta": [
            "2025-09-29T19:46:17.000Z",    # [0] timestamp
            "Teste Real",                   # [1] nome
            201916040030,                  # [2] matrícula (number)
            "teste@ufpa.br",               # [3] email
            201916040030,                  # [4] matrícula novamente (number)
            "Texto científico na forma de artigo", # [5] tipo trabalho
            "Elton Sarmanho Siqueira",     # [6] orientador
            "Elton Sarmanho Siqueiraa",   # [7] membro banca 1
            "Elton Sarmanho Siqueira",    # [8] membro banca 2
            "Elton Sarmanho Siqueira",         # [9] membro banca 3
            "Sistema de automação para processos acadêmicos usando Python", # [10] resumo
            "Python, Automação, Sistemas", # [11] palavras-chave
            "2025-12-15T14:00:00.000Z"     # [12] data defesa
        ]
    }
    
    print("📋 DADOS DO TESTE (formato real):")
    for i, valor in enumerate(payload['resposta']):
        print(f"   [{i:2}] {valor}")
    print("")
    
    try:
        print(f"📤 Enviando para: {ENDPOINT_URL}")
        
        response = requests.post(
            ENDPOINT_URL,
            json=payload,
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                print(f"✅ Response: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
                
                print("\n🔍 PRÓXIMOS PASSOS:")
                print("1. ✅ Lambda executou com sucesso")
                print("2. 🔧 Agora configure as Environment Variables:")
                print("")
                print("   EMAIL_SENDER = fasicuntins@ufpa.br")
                print("   EMAIL_PASSWORD = lzhg zgwc ihbk ypqn")
                print("   DESTINATARIOS = eltonss@ufpa.br")
                print("   PARECERISTAS = Elton Sarmanho Siqueira:eltonss@ufpa.br,Carlos dos Santos Portela:csp@ufpa.br,Fabricio de Souza Farias:fabriciosf@ufpa.br,Allan Barbosa Costa:allancosta@ufpa.br")
                print("")
                print("3. 🔄 Teste novamente após configurar")
                
            except json.JSONDecodeError:
                print(f"📄 Response: {response.text}")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_simple_tcc():
    """Teste com TCC simples (só orientação)"""
    print("\n" + "=" * 60)
    print("🧪 TESTE SIMPLES - TCC (SÓ ORIENTAÇÃO)")
    print("=" * 60)
    
    payload = {
        "form_id": "TCC", 
        "resposta": [
            "2025-09-29T19:50:00.000Z",
            "João Silva",
            "12345678901",
            "joao@ufpa.br",
            "Sistema de gestão acadêmica"
        ]
    }
    
    print("📋 Dados simples:")
    for i, valor in enumerate(payload['resposta']):
        print(f"   [{i}] {valor}")
    
    try:
        response = requests.post(
            ENDPOINT_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📊 Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Sucesso!")
        else:
            print(f"❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_tcc_real_data()
    test_simple_tcc()