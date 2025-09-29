# 🚀 Guia de Deployment - AWS Lambda

Este guia explica **quando e como** recriar o package de deployment para AWS Lambda.

## 🔄 **Quando Executar `create_final_package.sh`**

### ✅ **SIM - Precisa Recriar Package**

#### 📝 **Mudanças no Código Python**
```bash
# Qualquer alteração em arquivos .py
- lambda_function.py
- SERVER/CORE/SendEmail.py
- SERVER/CORE/PDFGenerator.py
- SERVER/CORE/GoogleDriveDownloader.py
- SERVER/UTIL/GoogleSheetsReader.py
- SERVER/UTIL/CredentialsEncoder.py
- ACCFormProcessor.py
- TEST/*.py

# ⚠️ APÓS QUALQUER MUDANÇA EM .py:
./create_final_package.sh
```

#### 📦 **Nova Biblioteca/Dependência**
```bash
# 1. Adicionar ao requirements.txt
echo "nova-biblioteca==1.0.0" >> requirements.txt

# 2. Instalar localmente para testar
pip install nova-biblioteca

# 3. Testar se funciona
python lambda_function.py  # ou testes

# 4. Recriar package com nova dependência
./create_final_package.sh

# 5. Upload no AWS Lambda Console
# deployment_package_final.zip
```

#### 🗂️ **Mudanças na Estrutura**
```bash
# Situações que exigem rebuild:
- Criação de novos arquivos .py
- Novos módulos/pastas
- Remoção de arquivos Python
- Alteração na organização do código
- Mudanças em __init__.py

# Sempre execute depois:
./create_final_package.sh
```

#### 🔧 **Mudanças no Script de Build**
```bash
# Se alterar:
- create_final_package.sh
- requirements.txt (versões)
- Estrutura de pastas

# Execute para aplicar:
./create_final_package.sh
```

---

### ❌ **NÃO - Não Precisa Recriar Package**

#### ⚙️ **Environment Variables**
```bash
# Mudanças APENAS no AWS Console:
EMAIL_SENDER=novo_email@ufpa.br
EMAIL_PASSWORD=nova_senha_app
DESTINATARIOS=novos@destinatarios.com
PARECERISTAS=Nome:email@ufpa.br
GOOGLE_CREDENTIALS={"novo":"json"}
ACC_FOLDER_ID=nova_folder_id
# etc...

# ✅ Como alterar:
# AWS Lambda Console → Configuration → Environment variables → Edit
# ❌ NÃO execute: ./create_final_package.sh
```

#### 🔧 **Configurações AWS Lambda**
```bash
# Mudanças no AWS Console (sem rebuild):
- Timeout da função (300 segundos)
- Memory allocation (512 MB)
- Layers (Pillow, ReportLab)
- Function URL settings
- Triggers e eventos
- Permissões IAM

# ✅ Altere direto no Console
# ❌ NÃO precisa recriar package
```

#### 📄 **Documentação**
```bash
# Mudanças que não afetam o código:
- README.md
- DEPLOYMENT_GUIDE.md (este arquivo)
- LICENSE
- .gitignore
- Comentários em código (sem lógica)

# ❌ NÃO precisa rebuild
```

---

## 🛠️ **Workflows Recomendados**

### 🆕 **Adicionando Nova Biblioteca**
```bash
# Passo 1: Teste local
pip install requests-cache==1.0.1

# Passo 2: Teste funcionalidade
python -c "import requests_cache; print('OK')"

# Passo 3: Adicione ao requirements
echo "requests-cache==1.0.1" >> requirements.txt

# Passo 4: Teste integração
python lambda_function.py  # ou seus testes

# Passo 5: Rebuild package
./create_final_package.sh

# Passo 6: Verificar arquivos gerados
ls -la deployment_package_final.zip
ls -la package_final/

# Passo 7: Deploy no AWS Lambda
# Upload deployment_package_final.zip no Console
```

### 🔧 **Modificando Código Existente**
```bash
# Passo 1: Fazer alterações
vim SERVER/CORE/SendEmail.py

# Passo 2: Testar localmente (opcional)
python TEST/test_real_data.py

# Passo 3: Rebuild package
./create_final_package.sh

# Passo 4: Deploy
# Upload deployment_package_final.zip
```

### ⚙️ **Alterando Configurações**
```bash
# Para Environment Variables:
# ✅ AWS Console → Lambda → Configuration → Environment variables

# Para timeout/memory:
# ✅ AWS Console → Lambda → Configuration → General configuration

# ❌ NÃO execute create_final_package.sh
```

---

## 📋 **Tabela de Referência Rápida**

| Tipo de Mudança | Rebuild Package? | Onde Alterar | Comando |
|------------------|------------------|---------------|---------|
| **Código Python (.py)** | ✅ **SIM** | Local + AWS | `./create_final_package.sh` → Upload |
| **requirements.txt** | ✅ **SIM** | Local + AWS | `./create_final_package.sh` → Upload |
| **Nova biblioteca** | ✅ **SIM** | Local + AWS | Add deps → `./create_final_package.sh` → Upload |
| **Estrutura pastas** | ✅ **SIM** | Local + AWS | `./create_final_package.sh` → Upload |
| **Environment Variables** | ❌ **NÃO** | AWS Console | Configuration → Environment variables |
| **Timeout/Memory** | ❌ **NÃO** | AWS Console | Configuration → General configuration |
| **Layers** | ❌ **NÃO** | AWS Console | Configuration → Layers |
| **Function URL** | ❌ **NÃO** | AWS Console | Configuration → Function URL |
| **Documentação** | ❌ **NÃO** | Local/GitHub | Git commit apenas |

---

## 🚨 **Troubleshooting**

### **Problema: Package muito grande**
```bash
# Verificar tamanho
ls -lh deployment_package_final.zip

# Se > 50MB, otimizar:
# 1. Remover dependências desnecessárias do requirements.txt
# 2. Usar Layers para bibliotecas pesadas (já configurado: Pillow, ReportLab)
# 3. Verificar arquivos desnecessários no package
```

### **Problema: Import errors após deploy**
```bash
# Causa comum: Dependência não incluída
# Solução:
# 1. Verificar se está no requirements.txt
# 2. Recriar package: ./create_final_package.sh
# 3. Verificar se dependência está no package_final/
# 4. Upload novo deployment_package_final.zip
```

### **Problema: Timeout durante build**
```bash
# Se create_final_package.sh demora muito:
# 1. Verificar conexão internet
# 2. Limpar cache pip: pip cache purge
# 3. Executar novamente: ./create_final_package.sh
```

---

## ⚡ **Scripts Úteis**

### **Verificar Package**
```bash
# Ver conteúdo do package
unzip -l deployment_package_final.zip | head -20

# Verificar tamanho das dependências
du -sh package_final/*/
```

### **Deploy Automatizado** (Opcional)
```bash
# Criar deploy.sh
cat << 'EOF' > deploy.sh
#!/bin/bash
echo "🔧 Recriando package..."
./create_final_package.sh

if [ $? -eq 0 ]; then
    echo "✅ Package criado com sucesso!"
    echo "📦 Arquivo: deployment_package_final.zip"
    echo "📏 Tamanho: $(du -sh deployment_package_final.zip | cut -f1)"
    echo "🚀 Faça upload manual no AWS Lambda Console"
else
    echo "❌ Erro ao criar package!"
    exit 1
fi
EOF

chmod +x deploy.sh
```

---

## 📝 **Checklist de Deploy**

### **Antes de Recriar Package:**
- [ ] Código testado localmente
- [ ] requirements.txt atualizado
- [ ] Dependências instaladas: `pip install -r requirements.txt`
- [ ] Testes passando (opcional): `python TEST/test_real_data.py`

### **Após Recriar Package:**
- [ ] Arquivo `deployment_package_final.zip` gerado
- [ ] Tamanho do arquivo < 50MB (idealmente)
- [ ] Upload realizado no AWS Lambda Console
- [ ] Teste básico no Lambda: enviar POST para Function URL
- [ ] Verificar logs no CloudWatch

### **Para Environment Variables:**
- [ ] Alterar apenas no AWS Console
- [ ] Não recriar package
- [ ] Testar após alteração

---

## 🎯 **Resumo Executivo**

**💡 Regra de Ouro:**
- **Mudou código ou dependências?** → Execute `./create_final_package.sh`
- **Mudou configurações?** → Altere no AWS Console

**📦 Package Rebuild Obrigatório:**
- Qualquer arquivo `.py` modificado
- Nova biblioteca no `requirements.txt`
- Mudanças estruturais no projeto

**⚙️ AWS Console Apenas:**
- Environment Variables
- Timeout, Memory, Layers
- Function URL, Triggers, Permissões

**🚀 Workflow Típico:**
1. Desenvolver/testar localmente
2. `./create_final_package.sh`
3. Upload `deployment_package_final.zip`
4. Testar no Lambda
5. Configurar Environment Variables (se necessário)

---

**✅ Mantenha este guia como referência para deployments futuros!**