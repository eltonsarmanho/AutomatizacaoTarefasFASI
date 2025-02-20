# 📌 Automatização de Tarefas FASI

Este projeto automatiza o processamento de respostas do **Google Forms**, gerenciando anexos no **Google Drive**, enviando **notificações por e-mail** e salvando registros em **CSV**.  

🔧 **Principais funcionalidades**:
- Captura automática de respostas do Google Forms via **Webhook**.
- Armazena respostas em **CSV** localmente.
- Envio automático de **notificações por e-mail** aos destinatários.
- Utilização do **Ngrok** para disponibilizar o Webhook publicamente.

---

## 📂 **Estrutura do Projeto**
```
📦 AutomatizacaoTarefasFASI
 ┣ 📂 Util
 ┃ ┣ 📜 DriveFileDownloader.py   # Gerencia download de arquivos do Google Drive
 ┃ ┣ 📜 GoogleDriveDownloader.py # (Opcional) Código anterior de gerenciamento do Drive
 ┃ ┣ 📜 GoogleSheetsReader.py    # Captura respostas do Google Sheets
 ┃ ┣ 📜 SendEmail.py             # Envio de e-mails automatizados
 ┣ 📜 .env                       # Variáveis de ambiente (credenciais)
 ┣ 📜 main.py                    # Script principal (Webhook)
 ┣ 📜 respostas.csv               # Armazena respostas recebidas
 ┣ 📜 README.md                   # Documentação do projeto
 ┣ 📜 WebHookHandler.py           # Gerencia as requisições do Webhook
```

---

## 🚀 **Instalação e Configuração**

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
Crie um arquivo `.env` na raiz do projeto e adicione:
```ini
EMAIL_SENDER=seuemail@gmail.com
EMAIL_PASSWORD=sua_senha
GOOGLE_APPLICATION_CREDENTIALS=Keys/credentials.json
```
💡 **Dica:** Use uma senha de aplicativo para evitar problemas de autenticação no SMTP do Gmail.

---

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
Isso criará um link público que redireciona para `localhost:5000`. Você verá algo como:
```
Forwarding    https://1234abcd.ngrok-free.app -> http://localhost:5000
```

---

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

---

## 📌 **Execução do Projeto**
### **1️⃣ Iniciar o Servidor**
```bash
python main.py
```
📌 Isso inicia um servidor Flask que recebe as respostas do **Google Forms**.

### **2️⃣ Expor o Webhook Publicamente**
Em um **terminal separado**, rode:
```bash
ngrok http 5000
```
Isso disponibilizará uma URL pública para o Webhook. Aplicação está na Web

### **3️⃣ Testar Envio de E-mail**
```bash
curl http://127.0.0.1:5000/test_email
```
📌 Isso dispara um e-mail de teste.

---

## 📜 **Licença**
Este projeto é licenciado sob a **MIT License** - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 **Autor**
**Desenvolvido por** [Elton Sarmanho](mailto:eltonss@ufpa.br)  

📩 Para mais informações ou colaborações, entre em contato via **[eltonss@ufpa.br](mailto:eltonss@ufpa.br)**.

---


