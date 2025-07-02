import httpx


async def get_exchange_rate():
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        data = response.json()

        for item in data:
            if item["ccy"] == "USD":
                return float(item["sale"])

        raise ValueError("Курс USD не знайдено в відповіді API ПриватБанку")



