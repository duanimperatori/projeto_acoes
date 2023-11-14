import pandas as pd
from lib import save_file_csv, read_file_csv

columns_list = [
    'date',
    'dividends',
    'ticker'
]

fact_dividend = read_file_csv(tier='gold', table='fact_price', separator=',')
fact_dividend = fact_dividend.loc[fact_dividend['dividends'] > 0]
fact_dividend = fact_dividend[columns_list]

save_file_csv(df=fact_dividend, tier='gold', table='fact_dividend')
