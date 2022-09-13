import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import yfinance as yf
# from fbprophet import Prophet
# from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import plotly.express as px
import pandas as pd
import quandl

# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# stocks = list(table[0]['Symbol'])[:5]
# # print(df)
# # print(yf.Ticker('AAPL').info)

# START = "2021-01-01"
# TODAY = date.today().strftime("%Y-%m-%d")
st.set_page_config(layout="wide")
st.title('Stock Filter App')


st.header("Choose Restrictions")
col1, col2 = st.columns(2)

with col1:
    option1 = st.selectbox(
     'Stocks with gross margin greater than',
     (.1, .2, .3, .4, .5, .6))

    option2 = st.selectbox(
     'Stocks with profit margin greater than',
     (.05, .1, .15, .2, .25))

with col2:
    option21 = st.selectbox(
     'Stocks with EV / EBITDA less than',
     (100, 50, 25, 15, 10, 5))

    option22 = st.selectbox(
     'Stocks with EV / Revenue less than',
     (50, 25, 15, 10, 5, 2))


stock_data = pd.read_excel('Stock Financial Information.xlsx')
stock_data.set_index("Unnamed: 0", inplace=True)
stocks = stock_data.columns
# st.write(stock_data)

@st.cache
def filter_stocks(option1, option2, option21, option22):
    filtered_stocks = []
    for stock in stocks:
        data = stock_data[stock]
        # st.write(type(data.loc['grossMargins']))
        if float(data.loc['grossMargins']) > option1 and float(data.loc['profitMargins']) > option2 \
            and float(data.loc['enterpriseToRevenue']) < option22 and float(data.loc['enterpriseToEbitda']) < option21:
            filtered_stocks.append(stock)
    return filtered_stocks


filtered_stocks = filter_stocks(option1, option2, option21, option22)
st.header("Filtered Stocks")
st.table(stock_data[filtered_stocks])

st.header("Display Stock Data")
chosen = st.selectbox('Filtered Stocks', filtered_stocks)



comps = []
for stock in stock_data.columns:
        if stock_data[chosen].loc['sector'] == stock_data[stock].loc['sector']:
            comps.append(float(stock_data[stock].loc['enterpriseToEbitda']))



col1, col2 = st.columns(2)
with col1:
    price_data = yf.download(chosen,'2015-1-1')['Adj Close']
    fig = px.line(price_data, title=f"{chosen} Stock Price Chart")  
    st.plotly_chart(fig, use_container_width=True)
    

with col2:
    fig = px.box(pd.Series(comps)).update_layout(
        yaxis_title="Comps Set EV / EBITDA", xaxis_title="Comparable Company Analysis"
    )
    st.plotly_chart(fig, use_container_width=True)














# selected_stock = st.selectbox('Select dataset for prediction', stocks)

# @st.cache
# def load_data(ticker):
#     for t in stocks:
#         s = yf.Ticker(t)
#         st.write(t)
#     # data = yf.download(ticker, START, TODAY)
#     # data.reset_index(inplace=True)
#     data = ""
#     return data

	
# data_load_state = st.text('Loading data...')
# data = load_data(selected_stock)
# data_load_state.text('Loading data... done!')


# # for i in range(50):
# #     msft = yf.Ticker('MSFT')
# # print(msft.financials)