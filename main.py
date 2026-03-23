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

async def raspar_steam():
    url = "https://store.steampowered.com/"
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Acessando url:")
        await page.goto(url, wait_until='domcontentloaded',timeout=30000)

        await page.get_by_placeholder("Buscar na loja").fill(STRING_BUSCA)
        await page.keyboard.press('Enter')
        await page.wait_for_selector(SELETOR_ITEM, timeout=3000)

        itens = await page.locator(SELETOR_ITEM).all()
        itens = itens[:MAX_RESULT]
        time.sleep(5)

        print(f"{len(itens)} encontrados...")

        for item in itens:
            try:
                el = item.locator(SELETOR_TITLE).first
                titulo = await el.inner_text(timeout=2000)
            except Exception:
                titulo = "Não encontrado"

            try:
                el = item.locator(SELETOR_DATA).first
                data = await el.inner_text(timeout=2000)
            except Exception:
                data = "Não encontrado"

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
                "data_lançamento": data,
                "desconto": desconto,
                "preco": preco
            })

    print(resultados)

async def main():
    await raspar_steam()

if __name__ == "__main__":
    asyncio.run(main())
