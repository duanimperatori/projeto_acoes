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


cash_flow_dir_df = pd.DataFrame()

for year in year_list:

    if cash_flow_dir_df.empty:
        cash_flow_dir_df = get_cvm_financial_statement('DFC_MD', year=year)
    else:
        cash_flow_dir_df = pd.concat([cash_flow_dir_df, get_cvm_financial_statement('DFC_MD', year=year)], ignore_index=True)


column_list = {
    'CNPJ_CIA': 'cnpj',
    'DT_REFER': 'base_date',
    'GRUPO_DFP': 'financial_statement_type',
    'MOEDA': 'currency',
    'ESCALA_MOEDA': 'scale',
    'ORDEM_EXERC': 'order',
    'DT_INI_EXERC': 'start_of_period',
    'DT_FIM_EXERC': 'end_of_period',
    'CD_CONTA': 'id_account',
    'DS_CONTA': 'account_description',
    'VL_CONTA': 'value',
    'ST_CONTA_FIXA': 'account_status'
}

fact_cashflow_direct = cash_flow_dir_df[column_list.keys()]
fact_cashflow_direct = fact_cashflow_direct.rename(columns=column_list)
fact_cashflow_direct['type'] = 'Direct Cash Flow'
fact_cashflow_direct['period_type'] = 'YTD'
fact_cashflow_direct['ticker'] = fact_cashflow_direct['cnpj'].map(stock_dict)
fact_cashflow_direct = fact_cashflow_direct.loc[(~fact_cashflow_direct['ticker'].isnull()) & (fact_cashflow_direct['order'] == 'ÚLTIMO')]

save_file_csv(df=fact_cashflow_direct, tier='gold', table='fact_cashflow_direct')
