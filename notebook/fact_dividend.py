import pandas as pd


with open(f'./notebook/lib.py', 'r') as script_file:
        script_code = script_file.read()
        exec(script_code)

columns_list = [
    'date',
    'close',
    'dividends',
    'per_dividend',
    'ticker'
]

fact_dividend = read_file_csv(tier='gold', table='fact_price', separator=',')
fact_dividend = fact_dividend.loc[fact_dividend['dividends'] > 0]
fact_dividend['per_dividend'] = fact_dividend['dividends'] / fact_dividend['close']
fact_dividend = fact_dividend[columns_list]

save_file_csv(df=fact_dividend, tier='gold', table='fact_dividend')
