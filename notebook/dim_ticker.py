import pandas as pd
from pathlib import Path

with open(f'./notebook/lib.py', 'r') as script_file:
        script_code = script_file.read()
        exec(script_code)

columns_names = {
    'CNPJ_CIA': 'cnpj',
    'DENOM_SOCIAL': 'company_name',
    'DT_REG': 'register_date',
    'DT_CANCEL': 'inactive_date',
    'SIT': 'status',
    'SETOR_ATIV': 'segment',
    'PAIS': 'country',
    'UF': 'state',
    'MUN': 'city' 
}


url = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
cadastro_cvm_df = pd.read_csv(url, encoding='ISO-8859-1', delimiter=';')
cadastro_cvm_df = cadastro_cvm_df[columns_names.keys()]
cadastro_cvm_df.rename(columns=columns_names, inplace=True)
cadastro_cvm_df['status'] = cadastro_cvm_df['status'].apply(lambda x: 'ACTIVE' if x == 'ATIVO' else 'INACTIVE')


stock_columns = {
    'CNPJ': 'cnpj',
    'TICKER': 'ticker'
}

stocks_df = read_file_csv(tier='extract', table='stock_list', separator=';')
stocks_df = stocks_df[stock_columns.keys()]
stocks_df.rename(columns=stock_columns, inplace=True)

dim_ticker = pd.merge(cadastro_cvm_df, stocks_df, on='cnpj', how='inner').drop_duplicates('ticker')

save_file_csv(df=dim_ticker, tier='gold', table='dim_ticker')


