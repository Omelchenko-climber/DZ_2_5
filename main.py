import logging
import argparse
import asyncio
import pprint
import sys
from datetime import datetime, timedelta

import aiohttp


URL_PB = "https://api.privatbank.ua/p24api/exchange_rates"


async def fetch_exchange_rate(session, date):
    url = get_right_url(date)
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


async def request():
    days = handle_days()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_exchange_rate(session, datetime.now() - timedelta(days=i)) for i in range(days)]
        result = await asyncio.gather(*tasks)
        return result


def handle_days():
    parser = argparse.ArgumentParser(description="Get exchange rate for the last N days.")
    parser.add_argument("days", type=int, help="Number of days to get exchange rates (for up to 10).")
    args = parser.parse_args()

    if args.days > 10 or args.days < 1:
        print("Number of days cannot be less than 1 and exceed 10.")
        sys.exit()
    else:
        return args.days


def get_right_url(date):
    return f"{URL_PB}?json&date={date.strftime('%d.%m.%Y')}"


def request_handler(result):
    ex_cur = {}
    res = []
    for day in result:
        ex_cur[day['date']] = {}
        for cur in day['exchangeRate']:
            if cur["currency"] in ["EUR", "USD"]:
                ex_cur[day["date"]].update({
                    cur["currency"]: {"sale": cur["saleRateNB"], "purchase": cur["purchaseRateNB"]}})

    res.append(ex_cur)
    return res


async def get_exchange(handler):
    result = await request()
    if result:
        return handler(result)
    return "Failed to retrieve data."


if __name__ == '__main__':

    result = asyncio.run(get_exchange(request_handler))
    pprint.pp(result, indent=1)
