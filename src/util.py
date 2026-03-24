async def pesquisar(page, placeholder, str_busca):
    await page.get_by_placeholder(placeholder).fill(str_busca)
    await page.keyboard.press("Enter")