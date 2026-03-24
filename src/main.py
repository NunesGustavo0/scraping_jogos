import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from src.bot.monitor_steam import raspar_steam
from src.bot.monitor_nuuvem import raspar_nuuvem

STRING_BUSCA = 'GTA'

async def main():
    resultados_steam = await raspar_steam(STRING_BUSCA)
    resultados_nuuvem = await raspar_nuuvem(STRING_BUSCA)

    result = resultados_steam + resultados_nuuvem
    df = pd.DataFrame(result)
    df.to_csv("jogos.csv", index=False)
    

if __name__ == "__main__":
    asyncio.run(main())