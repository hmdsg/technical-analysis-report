from model.ticker_model import Ticker
from service import price_service as ps
import json

# ticker_list = ["AMD"]

def read_json(filename:str) -> dict:
    with open(f'data/{filename}') as f:
        return json.load(f)

def is_buy(ticker, ma_day: int, ref_day: int) -> bool:
    """
    1.陽線であるか
    2.ロウソクの胴体占める割合が50%以上か
    :param ticker:
    :param ma_day:
    :param ref_day:
    :return: 1 or -1
    """
    DOMINARION_CRITERION = 50

    # 1
    line = ticker.check_line(ref_day)
    #print(f"陰線・陽線判定結果：{line}")

    # 2
    if line == 1:
        domination_rate = ticker.positive_domination_rate(ref_day, ma_day)
        #print(f"占有率判定結果：{domination_rate}")

        if domination_rate > DOMINARION_CRITERION:
            return True
        else:
            return False

    else:
        return False


def buy_jadge(ticker, ma_day: int) -> bool:
    """
    購入判定を行う

    1.前日のis_buyがTrue
    2.3日前のis_buyがFalse
    3.3日前の終値が25日移動平均線より低い
    4.最後に25日移動平均線を超えたのが3日以上前

    :param ticker:
    :param ma_day:
    :return:
    """

    if is_buy(ticker, MA_DAY, -1) and not is_buy(ticker, MA_DAY, -3) and ticker.get_trend(-3, 25) != 1 and ticker.last_over_25ma > 3:
        print(f"最終判定結果:True")

        return True
    else:
        return False


if __name__ == '__main__':
    MA_DAY = 25
    # data_filename = "nikkei225.json"
    # data_filename = "nikkei225_test.json"
    data_filename = "sp500.json"
    #data_filename = "nasdaq100.json"
    #data_filename = "sp500_test.json"

    data = read_json(data_filename)

    for ticker in data["ticker_list"]:
        print ("=================================")
        ticker = Ticker(ticker, data["country"])

        print(f"名称:{ticker.name}")
        print(f"証券コード:{ticker.code}")

        #dfデバック
        print(ticker.price_df)

        print(f"last_over_25ma: {ticker.last_over_25ma}")

        # print(f"購入判定結果:{is_buy(ticker, MA_DAY, -3)}")
        # print(f"購入判定結果:{is_buy(ticker, MA_DAY, -2)}")
        # print(f"購入判定結果:{is_buy(ticker, MA_DAY, -1)}")

        if buy_jadge(ticker, 25):
            ps.drow(ticker.price_df)


