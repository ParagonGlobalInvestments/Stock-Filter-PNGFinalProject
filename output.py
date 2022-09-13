import yfinance as yf
import pandas as pd
import random
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
stocks = list(table[0]['Symbol'])[:50]

wanted = ['sector', 'grossMargins', 'profitMargins', 'ebitdaMargins', 'revenueGrowth', 'enterpriseToRevenue', \
    'enterpriseToEbitda', 'enterpriseValue', 'priceToBook', 'beta', 'returnOnAssets','returnOnEquity']
stocks_info = {}
count = 0
for stock in stocks:
    data = yf.Ticker(stock).info
    data = dict_you_want = {your_key: data[your_key] for your_key in wanted}
    # print(data)
    stocks_info[stock] = list(data.values())
    # print(stock)
    count+=1
    print(count)

stock_data = pd.DataFrame.from_dict(stocks_info,orient='index').transpose()
# wanted.insert(0, "Items")
stock_data.index = wanted
stock_data.to_excel('Stock Financial Information.xlsx')