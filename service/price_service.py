import pandas as pd
from pandas_datareader import data
import mplfinance as mpf
import requests
from bs4 import BeautifulSoup


dfType = pd.core.frame.DataFrame

def get_price(name:str, start:str='01/01/2020') -> dfType:
    """
    価格情報を取得する
    ex) start = '01/01/2020'
    EX)  ticker = 'zm.us'
    :param name: ticker名
    :param start: 取得したいデータの開始日
    :return:価格情報のデータフレーム
    """

    return data.DataReader(name=name, data_source='stooq', start=start).sort_values('Date')

def drow(stockprice:dfType) -> None:
    """
    チャートを描画する
    :param stockprice:価格情報のデータフレーム
    """
    mpf.plot(stockprice, type='candle',  mav=(5, 25, 75), volume=True, datetime_format='%d/%m/%Y')

def get_premarket(ticker:str="aapl.us") -> float:
    """
    プレマーケットの価格を取得する
    :param ticker:
    :return: price
    """
    url = f"https://stooq.com/q/?s={ticker}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    id = f"aq_{ticker}_ct"

    return float(soup.find(id=id).text)

