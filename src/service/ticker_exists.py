import pandas as pd
from pandas_datareader import data
import mplfinance as mpf
import requests
from bs4 import BeautifulSoup
import datetime
import investpy

dfType = pd.core.frame.DataFrame


def get_price(name: str, start: str = '01/09/2020', end: str = None) -> dfType:
    """
    価格情報を取得する
    ex) start = '01/01/2020'
    EX)  ticker = 'zm.us'
    :param name: ticker名
    :param start: 取得したいデータの開始日
    :param end: 取得したいデータの終了日
    :return:価格情報のデータフレーム
    """

    res = data.DataReader(name=name,  start=start, data_source='yahoo')

    return res


# print("start")
# print(get_price("9433"))
# print("end")

def get_price_jpn(stock: str, start=None, end=None) -> dfType:
    """
    日本株の株価を取得する
    :param stock:証券コード
    :param start:取得開始日時
    :param end:取得終了日時 default:実行日時
    :return:価格情報のデータフレーム
    """
    if end is None:
        end = datetime.datetime.now().strftime("%d/%m/%Y")

    if start is None:
        start = (datetime.datetime.now() - datetime.timedelta(days=100)).strftime("%d/%m/%Y")

    res = investpy.get_stock_information(stock, "japan", as_json=True)

    print (res)

def get_price_ext(stock: str, start=None, end=None) -> dfType:
    """
    日本株の株価を取得する
    :param stock:証券コード
    :param start:取得開始日時
    :param end:取得終了日時 default:実行日時
    :return:価格情報のデータフレーム
    """
    if end is None:
        end = datetime.datetime.now().strftime("%d/%m/%Y")

    if start is None:
        start = (datetime.datetime.now() - datetime.timedelta(days=100)).strftime("%d/%m/%Y")

    res = investpy.get_stock_information(stock, "united states", as_json=True)

    print(res)

print(get_price_ext("aapl"))
