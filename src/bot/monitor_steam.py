from playwright.async_api import async_playwright
from ..util import pesquisar, log, normalizar_preco

SELETOR_ITEM = '.search_result_row'
SELETOR_TITLE = '.responsive_search_name_combined .search_name'
SELETOR_DATA = '.responsive_search_name_combined .search_released'
SELETOR_DISCOUNT = '.search_discount_and_price .discount_pct'
SELETOR_FINAL_PRICE = '.discount_final_price'

async def raspar_steam(str_busca, max_result):
    url = "https://store.steampowered.com/"
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        log("LOAD", 'Acessando url Steam...')
        await page.goto(url, wait_until='domcontentloaded',timeout=30000)

        await pesquisar(page, 'Buscar na loja', str_busca)
        await page.wait_for_selector(SELETOR_ITEM, timeout=3000)

        itens = await page.locator(SELETOR_ITEM).all()
        itens = itens[:max_result]

        log("INFO", f"{len(itens)} encontrados na steam")

        for item in itens:
            try:
                el = item.locator(SELETOR_TITLE).first
                titulo = await el.inner_text(timeout=2000)
                log('SUCCESS', 'Titulo coletado')
            except Exception:
                titulo = "Não encontrado"
                log('ERRO', 'Titulo nao encontrado')

            try:
                el = item.locator(SELETOR_DISCOUNT).first
                desconto = await el.inner_text(timeout=2000)
                log('SUCCESS', 'Desconto coletado')
            except Exception:
                desconto = "Sem desconto"
                log('ERRO', 'Desconto nao encontrado')

            try:
                el = item.locator(SELETOR_FINAL_PRICE).first
                p = await el.inner_text(timeout=2000)
                preco = normalizar_preco(p)
                log('SUCCESS', 'Preco coletado')
            except Exception:
                preco = "Não encontrado"
                log('ERRO', 'Preco nao encontrado')

            try:
                link = await item.get_attribute('href')
                log('SUCCESS', 'Link coletado')
            except Exception:
                link = 'Não encontrado'
                log('ERRO', 'Link nao encontrado')

            resultados.append({
                "titulo": titulo,
                "desconto": desconto,
                "preco": preco,
                'link': link
            })

        log('SUCCESS', 'Raspagem realizada')
        await browser.close()

    return resultados