# 📌 Automatização de Tarefas FASI

## Descrição do Projeto

O projeto "Automatização de Tarefas FASI" é um sistema completo para automatizar o fluxo de trabalho administrativo da Faculdade de Sistemas de Informação (FASI) da Universidade Federal do Pará, Campus Universitário de Cametá. 


**Para desenvolvimento e testes locais apenas:**

### **1️⃣ Clone o Repositório**
```bash
git clone https://github.com/eltonsarmanho/AutomatizacaoTarefasFASI.git
cd AutomatizacaoTarefasFASI
```

### **2️⃣ Criar e Ativar Ambiente Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### **3️⃣ Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configurar Variáveis de Ambiente**
```bash
cp LAMBDA_ENV_VARS.template.txt .env
# Editar .env com valores reais
```

## 📡 **Configurar Webhook no Google Forms**

### **Para AWS Lambda (Produção):**
1. **No Google Sheets** vinculado ao formulário: `Extensões` → `Apps Script`
2. **Criar função para enviar dados:**
```javascript
function aoSubmeterResposta(e) {
  var urlWebhook = "https://SEU_LAMBDA_FUNCTION_URL";  // Function URL do Lambda
  var planilha = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Respostas do formulário");
  var ultimaLinha = planilha.getLastRow();
  var ultimaResposta = planilha.getRange(ultimaLinha, 1, 1, planilha.getLastColumn()).getValues()[0];

  var payload = {
    "form_id": "ACC",  // Tipo: ACC, TCC, PROJETOS, ESTAGIO, PLANO_ENSINO
    "resposta": ultimaResposta
  };

  var opcoes = {
    "method": "post",
    "contentType": "application/json", 
    "payload": JSON.stringify(payload)
  };

  try {
    var resposta = UrlFetchApp.fetch(urlWebhook, opcoes);
    console.log("Webhook enviado com sucesso:", resposta.getContentText());
  } catch (erro) {
    console.error("Erro ao enviar webhook:", erro);
  }
}
```
3. **Configurar Trigger:** `Triggers` → `Add Trigger` → `On form submit`

### **Para Desenvolvimento Local (Ngrok):**
Se estiver testando localmente, use Ngrok:
```bash
# Instalar Ngrok
ngrok http 5000

# Usar URL gerada no Apps Script
var urlWebhook = "https://xyz123.ngrok.io/webhook";
```

## 🔍 **Monitoramento e Troubleshooting**

### **AWS CloudWatch Logs**
```bash
# Visualizar logs em tempo real
aws logs tail /aws/lambda/SUA_FUNCAO_LAMBDA --follow

# Filtrar por erros
aws logs filter-log-events --log-group-name /aws/lambda/SUA_FUNCAO_LAMBDA --filter-pattern "ERROR"
```

### **Problemas Comuns e Soluções**

#### **❌ Erro: "Runtime.ImportModuleError"**
- **Causa:** Dependência não incluída no package
- **Solução:** Executar `./create_final_package.sh` novamente

#### **❌ Erro: "Read-only file system"**  
- **Causa:** Tentativa de escrever fora do `/tmp/`
- **Solução:** PDFs são salvos automaticamente em `/tmp/`

#### **❌ Erro: "Task timed out after X seconds"**
- **Causa:** Timeout muito baixo
- **Solução:** Aumentar timeout para 5 minutos (300s)

#### **❌ Emails não são enviados**
- **Verificar:** Environment variables `EMAIL_SENDER` e `EMAIL_PASSWORD`
- **Verificar:** App Password do Gmail configurado corretamente
- **Verificar:** 2FA habilitado na conta Gmail

#### **❌ PDF não é gerado**
- **Verificar:** Layers do ReportLab e Pillow adicionados
- **Verificar:** Logs para mensagens de erro específicas
- **Verificar:** Formulário é do tipo "PROJETOS"

### **Teste de Conectividade**
```bash
# Testar Function URL
curl -X POST https://SUA_FUNCTION_URL \
  -H "Content-Type: application/json" \
  -d '{"form_id":"TEST","resposta":["teste"]}'

# Resposta esperada: {"status": "success", "message": "..."}
```

## 📊 **Recursos e Funcionalidades**

### **✅ Funcionalidades Implementadas**
- 📧 **Envio automático de emails** para destinatários configurados
- 📂 **Organização no Google Drive** (opcional, se credenciais fornecidas)  
- 📄 **Geração de PDFs** para formulários de Projetos
- 🔧 **Processamento robusto** com fallbacks e tratamento de erros
- 🚀 **Arquitetura serverless** com alta disponibilidade
- 📱 **Suporte a múltiplos formulários** (ACC, TCC, Projetos, Estágio, Plano de Ensino)

### **🔒 Segurança**
- ✅ **Environment Variables** para credenciais sensíveis
- ✅ **Imports condicionais** com graceful degradation
- ✅ **Validação de dados** de entrada
- ✅ **Logs estruturados** para auditoria

### **⚡ Performance**
- ✅ **Processamento paralelo** com threads
- ✅ **Layers para dependências** pesadas (Pillow, ReportLab)
- ✅ **Timeout otimizado** (5 minutos)
- ✅ **Memory adequada** (512MB+)

## 📞 **Suporte e Contribuição**

### **🐛 Reportar Bugs**
- Criar issue no GitHub com logs do CloudWatch
- Incluir configuração de Environment Variables (sem credenciais)
- Descrever passos para reproduzir o problema

### **🚀 Contribuir**
1. Fork do repositório
2. Criar branch para feature: `git checkout -b feature/nova-funcionalidade`
3. Commit das mudanças: `git commit -m 'Add nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abrir Pull Request

### **📋 Roadmap**
- [ ] Dashboard web para monitoramento
- [ ] Integração com AWS SNS para notificações
- [ ] Suporte a anexos múltiplos
- [ ] API REST para consultas
- [ ] Interface administrativa

---

## 📄 **Licença**

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 **Autor**

**Elton Sarmanho Siqueira**  
📧 Email: eltonss@ufpa.br  
🏫 Universidade Federal do Pará - Campus Cametá  
🎯 Faculdade de Sistemas de Informação (FASI)

---

⭐ **Se este projeto foi útil, considere dar uma estrela no GitHub!**á. O sistema gerencia diversos processos acadêmicos, incluindo Atividades Curriculares Complementares (ACC), Trabalhos de Conclusão de Curso (TCC), Projetos Acadêmicos e Estágios.

## 🚀 **Nova Implementação AWS Lambda**

Este sistema foi **migrado para AWS Lambda** para oferecer maior escalabilidade, disponibilidade e redução de custos operacionais. A nova arquitetura serverless elimina a necessidade de manter servidores, oferecendo execução sob demanda e alta disponibilidade.

## Visão Geral

Este sistema automatiza o processamento de respostas do **Google Forms**, gerenciando anexos no **Google Drive**, enviando **notificações por e-mail** aos interessados, gerando **documentos PDF** e salvando registros em **CSV**. A solução elimina processos manuais, reduz erros e agiliza o fluxo de trabalho administrativo da faculdade.

O sistema atende a diferentes tipos de formulários e processos acadêmicos:
- **ACC**: Gerenciamento de Atividades Curriculares Complementares
- **TCC**: Processamento de requisições e documentos de Trabalho de Conclusão de Curso
- **Projetos**: Gerenciamento de projetos acadêmicos, incluindo geração de pareceres
- **Estágio**: Processamento de documentação de estágios
- **Plano de Ensino**: Processamento de documentação relacionada aos planos de ensino

## 🏗️ Arquitetura AWS Lambda

O sistema utiliza uma **arquitetura serverless** baseada em AWS Lambda, oferecendo:

### **Vantagens da Nova Arquitetura:**
- ✅ **Zero Manutenção de Servidor**: Sem necessidade de gerenciar infraestrutura
- ✅ **Escalabilidade Automática**: Ajuste automático conforme demanda
- ✅ **Alta Disponibilidade**: 99.95% de uptime garantido pela AWS
- ✅ **Custo Reduzido**: Pagamento apenas por execução (pay-per-use)
- ✅ **Integração Nativa**: Melhor integração com outros serviços AWS

### **Componentes da Arquitetura:**

1. **AWS Lambda Function**: 
   - Handler principal que recebe webhooks do Google Forms
   - Identifica o tipo de formulário e direciona para o processador adequado
   - Utiliza layers para dependências (Pillow, ReportLab)

2. **Camada de Processamento**:
   - Módulos específicos para cada tipo de formulário (ACC, TCC, Projetos, Estágio)
   - Processamento paralelo via threads para operações independentes
   - Geração de PDFs no diretório `/tmp/` (AWS Lambda compatível)

3. **Camada de Serviços**:
   - **Google Drive**: Gerenciamento e organização de anexos
   - **Gmail SMTP**: Notificações automáticas com app passwords
   - **PDF Generator**: Geração de documentos formatados com ReportLab

4. **Environment Variables**:
   - Configuração segura via AWS Lambda Environment Variables
   - Credenciais Google, destinatários, pareceristas
   - Configuração de pastas do Google Drive

## Fluxo de Dados

1. **Captura de Dados**:
   - Usuário preenche um formulário Google (ACC, TCC, Projetos ou Estágio)
   - O script Apps Script do Google Sheets envia os dados para o webhook

2. **Processamento**:
   - O servidor Flask recebe os dados via webhook
   - Identifica o tipo de formulário e direciona para o processador específico
   - Extrai informações relevantes (nome, matrícula, links de anexos, etc.)

3. **Operações Paralelas**:
   - **Gerenciamento de Anexos**: 
     - Cria estrutura de pastas no Google Drive
     - Move os anexos para as pastas apropriadas
   - **Notificações**: 
     - Envia e-mails formatados para os destinatários relevantes
   - **Geração de Documentos**: 
     - Cria PDFs formatados (ex: pareceres para projetos)

4. **Armazenamento**:
   - Salva registros em CSV localmente para backup e referência

## Principais Recursos

- **Processamento Automático de Formulários**: Captura e processa respostas de múltiplos tipos de formulários Google
- **Organização Inteligente de Arquivos**: Cria automaticamente estruturas de pastas no Google Drive e organiza anexos
- **Notificações Personalizadas**: Envia e-mails formatados com informações relevantes para os destinatários apropriados
- **Geração de Documentos**: Cria PDFs formatados para pareceres e outros documentos oficiais
- **Processamento Paralelo**: Utiliza threads para executar operações independentes simultaneamente
- **Segurança de Credenciais**: Gerencia credenciais de forma segura usando codificação Base64
- **Webhook Público**: Utiliza Ngrok para disponibilizar o webhook publicamente

## Estrutura do Projeto

```
📦 AutomatizacaoTarefasFASI
 ┣ 📂 Arquivos                      # Diretório para armazenamento temporário de arquivos
 ┣ 📂 Keys                          # Armazena chaves de API e credenciais
 ┣ 📂 SERVER
 ┃ ┣ 📂 CORE                        # Componentes principais do sistema
 ┃ ┃ ┣ 📜 GoogleDriveDownloader.py  # Gerenciamento de arquivos no Google Drive
 ┃ ┃ ┣ 📜 PDFGenerator.py           # Geração de documentos PDF
 ┃ ┃ ┗ 📜 SendEmail.py              # Envio de e-mails automatizados
 ┃ ┗ 📂 UTIL                        # Utilitários e ferramentas auxiliares
 ┃   ┣ 📜 CredentialsEncoder.py     # Codificação/decodificação de credenciais
 ┃   ┗ 📜 GoogleSheetsReader.py     # Leitura de dados do Google Sheets
 ┣ 📂 TEST                          # Testes unitários e de integração
 ┃ ┗ 📜 test_pdf_generator.py       # Testes para o gerador de PDF
 ┣ 📜 .gitignore                    # Arquivos e diretórios ignorados pelo Git
 ┣ 📜 ACCFormProcessor.py           # Processador principal de formulários
 ┣ 📜 LICENSE                       # Licença do projeto
 ┣ 📜 README.md                     # Documentação do projeto
 ┗ 📜 requirements.txt              # Dependências do projeto
```

## 📋 Requisitos AWS Lambda

### **AWS Services**
- **AWS Lambda**: Função serverless (Python 3.11 runtime)
- **Lambda Layers**: Para dependências pesadas
  - Pillow Layer: `arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-Pillow:5`
  - ReportLab Layer: `arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-reportlab:5`

### **Dependências Python** (incluídas no deployment package)
- google-auth, google-auth-oauthlib, google-auth-httplib2: Autenticação Google
- google-api-python-client: Cliente para APIs Google
- python-dotenv: Gerenciamento de variáveis de ambiente
- reportlab: Geração de documentos PDF (via Layer)
- pillow: Processamento de imagens (via Layer)
- requests: Requisições HTTP

### **Serviços Externos**
- **Google Cloud Console**: APIs habilitadas
  - Google Drive API
  - Google Sheets API  
- **Google Forms**: Formulários configurados com webhooks
- **Gmail**: App Passwords configurados para SMTP

## 🚀 Deployment AWS Lambda

### **Passo 1: Preparar o Ambiente Local**

1. **Clone o repositório:**
```bash
git clone https://github.com/eltonsarmanho/AutomatizacaoTarefasFASI.git
cd AutomatizacaoTarefasFASI
```

2. **Criar ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

### **Passo 2: Gerar Package de Deployment**

**⚠️ OBRIGATÓRIO:** O sistema inclui scripts para criar automaticamente o package de deployment.

1. **Executar script de criação do package:**
```bash
chmod +x create_final_package.sh
./create_final_package.sh
```

2. **Arquivos gerados:**
- 📁 `package/`: Pasta com todas as dependências e código
- 📦 `deployment_package.zip`: Arquivo ZIP pronto para upload no Lambda

### **Passo 3: Configurar AWS Lambda**

1. **Criar função Lambda:**
   - Runtime: **Python 3.11**
   - Handler: `lambda_function.lambda_handler`
   - Timeout: **5 minutos** (300 segundos)
   - Memory: **512 MB** ou mais

2. **Adicionar Layers (OBRIGATÓRIO):**
   ```
   Pillow Layer: arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-Pillow:5
   ReportLab Layer: arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p311-reportlab:5
   ```

3. **Upload do código:**
   - Fazer upload do arquivo `deployment_package.zip`
   - Verificar se `lambda_function.py` aparece no editor

### **Passo 4: Configurar Environment Variables**

Use o arquivo `LAMBDA_ENV_VARS.template.txt` como referência e configure no AWS Console:

**Configuration → Environment variables → Edit:**

```bash
# E-MAIL (OBRIGATÓRIO)
EMAIL_SENDER=fasicuntins@ufpa.br  
EMAIL_PASSWORD=lzhg_zgwc_ihbk_ypqn  # App Password do Gmail

# DESTINATÁRIOS (OBRIGATÓRIO)
DESTINATARIOS=eltonss@ufpa.br,outrofuncionario@ufpa.br

# PARECERISTAS (OBRIGATÓRIO)
PARECERISTAS=Elton Sarmanho Siqueira:eltonss@ufpa.br,Carlos dos Santos Portela:csp@ufpa.br

# GOOGLE DRIVE (OPCIONAL)
ACC_FOLDER_ID=17GiNzOq0yWsvDNKlIx5672ya_qviGOto
PROJETOS_FOLDER_ID=1rH_-Lsl-AwaNAOrlAemacTtp6sjBGNPJ
TCC_FOLDER_ID=1lQmh3nV26OUsXhD118qts-QV0-vYieqR
ESTAGIO_FOLDER_ID=1wT0wXn1bzP56h-bjy39bWv2eIhV9zdjO
PLANO_ENSINO_FOLDER_ID=15UtPsq8vFewVE10JaGGaXiBPwuu9fhhC

# GOOGLE CREDENTIALS (OPCIONAL - Para Drive)
GOOGLE_CREDENTIALS={"type":"service_account",...}  # JSON das credenciais
```

### **Passo 5: Configurar Trigger**

1. **Criar Function URL:**
   - Configuration → Function URL → Create function URL
   - Auth type: **NONE** (público)
   - Copiar a URL gerada

2. **Configurar webhook nos Google Forms:**
   - Usar a Function URL como endpoint do webhook
   - Configurar Apps Script para enviar dados para a URL

### **Passo 6: Testar o Sistema**

1. **Teste básico:**
   - Enviar requisição POST para Function URL
   - Verificar logs no CloudWatch

2. **Teste completo:**
   - Preencher um formulário Google
   - Verificar se emails são enviados
   - Confirmar geração de PDF (para Projetos)

## 📦 Estrutura do Deployment Package

Após executar `./create_final_package.sh`, a estrutura será:

```
📦 deployment_package.zip
 ┣ 📜 lambda_function.py           # Handler principal
 ┣ 📂 SERVER/                      # Módulos do sistema
 ┃ ┣ 📂 CORE/
 ┃ ┃ ┣ 📜 SendEmail.py            # Sistema de emails
 ┃ ┃ ┣ 📜 PDFGenerator.py         # Geração de PDFs
 ┃ ┃ ┗ 📜 GoogleDriveDownloader.py # Google Drive
 ┃ ┗ 📂 UTIL/
 ┃   ┗ 📜 GoogleSheetsReader.py   # Leitura de planilhas
 ┗ 📂 [dependências]              # Bibliotecas Python
   ┣ 📂 google/                   # APIs Google  
   ┣ 📂 requests/                 # Requisições HTTP
   ┣ 📂 dotenv/                   # Variáveis ambiente
   ┗ ... (outras dependências)
```

## 🔄 Atualizar Deployment

**Para mudanças no código:**
1. Modificar arquivos Python
2. Executar: `./create_final_package.sh`
3. Upload do novo `deployment_package.zip`

**Para mudanças nas variáveis:**
- Apenas alterar no AWS Console (não precisa recriar package)

## ⚡ Instalação e Configuração (Desenvolvimento Local)

### **1️⃣ Pré-requisitos**
- Python 3.8+  
- Conta no **Google Cloud Console** com credenciais ativas.  
- Conta no **Google Forms** com coleta de respostas ativada.  
- SMTP ativo para envio de e-mails (**Gmail, Outlook, etc.**).  
- **Ngrok** instalado para expor o Webhook publicamente.

### **2️⃣ Clonar o Repositório**
```bash
git clone https://github.com/seu-usuario/AutomatizacaoTarefasFASI.git
cd AutomatizacaoTarefasFASI
```

### **3️⃣ Criar e Ativar Ambiente Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### **4️⃣ Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **5️⃣ Configurar Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto e adicione as variáveis necessárias conforme descrito na seção de Requisitos.

## 🌍 **Configurando o Ngrok para expor o Webhook**

### **1️⃣ Instalar o Ngrok**
Baixe e instale o **Ngrok** conforme sua arquitetura:

- **Linux/macOS**:
  ```bash
  sudo tar -xvzf ~/Downloads/ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
  ```
- **Windows**:  
  Faça o download do executável em [ngrok.com/download](https://ngrok.com/download) e extraia o arquivo.

### **2️⃣ Configurar o Token do Ngrok**
Antes de usar o **Ngrok**, adicione sua chave de autenticação:
```bash
ngrok config add-authtoken SEU_AUTHTOKEN
```
(O token pode ser encontrado em [dashboard.ngrok.com](https://dashboard.ngrok.com))

### **3️⃣ Executar o Ngrok**
Agora, execute o **Ngrok** para expor seu servidor Flask (Porta 5000):
```bash
ngrok http 5000
```
Isso criará um link público que redireciona para `localhost:5000`.

## 📡 **Configurar o Webhook no Google Forms**
1. No **Google Sheets** vinculado ao formulário, vá até `Extensões` → `Apps Script`.
2. Crie um script para capturar os dados e enviá-los ao Webhook:
```javascript
function aoSubmeterResposta(e) {
  var urlWebhook = "https://SEU_NGROK_URL/webhook";  // Substitua pelo link do Ngrok
  var planilha = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Respostas do formulário");
  var ultimaLinha = planilha.getLastRow();
  var ultimaResposta = planilha.getRange(ultimaLinha, 1, 1, planilha.getLastColumn()).getValues()[0];

  var payload = {
    "form_id": "ACC",  // Identifique o formulário (ACC, TCC, PROJETOS, ESTAGIO)
    "resposta": ultimaResposta
  };

  var opcoes = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload)
  };

  UrlFetchApp.fetch(urlWebhook, opcoes);
}
```
3. Salve e configure para rodar **ao enviar o formulário** (`Triggers` → `OnFormSubmit`).

## 📌 **Execução do Projeto**
### **1️⃣ Iniciar o Servidor**
```bash
python ACCFormProcessor.py
```
📌 Isso inicia um servidor Flask que recebe as respostas do **Google Forms**.

### **2️⃣ Expor o Webhook Publicamente**
Em um **terminal separado**, rode:
```bash
ngrok http 5000
```
Isso disponibilizará uma URL pública para o Webhook.

### **3️⃣ Testar Funcionalidades**
```bash
curl http://127.0.0.1:5000/test_acc
```
📌 Isso dispara um teste do processador de ACC.

## 📜 **Licença**
Este projeto é licenciado sob a **MIT License** - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 **Autor**
**Desenvolvido por** [Elton Sarmanho](mailto:eltonss@ufpa.br)  

📩 Para mais informações ou colaborações, entre em contato via **[eltonss@ufpa.br](mailto:eltonss@ufpa.br)**.

---
