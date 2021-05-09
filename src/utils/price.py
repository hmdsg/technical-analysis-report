import pandas as pd
from pandas_datareader import data
import investpy
import datetime


dfType = pd.core.frame.DataFrame


def get_price(stock: str, country: str,  start=None, end=None) -> dfType:
    """
    investypyでの株価を取得する
    :param country: investpyで定義される国
    :param stock:証券コード
    :param start:取得開始日時
    :param end:取得終了日時 default:実行日時
    :return:価格情報のデータフレーム
    """
    if end is None:
        end = datetime.datetime.now().strftime("%d/%m/%Y")

    if start is None:
        start = (datetime.datetime.now() - datetime.timedelta(days=100)).strftime("%d/%m/%Y")

    try:
        res = investpy.get_stock_historical_data(
            stock=stock,
            from_date=start,
            to_date=end,
            country=country
        )
    except RuntimeError:
        print("価格の取得に失敗しました。")

        res = ""

    return res


def get_price_us_datareader(name: str, start=None, end=None) -> dfType:
    """
    datareaderで価格情報を取得する
    ex) start = '01/01/2020'
    EX)  ticker = 'zm.us'
    :param name: ticker名
    :param start: 取得したいデータの開始日
    :param end: 取得したいデータの終了日
    :return:価格情報のデータフレーム
    """
    if end is None:
        end = datetime.datetime.now().strftime("%d/%m/%Y")

    if start is None:
        start = (datetime.datetime.now() - datetime.timedelta(days=100)).strftime("%d/%m/%Y")

    res = data.DataReader(name=name, data_source='yahoo', start=start, end=end)

    return res
