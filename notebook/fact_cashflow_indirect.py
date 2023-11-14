from datetime import date, timedelta
import pandas as pd
from lib import save_file_csv, read_file_csv, get_cvm_financial_statement


number_exercises = 5
end_year = date.today().year
start_year = end_year - number_exercises + 1
year_list = list(range(start_year, end_year + 1))


stocks_df = read_file_csv(tier='extract', table='stock_list', separator=';')
stock_dict = {row['CNPJ']: row['TICKER'] for index, row in stocks_df.iterrows()}
stock_list = list(stocks_df['TICKER'])


cash_flow_ind_df = pd.DataFrame()

for year in year_list:

    if cash_flow_ind_df.empty:
        cash_flow_ind_df = get_cvm_financial_statement('DFC_MI', year=year)
    else:
        cash_flow_ind_df = pd.concat([cash_flow_ind_df, get_cvm_financial_statement('DFC_MI', year=year)], ignore_index=True)


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

fact_cash_flow_indirect = cash_flow_ind_df[column_list.keys()]
fact_cash_flow_indirect = fact_cash_flow_indirect.rename(columns=column_list)
fact_cash_flow_indirect['type'] = 'Indirect Cash Flow'
fact_cash_flow_indirect['period_type'] = 'YTD'
fact_cash_flow_indirect['ticker'] = fact_cash_flow_indirect['cnpj'].map(stock_dict)
fact_cash_flow_indirect = fact_cash_flow_indirect.loc[(~fact_cash_flow_indirect['ticker'].isnull()) & (fact_cash_flow_indirect['order'] == 'ÚLTIMO')]

save_file_csv(df=fact_cash_flow_indirect, tier='gold', table='fact_cash_flow_indirect')
