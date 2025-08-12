# 📌 Automatização de Tarefas FASI

## Descrição do Projeto

O projeto "Automatização de Tarefas FASI" é um sistema completo para automatizar o fluxo de trabalho administrativo da Faculdade de Sistemas de Informação (FASI) da Universidade Federal do Pará, Campus Universitário do Tocantins/Cametá. O sistema gerencia diversos processos acadêmicos, incluindo Atividades Curriculares Complementares (ACC), Trabalhos de Conclusão de Curso (TCC), Projetos Acadêmicos e Estágios.

## Visão Geral

Este sistema automatiza o processamento de respostas do **Google Forms**, gerenciando anexos no **Google Drive**, enviando **notificações por e-mail** aos interessados, gerando **documentos PDF** e salvando registros em **CSV**. A solução elimina processos manuais, reduz erros e agiliza o fluxo de trabalho administrativo da faculdade.

O sistema atende a diferentes tipos de formulários e processos acadêmicos:
- **ACC**: Gerenciamento de Atividades Curriculares Complementares
- **TCC**: Processamento de requisições e documentos de Trabalho de Conclusão de Curso
- **Projetos**: Gerenciamento de projetos acadêmicos, incluindo geração de pareceres
- **Estágio**: Processamento de documentação de estágios
- **Plano de Ensino**: Processamento de documentação relacionada aos planos de ensino

## Arquitetura

O sistema segue uma arquitetura modular baseada em componentes, organizada em camadas:

1. **Camada de Interface (Webhook)**: 
   - Recebe dados dos formulários Google via webhook
   - Identifica o tipo de formulário e direciona para o processador adequado

2. **Camada de Processamento**:
   - Módulos específicos para cada tipo de formulário (ACC, TCC, Projetos, Estágio)
   - Processamento paralelo via threads para operações independentes

3. **Camada de Serviços**:
   - **Google Drive**: Gerenciamento e organização de anexos
   - **Email**: Notificações automáticas para alunos, professores e administradores
   - **PDF**: Geração de documentos formatados

4. **Camada de Utilitários**:
   - Gerenciamento de credenciais e autenticação
   - Leitura de planilhas Google
   - Formatação de dados

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

## Requisitos

### Requisitos de Sistema
- Python 3.8 ou superior
- Acesso à internet para comunicação com APIs Google

### Dependências Python
- Flask: Framework web para o servidor webhook
- gspread: Acesso à API do Google Sheets
- google-auth, google-auth-oauthlib, google-auth-httplib2: Autenticação com serviços Google
- google-api-python-client: Cliente para APIs Google
- pandas: Manipulação e análise de dados
- python-dotenv: Gerenciamento de variáveis de ambiente
- reportlab: Geração de documentos PDF

### Requisitos de Serviços
- **Google Cloud Console**: Conta com credenciais ativas e APIs habilitadas
  - Google Drive API
  - Google Sheets API
- **Google Forms**: Formulários configurados com coleta de respostas
- **SMTP**: Servidor de e-mail configurado para envio de notificações
- **Ngrok**: Para expor o webhook publicamente

### Configuração de Ambiente
É necessário configurar as seguintes variáveis de ambiente em um arquivo `.env`:
```
EMAIL_SENDER=seuemail@gmail.com
EMAIL_PASSWORD=sua_senha_ou_app_password
GOOGLE_CLOUD_CREDENTIALS_FASI_BASE64=credenciais_codificadas_em_base64
DESTINATARIOS=email1@exemplo.com,email2@exemplo.com
PARECERISTAS=Nome1:email1@exemplo.com,Nome2:email2@exemplo.com
ACC_FOLDER_ID=id_da_pasta_acc_no_google_drive
TCC_FOLDER_ID=id_da_pasta_tcc_no_google_drive
PROJETOS_FOLDER_ID=id_da_pasta_projetos_no_google_drive
ESTAGIO_FOLDER_ID=id_da_pasta_estagio_no_google_drive
SHEET_ID=id_da_planilha_google
```

## 🚀 Instalação e Configuração

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
