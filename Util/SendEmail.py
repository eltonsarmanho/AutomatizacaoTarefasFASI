import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime
import locale

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


# Configurações do servidor de e-mail
SMTP_SERVER = "smtp.gmail.com"  # Use "smtp.office365.com" para Outlook, etc.
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Seu e-mail remetente
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Senha do e-mail ou App Password
DESTINATARIOS = ["eltonss@ufpa.br", ]  # Lista de e-mails


def formatar_data(data_iso):
    """Converte data do formato ISO 8601 para um formato mais legível."""
    try:
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")  # Para Linux e Mac
        # Converter a string para um objeto datetime
        dt = datetime.strptime(data_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Formatar para o estilo desejado: "20 de fevereiro de 2025, 14h42"
        data_formatada = dt.strftime("%d de %B de %Y")
        
        return data_formatada
    except ValueError:
        return "Data inválida"
    
def enviar_email_acc(resposta):
    """Gera e envia e-mail formatado para notificações de ACC."""
    
    # Criar lista de anexos formatados
    anexos = "\n".join(resposta[5:]) if len(resposta) > 4 else "Nenhum anexo enviado"

    # Corpo do e-mail formatado corretamente
    body = f"""\
    Olá,

    Uma nova resposta foi registrada no formulário de Atividades Curriculares Complementares (ACC).

    📅 Data: {formatar_data(resposta[0])}
    🎓 Nome: {resposta[1]}
    🔢 Matrícula: {resposta[2]}
    📌 Turma: {resposta[4]}

    📎 Anexos: 
    {anexos}

    🔗 Você pode acessar os anexos através dos links fornecidos.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🤖 Sistema de Automação da FASI
    """

    enviar_email(body=body,nameForm='ACC')





    
def enviar_email(body,nameForm):
    """Envia um e-mail notificando os destinatários sobre uma nova resposta."""
    try:
        # Verifica se as credenciais foram carregadas corretamente
        if not EMAIL_SENDER or not EMAIL_PASSWORD:
            raise ValueError("Credenciais de e-mail não carregadas corretamente! Verifique o arquivo .env.")

        # Configuração do e-mail
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(DESTINATARIOS)
        msg["Subject"] = f"📥 Nova Resposta Recebida no Formulário de {nameForm}"

        # Corpo do e-mail
        
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


