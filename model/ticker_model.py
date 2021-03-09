from dataclasses import dataclass
from service import price_service as ps
import pandas as pd

pd.set_option('display.max_rows', None)
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
    last_over_25ma = 0

    def __post_init__(self):

        self.price_df = ps.get_price(self.name)

        self._insert_ma(25)
        self._insert_ma_vs_Close(25)
        self._check_last_over(25)
        self.trend_direction_25ma = self._get_trend_direction(25)
        self.deviation_rate_25ma = self._check_deviation_rate(25)

    def _insert_ma(self, ma_days: int):
        """
        dfに移動平均値を挿入する
        :param ma_days: 移動平均の日数
        :return:
        """
        assert self.price_df is not None
        ma_name = 'MA_' + str(ma_days)

        self.price_df[ma_name] = self.price_df['Close'].rolling(ma_days).mean().round(2)

    def _insert_ma_vs_Close(self, ma_days: int):
        """
        dfに指定のmaとcloseの相対位置を挿入する
        :param ma_days: 移動平均の日数
        """
        ma_name = 'MA_' + str(ma_days)
        assert self.price_df is not None

        self.price_df[f"{ma_name}_vs_Close"] = self.price_df['Close'] - self.price_df[ma_name]

    def _check_last_over(self, ma_days: int):
        """
        終値が指定の移動平均線を超えた最後の日にちを検索する
        :param ma_days: 移動平均の日数
        """

        ma_name = 'MA_' + str(ma_days)
        assert self.price_df is not None

        for day in reversed(range(-25, -1)):
            if self.price_df.iloc[day][f"{ma_name}_vs_Close"] > 0:
                self.last_over_25ma = day * (-1)
                break

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

    def get_trend(self, ref_days, ma_days: int) -> int:
        """
        指定日の終値を参考にトレンドを返す
        """
        ma_name = 'MA_' + str(ma_days)

        assert self.price_df is not None

        # 日毎の判定

        if self.price_df.iloc[ref_days]['Close'] - self.price_df.iloc[ref_days][ma_name] > 0:
            return 1
        elif self.price_df.iloc[ref_days]['Close'] - self.price_df.iloc[ref_days][ma_name] < 0:
            return -1
        else:
            return 0


    def _check_deviation_rate(self, ma_days: int) -> float:
        """
        前日の終値と移動平均値の乖離率を百分率で返す。
        """

        ma_name = 'MA_' + str(ma_days)

        return round(
            100 * (self.price_df.iloc[-1]['Close'] - self.price_df.iloc[-1][ma_name]) / self.price_df.iloc[-1]['Close'],
            1)

    def positive_domination_rate(self, ref_day: int, ma_days: int) -> float:
        """
        陽線の移動平均値からの剥離値がロウソクの胴体占める割合
        """

        ma_name = 'MA_' + str(ma_days)


        if self.price_df.iloc[ref_day]['Close'] > self.price_df.iloc[ref_day][ma_name]:

            return 100 * (self.price_df.iloc[ref_day]['Close'] - self.price_df.iloc[ref_day][ma_name]) / (self.price_df.iloc[ref_day]['Close'] - self.price_df.iloc[ref_day]['Open'])

        else:
            return 0

    def check_line(self, ref_day: int) -> int:
        """
        相対的な指定日が陽線か陰線かを判定する。
        """

        if self.price_df.iloc[ref_day]['Close'] - self.price_df.iloc[ref_day]['Open'] > 0:
            return 1
        elif self.price_df.iloc[ref_day]['Close'] - self.price_df.iloc[ref_day]['Open'] < 0:
            return -1
        else:
            return 0
