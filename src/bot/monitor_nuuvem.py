from playwright.async_api import async_playwright
from ..util import pesquisar

DELAY = 0.5
MAX_RESULT = 4
SELETOR_ITEM = '.grid-col-lg-3'
SELETOR_TITLE = '.game-card__product-name'
SELETOR_DATA = '.responsive_search_name_combined .search_released'
SELETOR_DISCOUNT = '.product-price--discount'
SELETOR_FINAL_PRICE = '.add-to-cart__btn--add'

async def raspar_nuuvem(str_busca):
    url = "https://www.nuuvem.com/br-pt"
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Acessando url nuuvem:")
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)

        await pesquisar(page, 'Buscar jogo ou palavra-chave', str_busca)
        await page.wait_for_selector(SELETOR_ITEM, timeout=3000)

        itens = await page.locator(SELETOR_ITEM).all()
        itens = itens[:MAX_RESULT]

        print(f"{len(itens)} encontrados...")

        for item in itens:
            try:
                el = item.locator(SELETOR_TITLE).first
                titulo = await el.inner_text(timeout=2000)
            except Exception:
                titulo = "Não encontrado"

            try:
                el = item.locator(SELETOR_FINAL_PRICE).first
                preco = await el.inner_text(timeout=2000)
            except Exception:
                preco = "Não encontrado"

            try:
                el = item.locator(SELETOR_DISCOUNT).first
                desconto = await el.inner_text(timeout=2000)
            except Exception:
                desconto = "Sem desconto"

            resultados.append({
                "titulo": titulo,
                "desconto": desconto,
                "preco": preco
            })

        await browser.close()
    
    return resultados