import requests as re
import pandas as pd
from io import StringIO
import sqlalchemy as sa

def get_table_name(value):
    dict = {
        'TIME_SERIES_MONTHLY_ADJUSTED': '',
        'TIME_SERIES_INTRADAY': 'stock.intraday_stock'
    }

    return dict.get(value)

class stock:
    def __init__(self, name: str):
        self.data = None
        self.url = None
        self.period = None
        self.list_values = None
        self.stock = name

    def extract(self, period: str, apikey: str, datatype: str, interval: int = None, compact=True):
        interval = '' if interval is None else f'&interval={interval}min'
        compact = '&outputsize=compact' if compact else '&outputsize=full'

        url = f'https://www.alphavantage.co/query?' \
              f'function={period}&symbol={self.stock}&apikey={apikey}&datatype={datatype}{interval}{compact}'
        response = re.get(url)
        if datatype == 'csv':
            decoded_content = response.content.decode('utf-8')
            temp_file = StringIO(decoded_content)
            date_col = temp_file.getvalue().split('\r\n', 1)[0].split(',', 1)[0]
            df = pd.read_csv(temp_file, parse_dates=[date_col])
            df = df.sort_values(date_col)

        self.url = url
        self.period = period
        self.data = df

        return None

    def treat(self, conn):
        last_date = conn.execute("SELECT TO_CHAR(MAX(dt_stock), 'yyyy-mm-dd HH24:MI:ss') FROM stock.intraday_stock").fetchone()[0]

        df = self.data
        rename_cols = {
            df.columns[0]: 'dt_stock', 'open': 'vl_open', 'high': 'vl_high',
            'low': 'vl_low', 'close': 'vl_close', 'volume': 'vl_volume'
        }

        df.insert(0, 'no_stock', ibm_stock.stock)
        df = df.rename(rename_cols, axis=1)
        if last_date is not None:
            df = df.query(f'dt_stock > "{last_date}"')
        df = df[['no_stock', 'dt_stock', 'vl_open', 'vl_close', 'vl_high', 'vl_low', 'vl_volume']]

        self.list_values = df.to_numpy().tolist()

    def load(self, conn):
        query = f"""
            INSERT INTO {get_table_name(self.period)} (no_stock, dt_stock, vl_open, vl_close, vl_high, vl_low, vl_volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        connection = conn.raw_connection()
        conn_cursor = connection.cursor()
        conn_cursor.executemany(query, self.list_values)
        conn_cursor.close()
        connection.commit()
        connection.close()

        return 'Carga finalizada com sucesso!'

    def run_all(self, **kwargs):
        self.extract(period=kwargs['period'], apikey=kwargs['apikey'], datatype=kwargs['datatype'],
                     interval=kwargs['interval'], compact=True if kwargs['interval'] is None else kwargs['interval'])
        self.treat(kwargs['conn'])
        self.load(kwargs['conn'])


if __name__ == '__main__':
    conn_db = sa.create_engine('postgresql+psycopg2://myuser:password@localhost:5432/postgres')
    ibm_stock = stock('IBM')
    ibm_stock.run_all(period='TIME_SERIES_INTRADAY', apikey='0Y1FH212RT9QK39P', datatype='csv', interval=5,
                      compact=None, conn=conn_db)
