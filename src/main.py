from model.ticker_model import Ticker
from utils import writer as wr
from service import price_service as ps
import json
import datetime


# ticker_list = ["AMD"]

def read_json(filename: str) -> dict:
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

    ma_name = 'MA_' + str(ma_day)
    column = ma_name + "_domination_rate"

    if ticker.is_positive_line(ref_day):
        domination_rate = ticker.price_df.iloc[ref_day][column]

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
    2.最後に25日移動平均線を超えたのが5日以上前

    :param ticker:
    :param ma_day:
    :return:
    """

    print(f"last diff is {ticker.get_ma_vs_close(25, -1)}")

    if len(ticker.period_list_25ma) < 2:
        print("periodのデータ数が足りません")
        return False

    if is_buy(ticker, MA_DAY, -1) \
            and (ticker.period_list_25ma[0] < 3) \
            and (ticker.period_list_25ma[1] - ticker.period_list_25ma[0]) > 5:
        print("最終判定結果:True")
        return True
    else:
        print("最終判定結果:False")
        # print("is_buy(ticker, MA_DAY, -1)")
        # print(is_buy(ticker, MA_DAY, -1))
        # print("ticker.period_list_25ma[0] < 3")
        # print(ticker.period_list_25ma[0] < 3)
        # print("ticker.period_list_25ma[1] - ticker.period_list_25ma[0] > 5")
        # print(ticker.period_list_25ma[1] - ticker.period_list_25ma[0] > 5)
        return False


if __name__ == '__main__':
    MA_DAY = 25
    now = datetime.datetime.now()
    # data_filename = "nikkei225.json"
    # data_filename = "nikkei225_test.json"
    # data_filename = "sp500.json"
    # data_filename = "nasdaq100.json"
    data_filename = "sp500_test.json"

    data = read_json(data_filename)

    for ticker in data["ticker_list"]:
        print("=================================")
        ticker = Ticker(ticker, data["country"])

        print(f"名称:{ticker.name}")
        print(f"証券コード:{ticker.code}")

        # dfデバック
        print(ticker.price_df)

        print(f"last_over_25ma: {ticker.period_list_25ma[0]}")

        if buy_jadge(ticker, 25):
            wr.write(ticker.price_df, f"./out/{ticker.code}.png", f"{ticker.code}  {now.strftime('%m/%d/%Y')}")
            #ps.drow(ticker.price_df)
