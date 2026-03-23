import asyncio
import time
from playwright.async_api import async_playwright

STRING_BUSCA = 'GTA'
DELAY = 0.5
MAX_RESULT = 4
SELETOR_ITEM = '.search_result_row'
SELETOR_TITLE = '.responsive_search_name_combined .search_name'
SELETOR_DATA = '.responsive_search_name_combined .search_released'
SELETOR_DISCOUNT = '.search_discount_and_price .discount_pct'
SELETOR_FINAL_PRICE = '.discount_final_price'

async def pesquisar(page, placeholder):
    await page.get_by_placeholder(placeholder).fill(STRING_BUSCA)
    await page.keyboard.press("Enter")

async def raspar_nuuvem():
    url = "https://www.nuuvem.com/br-pt"
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Acessando url nuuvem:")
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)

        await pesquisar(page, 'Buscar jogo ou palavra-chave')
        await page.wait_for_selector('.grid-col-lg-3', timeout=3000)

        itens = await page.locator('.grid-col-lg-3').all()
        itens = itens[:MAX_RESULT]

        print(f"{len()} encontrados...")

        for item in itens:
            try:
                el = item.locator(".game-card__product-name").first
                titulo = await el.inner_text(timeout=2000)
            except Exception:
                titulo = "Não encontrado"

            try:
                el = item.locator(".product-price--val .free, .product-price--val .decimal, .product-price--val .integer, .product-price--val sup").first
                preco = await el.inner_text(timeout=2000)
            except Exception:
                preco = "Não encontrado"

            try:
                el = item.locator("product-price--discount").first
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

async def raspar_steam():
    url = "https://store.steampowered.com/"
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Acessando url steam:")
        await page.goto(url, wait_until='domcontentloaded',timeout=30000)

        await pesquisar(page, 'Buscar na loja')
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
                el = item.locator(SELETOR_DISCOUNT).first
                desconto = await el.inner_text(timeout=2000)
            except Exception:
                desconto = "Sem desconto"

            try:
                el = item.locator(SELETOR_FINAL_PRICE).first
                preco = await el.inner_text(timeout=2000)
            except Exception:
                preco = "Não encontrado"

            resultados.append({
                "titulo": titulo,
                "desconto": desconto,
                "preco": preco
            })

        await browser.close()

    return resultados

async def main():
    resultados_steam = await raspar_steam()
    print(resultados_steam)

    resultados_nuuvem = await raspar_nuuvem()
    print(resultados_nuuvem)

if __name__ == "__main__":
    asyncio.run(main())
