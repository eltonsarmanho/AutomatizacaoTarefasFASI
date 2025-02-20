# 📌 Automatização de Tarefas FASI

Este projeto automatiza o processamento de respostas do **Google Forms**, gerenciando anexos no **Google Drive**, enviando **notificações por e-mail** e salvando registros em **CSV**.  

🔧 **Principais funcionalidades**:
- Captura automática de respostas do Google Forms via **Webhook**.
- Armazena respostas em **CSV** localmente.
- Envio automático de **notificações por e-mail** aos destinatários.

---


## 🚀 **Instalação e Configuração**

### **1️⃣ Pré-requisitos**
- Python 3.8+  
- Conta no **Google Cloud Console** com credenciais ativas.  
- Conta no **Google Forms** com coleta de respostas ativada.  
- SMTP ativo para envio de e-mails (**Gmail, Outlook, etc.**).  

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

### **6️⃣ Configurar Webhook no Google Forms**
1. No **Google Sheets** vinculado ao formulário, vá até `Extensões` → `Apps Script`.
2. Crie um script para capturar os dados e enviá-los ao webhook:
```javascript
function aoSubmeterResposta(e) {
  var urlWebhook = "http://SEU_IP:5000/webhook";  // URL do seu servidor Flask
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

### **2️⃣ Testar Envio de E-mail**
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

