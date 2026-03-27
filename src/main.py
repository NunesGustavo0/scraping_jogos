import asyncio
from src.bot.monitor_steam import raspar_steam
from src.bot.monitor_nuuvem import raspar_nuuvem
from src.bot.bot_google_sheets import conectar_planilha, salvar_planilha
from src.util import log

STRING_BUSCA = 'GTA'
MAX_RESULT = 4
PRECO_LIMITE = 50.00

async def main():
    log('LOAD', 'Realizando raspagem Steam...')
    resultados_steam = await raspar_steam(STRING_BUSCA, MAX_RESULT)
    log('LOAD', 'Realizando raspagem Nuuvem...')
    resultados_nuuvem = await raspar_nuuvem(STRING_BUSCA, MAX_RESULT)

    resultados = resultados_steam + resultados_nuuvem
    # Conectar planilha google
    log('LOAD', "Conectando com planilha...")
    aba = conectar_planilha()
    log('SUCCESS', "Planilha conectada")
    # Salvando na planilha
    log("LOAD", "Salvando na planilha")
    salvar_planilha(aba, resultados, STRING_BUSCA, PRECO_LIMITE)
    log("SUCCESS", "Salvo na planilha")
    log("SUCCESS", "Processo concluido")

if __name__ == "__main__":
    asyncio.run(main())