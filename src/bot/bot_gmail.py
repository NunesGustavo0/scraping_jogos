from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from ..util import log

load_dotenv()

GMAIL_USER = os.getenv('GMAIL_USER')
SENHA = os.getenv('GMAIL_PWD')
ASSUNTO = 'ALERTA DE PROMOÇÃO!!!'
DEST = '2024004958@ifam.edu.br'

def criar_msg(corpo_texto):
    msg = MIMEMultipart('alternative')

    msg['Subject'] = ASSUNTO
    msg['From'] = GMAIL_USER
    msg['to'] = DEST

    msg.attach(MIMEText(corpo_texto, 'plain', 'utf-8'))

    return msg

def enviar_email(msg):
    log('LOAD', 'Tentando se conectar ao email...')

    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.ehlo() # handshake
        servidor.starttls() # Criptografar comunicação
        servidor.login(GMAIL_USER, SENHA)
        log('LOAD', f'Conectando como {GMAIL_USER}')
        servidor.sendmail(
            from_addr=GMAIL_USER,
            to_addrs=DEST,
            msg=msg.as_string()
        )

    log('SUCCESS', f'Mensagem enviada com sucesso ao {DEST}')

def notificar(corpo_texto):
    if not GMAIL_USER or not SENHA:
        log("ERRO", "Erro de autenticação")
        return
    
    log('LOAD', 'Mostrando a mensagem...')
    msg = criar_msg(corpo_texto)
    enviar_email(msg)