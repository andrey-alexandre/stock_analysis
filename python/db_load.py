import requests as re
import pandas as pd
import matplotlib.pyplot as plt
import math
from io import StringIO


def extract_data(function, symbol, outputsize='compact'):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&apikey=demo'
    r = re.get(url)
    data = r.json()

    return data

def load_data():
    pass

if __name__ == '__main__':
    data = extract_data('TIME_SERIES_DAILY_ADJUSTED', 'IBM')
    df = pd.DataFrame.from_dict(data = data['Time Series (Daily)'], orient='index').astype(float)
    # df['1. open'].plot(ax=ax)



    url1 = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=demo'
    r = re.get(url1)
    decoded_content = r.content.decode('utf-8')
    TESTDATA = StringIO(decoded_content)
    df = pd.read_csv(TESTDATA,  parse_dates=['time'])
    df.describe()
    plt.switch_backend("qt5agg")
    fig, ax = plt.subplots()
    for column in df.columns:
        if df.columns.to_list().index(column) != 0:
            ind_col = math.floor(df.columns.to_list().index(column) % 4)
            ind_row = math.floor(df.columns.to_list().index(column) / 4)
        else:
            ind_row = ind_col = 0
        print(f'Data={column}, row={ind_row}, col={ind_col}')
        df.plot(xd='date', y=column, ax=ax[ind_row, ind_col])  # pd.DataFrame(np.random.randn(10, 3)).plot(ax=ax)
    plt.pause(100)
