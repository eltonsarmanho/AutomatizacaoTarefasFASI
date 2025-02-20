import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from googleapiclient.discovery import build
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do servidor de e-mail
SMTP_SERVER = "smtp.gmail.com"  # Use "smtp.office365.com" para Outlook, etc.
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Seu e-mail remetente
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Senha do e-mail ou App Password
DESTINATARIOS = ["eltonss@ufpa.br", "fasicuntins@ufpa.br"]  # Lista de e-mails


def enviar_email(resposta):
    """Envia um e-mail notificando os destinatários sobre uma nova resposta."""
    try:
        # Verifica se as credenciais foram carregadas corretamente
        if not EMAIL_SENDER or not EMAIL_PASSWORD:
            raise ValueError("Credenciais de e-mail não carregadas corretamente! Verifique o arquivo .env.")

        # Configuração do e-mail
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(DESTINATARIOS)
        msg["Subject"] = "📥 Nova Resposta Recebida no Formulário"

        # Corpo do e-mail
        body = f"""
        Olá,

        Uma nova resposta foi recebida no formulário:

        📅 Data: {resposta[0]}
        ✅ Escolha 1: {resposta[1]}
        ✅ Escolha 2: {resposta[2]}
        🔢 Número: {resposta[3]}
        📎 Anexo: {resposta[4]}

        Você pode acessar os anexos através do link fornecido.

        Atenciosamente,
        Sistema de Automação
        """
        msg.attach(MIMEText(body, "plain"))

        # Conectar ao servidor SMTP e enviar o e-mail
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, DESTINATARIOS, msg.as_string())
        server.quit()

        print("📧 E-mail enviado com sucesso!")

        

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

# ✅ Teste: Apenas rode esse script para enviar um e-mail de teste
#if __name__ == "__main__":
#    resposta_teste = ["2025-02-20", "Opção 1", "Opção 2", 42]
#    enviar_email(resposta_teste)
