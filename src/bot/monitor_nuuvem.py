from playwright.async_api import async_playwright
from ..util import pesquisar, log, normalizar_preco

SELETOR_ITEM = '.grid-col-lg-3'
SELETOR_TITLE = '.game-card__product-name'
SELETOR_DATA = '.responsive_search_name_combined .search_released'
SELETOR_DISCOUNT = '.product-price--discount'
SELETOR_FINAL_PRICE = '.add-to-cart__btn--add'
SELETOR_LINK = ".grid-col-6"

async def raspar_nuuvem(str_busca, max_result):
    url = "https://www.nuuvem.com/br-pt"
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='pt-BR',
            timezone_id='America/Manaus',
        )
        page = await context.new_page()

        log('LOAD',"Acessando url nuuvem:")
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)

        await pesquisar(page, 'Buscar jogo ou palavra-chave', str_busca)
        await page.wait_for_selector(SELETOR_ITEM, timeout=30000)

        itens = await page.locator(SELETOR_ITEM).all()
        itens = itens[:max_result]

        log("INFO", f"{len(itens)} encontrados na nuuvem")

        for item in itens:
            try:
                el = item.locator(SELETOR_TITLE).first
                titulo = await el.inner_text(timeout=2000)
                log('SUCCESS', 'Titulo coletado')
            except Exception:
                titulo = "Não encontrado"
                log('ERRO', 'Titulo nao encontrado')

            try:
                el = item.locator(SELETOR_FINAL_PRICE).first
                p = await el.inner_text(timeout=2000)
                preco = normalizar_preco(p)
                log('SUCCESS', 'Preco coletado')
            except Exception:
                preco = "Não encontrado"
                log('ERRO', 'Preco nao encontrado')

            try:
                el = item.locator(SELETOR_DISCOUNT).first
                desconto = await el.inner_text(timeout=2000)
                log('SUCCESS', 'Desconto coletado')
            except Exception:
                desconto = "Sem desconto"
                log('ERRO', 'Desconto nao encontrado')

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
                "link": link
            })

        log('SUCCESS', 'Raspagem realizada')
        await browser.close()
    
    return resultados