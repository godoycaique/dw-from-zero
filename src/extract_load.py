import yfinance as yf
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHM = os.getenv('DB_SCHM_PROD')
DB_THRD = os.getenv('DB_THRD_PROD')
DB_TYPE = os.getenv('DB_TYPE_PROD')
DBT_PROF_DIR = os.getenv('DBT_PROF_DIR')


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)

def buscar_dados_commodities(simbolo, periodo= '6mo', intervalo = '1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_no_postgres(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema=schema)

if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema='public')