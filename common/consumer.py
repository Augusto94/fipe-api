import asyncio
import json

import aiohttp
import redis

redis_client = redis.Redis(host="redis", port=6379, db=0)


async def main():
    """Processa as marcas da fila e envia para a API-2.

    Este código é executado continuamente, processando as marcas da fila e enviando para a API-2.
    Se ocorrer algum erro, ele será ignorado e o processo continuará em execução.
    """
    while True:
        try:
            marca_data = redis_client.blpop("marcas-queue")
            marca = marca_data[1].decode()
            marca_json = json.loads(marca)
            async with aiohttp.ClientSession() as session:
                url = "http://api-2:8001/veiculos"
                async with session.post(url, json=marca_json) as resp:
                    r = await resp.json()
        except Exception:
            pass


asyncio.run(main())
