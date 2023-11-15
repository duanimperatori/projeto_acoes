from datetime import date, timedelta
import pandas as pd

with open(f'./notebook/lib.py', 'r') as script_file:
        script_code = script_file.read()
        exec(script_code)

number_exercises = 5
end_year = date.today().year
start_year = end_year - number_exercises + 1
year_list = list(range(start_year, end_year + 1))


stocks_df = read_file_csv(tier='extract', table='stock_list', separator=';')
stock_dict = {row['CNPJ']: row['TICKER'] for index, row in stocks_df.iterrows()}
stock_list = list(stocks_df['TICKER'])


asset_df = pd.DataFrame()
liabilities_df = pd.DataFrame()

for year in year_list:

    if asset_df.empty:
        asset_df = get_cvm_financial_statement('BPA', year=year)
    else:
        asset_df = pd.concat([asset_df, get_cvm_financial_statement('BPA', year=year)], ignore_index=True)

    if liabilities_df.empty:
        liabilities_df = get_cvm_financial_statement('BPP', year=year)
    else:
        liabilities_df = pd.concat([liabilities_df, get_cvm_financial_statement('BPP', year=year)], ignore_index=True)


column_list = {
    'CNPJ_CIA': 'cnpj',
    'DT_REFER': 'base_date',
    'GRUPO_DFP': 'financial_statement_type',
    'MOEDA': 'currency',
    'ESCALA_MOEDA': 'scale',
    'ORDEM_EXERC': 'order',
    'DT_FIM_EXERC': 'end_of_period',
    'CD_CONTA': 'id_account',
    'DS_CONTA': 'account_description',
    'VL_CONTA': 'value',
    'ST_CONTA_FIXA': 'account_status',
    'VL_CONTA': 'value'
}


temp_asset_df = asset_df[column_list.keys()]
temp_asset_df = temp_asset_df.rename(columns=column_list)
temp_asset_df['type'] = 'Assets'
temp_asset_df['period_type'] = 'YTD'

temp_liabilities_df = liabilities_df[column_list.keys()]
temp_liabilities_df = temp_liabilities_df.rename(columns=column_list)
temp_liabilities_df['type'] = 'Liabilities'
temp_liabilities_df['period_type'] = 'YTD'

fact_balance = pd.concat([temp_asset_df, temp_liabilities_df], ignore_index=True)
fact_balance['ticker'] = fact_balance['cnpj'].map(stock_dict)
fact_balance = fact_balance.loc[(~fact_balance['ticker'].isnull()) & (fact_balance['order'] == 'ÚLTIMO')]

save_file_csv(df=fact_balance, tier='gold', table='fact_balance')
