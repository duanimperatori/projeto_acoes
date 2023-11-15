import yfinance as yf
import pandas as pd


with open(f'./notebook/lib.py', 'r') as script_file:
        script_code = script_file.read()
        exec(script_code)

load_years = 15

stocks_df = read_file_csv(tier='extract', table='stock_list', separator=';')
stock_list = list(stocks_df['TICKER'])

def get_stock_price(tickers: list, base_year: str):
    import pandas as pd
    import yfinance as yf

    df = pd.DataFrame()

    for ticker in tickers:

        print(f'Buscando... {ticker}')
        ticker_request = ticker + '.SA'

        data = yf.Ticker(ticker_request).history(f'{base_year}y')
        data.reset_index(inplace=True)

        if df.empty:
            df = data
            df['ticker'] = ticker
        else:
            data['ticker'] = ticker
            df = pd.concat([df, data], ignore_index=True)

    return df

fact_price = get_stock_price(stock_list, load_years)

columns_list = {
    'Date': 'date',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close',
    'Volume': 'volume',
    'Dividends': 'dividends',
    'Stock Splits': 'splits',
    'ticker': 'ticker'
}

fact_price.rename(columns=columns_list, inplace=True)
fact_price = fact_price[columns_list.values()]
fact_price['date'] = fact_price['date'].apply(lambda x: str(x)[0:10])

save_file_csv(df=fact_price, tier='gold', table='fact_price')
