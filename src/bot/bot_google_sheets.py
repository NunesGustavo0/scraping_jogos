from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime
from ..util import log
from src.bot.bot_gmail import notificar
import gspread
import os

load_dotenv()

CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS')
SHEET_NAME = os.getenv('SHEET_NAME')

def conectar_planilha():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    cred = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(cred)

    planilha = client.open(SHEET_NAME)
    aba = planilha.sheet1

    if not aba.row_values(1):
        aba.append_row(
            ['Tema', 'Data/Hora', 'Titulo', 'Desconto', 'Preço', 'Oferta?', 'Link'],
            value_input_option = 'USER_ENTERED'
        )
        log("SUCCESS", "Cabeçalho criado na planilha")
    return aba

def salvar_planilha(aba, resultados, str_busca, preco_limite):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')
    linhas = []

    for r in resultados:
        oferta = ''
        if r['preco'] and r['preco'] <= preco_limite:
            notificar(
                f"""
                ALERTA DE PROMOCAO!!!
                {r['titulo']} em promoção
                Custando apenas {r['preco']}
                Acesse pelo link: {r['link']}
                """
            )
            oferta = 'SIM'
        else:
            oferta = 'NAO'

        linhas.append([
            str_busca,
            agora,
            r['titulo'],
            r['desconto'],
            r['preco'],
            oferta,
            r['link']
        ])

    aba.append_rows(linhas, value_input_option='USER_ENTERED')
    log('INFO', f"{len(linhas)} linhas adicionadas a planilha")