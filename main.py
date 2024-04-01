import logging
import asyncio
from datetime import datetime, timedelta

import aiohttp


URL_PB = "https://api.privatbank.ua/p24api/exchange_rates"


async def fetch_exchange_rate(session, date):
    url = get_right_pb_url(URL_PB, date)
    try:
        async with session.get(url) as response:
            if response.ok:
                result = await response.json()
                return result

        logging.error(f"Error status: {response.status} for {url}.")
        return None

    except aiohttp.ClientConnectorError as err:
        print(f"Error status: {str(err)}.")
        return None


async def request(days):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_exchange_rate(session, datetime.now() - timedelta(days=i)) for i in range(days)]
        result = await asyncio.gather(*tasks)
        return result


def get_right_pb_url(url, date):
    return f"{url}?json&date={date.strftime('%d.%m.%Y')}"


def handle_output(result, another_curr=None):
    list_currency = ["EUR", "USD"]
    if another_curr:
        list_currency += another_curr
    ex_cur = {}
    res = []
    for day in result:
        ex_cur[day['date']] = {}
        for cur in day['exchangeRate']:
            if cur["currency"] in list_currency:
                ex_cur[day["date"]].update({
                    cur["currency"]: {"sale": cur["saleRate"], "purchase": cur["purchaseRate"]}})

    res.append(ex_cur)
    return res


async def get_exchangerate(handler, days):
    days = int(days)
    result = await request(days)
    if result:
        return handler(result)
    return "Failed to retrieve data."


async def get_exchange_data(days=1):
    result = await get_exchangerate(handle_output, days)
    result_list = []
    for day in result:
        for date, currencies in day.items():
            result_str = ""
            result_str += f"Date: {date}. "
            for currency, rates in currencies.items():
                result_str += f"Currency: {currency}. Sale Rate: {rates['sale']}, Purchase Rate: {rates['purchase']}."
            result_list.append(result_str)

    return result_list


if __name__ == '__main__':
    result = asyncio.run(get_exchange_data(2))
    print("\n".join(result))
