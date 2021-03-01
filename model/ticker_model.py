from dataclasses import dataclass
from service import price_service as ps
import pandas as pd

dfType = pd.core.frame.DataFrame


@dataclass
class Ticker:
    name: str
    price_df: dfType = None
    trend_25ma = 0
    trend_direction_25ma = 0
    last_line = 0
    last_position_25ma = 0
    deviation_rate_25ma = 0.0
    domination_rate_25ma = 0.0

    def __post_init__(self):

        self.price_df = ps.get_price(self.name)

        self._insert_ma(25)
        self.trend_25ma = self._get_trend(25)
        self.trend_direction_25ma = self._get_trend_direction(25)
        self.last_position_25ma = self._check_last_position(25)
        self.deviation_rate_25ma = self._check_deviation_rate(25)
        self.domination_rate_25ma = self._check_domination_rate(25)

        self._check_last_line()



    def _insert_ma(self, ma_days: int):
        """
        dfに移動平均値を挿入する
        :param ma_days: 移動平均の日数
        :return:
        """
        assert self.price_df is not None
        ma_name = 'MA_' + str(ma_days)

        self.price_df[ma_name] = self.price_df['Close'].rolling(ma_days).mean().round(2)

    def _get_trend_direction(self, ma_days: int) -> int:
        """
   　　　指定の移動平均の方向を返す。
        前日の移動平均値が前々日の移動平均値より大きければ1,小さければ-1を返す。
        """
        ma_name = 'MA_' + str(ma_days)

        if self.price_df.iloc[-1][ma_name] - self.price_df.iloc[-2][ma_name] > 0:
            return 1
        elif self.price_df.iloc[-1][ma_name] - self.price_df.iloc[-2][ma_name] < 0:
            return -1
        else:
            return 0

    def _get_trend(self, ma_days: int) -> int:
        """
        前日を除く過去(ref_days)の終値を参考にトレンドを返す
        """
        ma_name = 'MA_' + str(ma_days)
        ref_days = 4
        last_trend_list = []

        assert self.price_df is not None

        # 日毎の判定
        for n in range(-1 * ref_days, -1):
            if self.price_df.iloc[n]['Close'] - self.price_df.iloc[n][ma_name] > 0:
                last_trend_list.append(1)
            elif self.price_df.iloc[n]['Close'] - self.price_df.iloc[n][ma_name] < 0:
                last_trend_list.append(-1)
            else:
                last_trend_list.append(0)

        print (last_trend_list)

        # 全通りの判定
        if last_trend_list.count(1) == 3:
            return 1
        elif last_trend_list.count(-1) == 3:
            return -1
        else:
            return 0

    def _check_deviation_rate(self, ma_days: int) -> float:
        """
        前日の終値と移動平均値の乖離率を百分率で返す。
        """

        ma_name = 'MA_' + str(ma_days)

        return round(100*(self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1][ma_name]) / self.price_df.iloc[-1]['Close'], 1)

    def _check_domination_rate(self, ma_days:int) -> float:
        """
        終値の移動平均値からの剥離値がロウソクの胴体占める割合
        胴体の中にいる場合のみ値を返す
        """
        ma_name = 'MA_' + str(ma_days)
        band_size = self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1]['Open']

        if  self.price_df.iloc[-2][ma_name] >= self.price_df.iloc[-1]['Open'] and self.price_df.iloc[-2][ma_name] <= self.price_df.iloc[-1]['Close']:
            #陽線に刺さる場合
            deviation_size = self.price_df.iloc[-2]['ma_name'] - self.price_df.iloc[-1]['Open']
            return round(100 * (deviation_size / band_size), 1)

        elif  self.price_df.iloc[-2][ma_name] <= self.price_df.iloc[-1]['Open'] and self.price_df.iloc[-2][ma_name] >= self.price_df.iloc[-1]['Close']:
            #陰線に刺さる場合
            deviation_size = self.price_df.iloc[-2]['ma_name'] - self.price_df.iloc[-1]['Open']
            return (-1) * round(100 * (deviation_size / band_size), 1)

        else:
            return 0

    def _check_last_line(self):
        """
        前日が陽線か陰線かを判定する。
        """
        if self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1]['Open'] > 0:
            self.last_line = 1
        elif self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1]['Open'] < 0:
            self.last_line = -1
        else:
            self.last_line = 0

    def _check_last_position(self, ma_days: int) -> int:
        """
        前日の終値と移動平均値の相対位置を計算する
        """

        ma_name = 'MA_' + str(ma_days)

        if self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1][ma_name] > 0:
            return 1
        elif self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1][ma_name] < 0:
            return -1
        else:
            return 0




