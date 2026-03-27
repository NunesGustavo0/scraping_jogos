from datetime import datetime
import re

async def pesquisar(page, placeholder, str_busca):
    await page.get_by_placeholder(placeholder).fill(str_busca)
    await page.keyboard.press("Enter")

def log(log, msg):
    agora = datetime.now().strftime('%d/%m/%Y-%H:%M')
    print(f"{agora} | {log} | {msg}")

def normalizar_preco(preco):
    preco_limpo = re.sub(r'[^\d,]', '', preco)
    preco_formatado = preco_limpo.replace(',', '.')
    return float(preco_formatado)