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

income_statement_df = pd.DataFrame()

for year in year_list:

    if income_statement_df.empty:
        income_statement_df = get_cvm_financial_statement('DRE', year=year)
    else:
        income_statement_df = pd.concat([income_statement_df, get_cvm_financial_statement('DRE', year=year)], ignore_index=True)


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

def determine_period_type(row):
    if row['start_month'] == '01' and row['end_month'] != '03':
        return 'YTD'
    else:
        return 'Quarter'

fact_income_statement = income_statement_df[column_list.keys()]
fact_income_statement = fact_income_statement.rename(columns=column_list)
fact_income_statement['type'] = 'Income Statement'
fact_income_statement['start_month'] = fact_income_statement['start_of_period'].apply(lambda x: str(x)[5:7])
fact_income_statement['end_month'] = fact_income_statement['end_of_period'].apply(lambda x: str(x)[5:7])
fact_income_statement['period_type'] = fact_income_statement.apply(determine_period_type, axis=1)
fact_income_statement['ticker'] = fact_income_statement['cnpj'].map(stock_dict)
fact_income_statement = fact_income_statement.loc[(~fact_income_statement['ticker'].isnull()) & (fact_income_statement['period_type'] == 'Quarter')]

save_file_csv(df=fact_income_statement, tier='gold', table='fact_income_statement')
