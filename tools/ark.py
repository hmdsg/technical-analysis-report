import pandas as pd
import requests
import io

url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv"
r = requests.get(url).content

print (r)
#
# df = pd.read_csv(io.BytesIO(r), sep=";")
#
# print (df)