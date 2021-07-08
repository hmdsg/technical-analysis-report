import pandas as pd
import mplfinance as mpf
import requests
from bs4 import BeautifulSoup
from utils import price
import sys
import datetime

dfType = pd.core.frame.DataFrame
DEFAULT_PERIOD = 180

def get_price(name: str, country: str, start: str = None, end=None) -> dfType:
    """
    価格情報を取得する
    ex) start = '01/01/2020'
    :param name: ticker名
    :param country: 国名
    :param start: 取得したいデータの開始日
    :param end: 取得したいデータの終了日
    :return:価格情報のデータフレーム
    """

    now = datetime.datetime.now()

    if start is None:
        td = datetime.timedelta(days=DEFAULT_PERIOD)
        start = (now-td).strftime("%m/%d/%Y")

    if end is None:
        end = now.strftime("%m/%d/%Y")

    if country == "united states":
        return price.get_price_us_datareader(name, start, end)
    elif country == "japan":
        return price.get_price(name, country, start, end)
    else:
        print("価格取得対象外の国名")
        sys.exit()

def drow(stockprice: dfType) -> None:
    """
    チャートを描画する
    :param stockprice:価格情報のデータフレーム
    """
    mpf.plot(stockprice, type='candle', mav=(5, 25, 75), volume=True, datetime_format='%d/%m/%Y')


def get_premarket(ticker: str = "aapl.us") -> float:
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
