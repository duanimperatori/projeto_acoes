


def get_root_path():
    from pathlib import Path
    lib_path = Path().resolve()
    root = lib_path.as_posix()
    return root


def save_file_csv(df, tier, table):
    #df.to_csv(f'{get_root_path()}/data/{tier}/{table}.csv', index=False)
    df.to_csv(f'./data/{tier}/{table}.csv', index=False)


def read_file_csv(tier, table, separator):
    import pandas as pd
    #df = pd.read_csv(f'{get_root_path()}/data/{tier}/{table}.csv', sep=separator, encoding='iso-8859-1')
    df = pd.read_csv(f'./data/{tier}/{table}.csv', sep=separator, encoding='iso-8859-1')
    return df


def get_cvm_financial_statement(fs_type: str, year: int):
    """
    financial statements type (fs_type)
    -- BPA - Assets
    -- BPP - Liabilities
    -- DRE - Income Statement
    -- DFC_MI - Indirect Cash Flow
    -- DFC_MD - Direct Cash Flow
    """
    import pandas as pd
    import requests, zipfile
    import os

    url = f'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip'
    arquivo_zip = f'itr_cia_aberta_{year}.zip'
    arquivo_csv = f'itr_cia_aberta_{fs_type}_con_{year}.csv'

    download = requests.get(url)

    with open(arquivo_zip, 'wb') as arquivo_cvm:
        arquivo_cvm.write(download.content)

    arquivo_zip = zipfile.ZipFile(arquivo_zip)

    df = pd.read_csv(arquivo_zip.open(name=arquivo_csv), sep=';', encoding='ISO-8859-1')

    # arquivo_zip.close()
    # os.remove(arquivo_zip.filename)

    return df

