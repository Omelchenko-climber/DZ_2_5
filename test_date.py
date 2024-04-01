from datetime import datetime,timedelta
from collections import defaultdict
import pprint


data = [{'date': '30.03.2024',
  'bank': 'PB',
  'baseCurrency': 980,
  'baseCurrencyLit': 'UAH',
  'exchangeRate': [
                   {'baseCurrency': 'UAH',
                    'currency': 'EUR',
                    'saleRateNB': 42.367,
                    'purchaseRateNB': 42.367,
                    'saleRate': 43.0,
                    'purchaseRate': 42.0},
                   {'baseCurrency': 'UAH',
                    'currency': 'GBP',
                    'saleRateNB': 49.5641,
                    'purchaseRateNB': 49.5641,
                    'saleRate': 49.79,
                    'purchaseRate': 49.0}
                   ]},
        {'date': '31.03.2024',
         'bank': 'PB',
         'baseCurrency': 980,
         'baseCurrencyLit': 'UAH',
         'exchangeRate': [
                    {'baseCurrency': 'UAH',
                    'currency': 'EUR',
                    'saleRateNB': 42.367,
                    'purchaseRateNB': 42.367,
                    'saleRate': 43.0,
                    'purchaseRate': 42.0},
                    {'baseCurrency': 'UAH',
                    'currency': 'GBP',
                    'saleRateNB': 49.5641,
                    'purchaseRateNB': 49.5641,
                    'saleRate': 49.79,
                    'purchaseRate': 49.0}]}]


ex_cur = {}
res = []
for day in data:
    # print(day)
    ex_cur[day['date']] = {}
    # print(ex_cur)
    for cur in day['exchangeRate']:
        # print(cur)
        ex_cur[day["date"]].update({cur["currency"]: {"sale": cur["saleRateNB"], "purchase": cur["purchaseRateNB"]}})
        # print(ex_cur)

res.append(ex_cur)


# pprint.pp(ex_cur)
pprint.pp(res)

