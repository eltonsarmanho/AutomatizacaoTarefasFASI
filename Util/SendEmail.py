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


def formatar_data(data_iso):
    """Converte data do formato ISO 8601 para um formato mais legível."""
    try:
        import locale

        locale.setlocale(locale.LC_TIME, "C")  # Alternativa para Linux
        # Converter a string para um objeto datetime
        dt = datetime.strptime(data_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Formatar para o estilo desejado: "20 de fevereiro de 2025, 14h42"
        data_formatada = dt.strftime("%d-%m-%Y")
        
        return data_formatada
    except ValueError:
        return "Data inválida"
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, "pt_BR")  # Tenta sem UTF-8
        except locale.Error:
            locale.setlocale(locale.LC_TIME, "C")  # Fallback para inglês padrão

def enviar_email_projetos(resposta):
    """Envia um e-mail notificando sobre uma nova submissão do formulário de Projetos."""
    
    # Criar lista de anexos formatados
    anexos = "\n".join(resposta[10:]) if len(resposta) > 9 else "Nenhum anexo enviado"
    body = f"""
    Olá,

    Uma nova submissão foi registrada no formulário de *Projetos*.

    🧑‍🏫 Docente: {resposta[1]}  
    📝 Parecerista 1: {resposta[2]}  
    📝 Parecerista 2: {resposta[3]}  
    📌 Projeto: {resposta[4]}  
    ⏳ Carga Horária: {resposta[5]} horas  
    📅 Edital: {resposta[6]}  
    📌 Natureza: {resposta[7]}  
    📆 Ano do Edital: {resposta[8]}  
    🏛️ Solicitação: {resposta[9]}  

    📎 Anexos: 
    {anexos}

    🔗 Você pode acessar os anexos através dos links fornecidos.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🤖 *Sistema de Automação da FASI*
    """

    DESTINATARIOS = os.getenv("DESTINATARIOS", "").split(",")  # Lista de e-mails
    pareceristas_env = os.getenv("PARECERISTAS")
    pareceristas = dict(item.split(":") for item in pareceristas_env.split(","))
    email1 = pareceristas.get(resposta[2], "")
    email2 = pareceristas.get(resposta[3], "")
    DESTINATARIOS.append(email1)
    DESTINATARIOS.append(email2)

    enviar_email(body=body,nameForm='Projetos',DESTINATARIOS=DESTINATARIOS)

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
    DESTINATARIOS = os.getenv("DESTINATARIOS", "").split(",")  # Lista de e-mails

    enviar_email(body=body,nameForm='ACC',DESTINATARIOS=DESTINATARIOS)

    
def enviar_email(body,nameForm,DESTINATARIOS):
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


