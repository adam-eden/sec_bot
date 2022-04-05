from datetime import date, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from finvizfinance.insider import Insider
from table_lib.plot_table import plot_table
from telegram_api.bot_message import *
import urllib.request

pd.options.mode.chained_assignment = None  # default='warn'

# yesterday's data or y_day = "01-04" if you need a specific date
yesterday = date.today() - timedelta(days=1)
y_day = yesterday.strftime("%d-%m")

# download SPB-exchange's tickers https://spbexchange.ru/ru/listing/securities/list/
file_spb = 'spb_list/spb_list.csv'
url = 'https://spbexchange.ru/ru/listing/securities/list/?csv=download'
urllib.request.urlretrieve(url, file_spb)
ticker_df = pd.read_csv(file_spb, sep=';')
N_ticker = ticker_df['s_RTS_code'].tolist()

# sales
finsider = Insider(option='top week sales')
'''
option: latest, latest buy, latest sales, top week, top week buy, top week sales
default: latest, top owner trade, top owner buy, top owner sales, insider_id - future option
'''
insider_df = finsider.getInsider()
new_df = insider_df.loc[insider_df['Ticker'].isin(N_ticker)]
new_df.columns = ['Тикер', 'Инсайдер', 'Должность', 'Дата', 'Сделка', 'Цена', 'Кол-во',
                  'Сумма,$', 'Остаток акций', 'Дата отчета SEC']

new_df['Кол-во'] = new_df['Кол-во'].replace('', np.nan).astype('Int64')
new_df['Дата отчета SEC'] = pd.to_datetime(new_df['Дата отчета SEC'], format='%b %d %I:%M %p')
new_df['Дата отчета SEC'] = new_df['Дата отчета SEC'].dt.strftime('%d-%m %H:%M')
today_df = new_df[new_df['Дата отчета SEC'].str.contains(y_day)]
today_df['Сумма,$'] = pd.Series(['{:,.2f}'.format(val) for val in today_df['Сумма,$']],
                                index=today_df['Сумма,$'].index, dtype='object')

# Checking for SPB-tickers
if len(today_df['Тикер'].value_counts()) > 0:
    sale_df = today_df.loc[today_df['Сделка'].isin(['Sale'])]
    sale_df = sale_df.loc[:, 'Тикер': 'Сумма,$']
    sale_df2 ='       ' + sale_df.astype(str) + '       '
    sale_df2['Должность'] = '    ' + sale_df2['Должность'] + '    '
    sale_df2['Сумма,$'] = sale_df2['Сумма,$'].str.replace(".00", "", regex=False)

    data = np.vstack((sale_df2.columns.values, sale_df2.values.astype(str)))
    plot_table(data)
    plt.savefig('image_res/sale.jpg')

    tk_df = sale_df.drop_duplicates('Тикер')
    tk_df['Тикер'] = '$' + tk_df['Тикер'].astype(str)
    tickers = ' '.join(tk_df['Тикер'].tolist())

    files = {'photo': open('image_res/sale.jpg', 'rb')}

    send_photo_telegram(files, f'🔥🔥🔥 Интересные инсайдерские продажи на {y_day}-2021\n{tickers}')

else:
    send_text_telegram(f'Интересных инсайдерских продаж на {y_day}-2021 не обнаружено')

# buy
finsider = Insider(option='top week buy')
insider_df = finsider.getInsider()
new_df = insider_df.loc[insider_df['Ticker'].isin(N_ticker)]
new_df.columns = ['Тикер', 'Инсайдер', 'Должность', 'Дата', 'Сделка', 'Цена', 'Кол-во',
                  'Сумма,$', 'Остаток акций', 'Дата отчета SEC']

new_df['Кол-во'] = new_df['Кол-во'].replace('', np.nan).astype('Int64')
new_df['Дата отчета SEC'] = pd.to_datetime(new_df['Дата отчета SEC'], format='%b %d %I:%M %p')
new_df['Дата отчета SEC'] = new_df['Дата отчета SEC'].dt.strftime('%d-%m %H:%M')
today_df = new_df[new_df['Дата отчета SEC'].str.contains(y_day)]
today_df['Сумма,$'] = pd.Series(['{:,.2f}'.format(val) for val in today_df['Сумма,$']],
                                index=today_df['Сумма,$'].index,  dtype = 'object')

if len(today_df['Тикер'].value_counts()) > 0:
    buy_df = today_df.loc[today_df['Сделка'].isin(['Buy'])]
    buy_df = buy_df.loc[:, 'Тикер': 'Сумма,$']
    buy_df2 = '       ' + buy_df.astype(str) + '       '
    buy_df2['Должность'] = '    ' + buy_df2['Должность'] + '    '
    buy_df2['Сумма,$'] = buy_df2['Сумма,$'].str.replace(".00", "", regex=False)
    
    data = np.vstack((buy_df2.columns.values, buy_df2.values.astype(str)))
    plot_table(data)
    plt.savefig('image_res/buy.jpg')

    tk_df2 = buy_df.drop_duplicates('Тикер')
    tk_df2['Тикер'] = '$' + tk_df2['Тикер'].astype(str)
    tickers = ' '.join(tk_df2['Тикер'].tolist())

    files = {'photo': open('image_res/buy.jpg', 'rb')}

    send_photo_telegram(files, f'🔥🔥🔥 Интересные инсайдерские покупки на {y_day}-2021\n{tickers}')

else:
    send_text_telegram(f'Интересных инсайдерских покупок на {y_day}-2021 не обнаружено')

# top sales
finsider = Insider(option='top owner sales')
insider_df = finsider.getInsider()
new_df = insider_df.loc[insider_df['Ticker'].isin(N_ticker)]
new_df.columns = ['Тикер', 'Инсайдер', 'Должность', 'Дата', 'Сделка', 'Цена', 'Кол-во',
                  'Сумма,$', 'Остаток акций', 'Дата отчета SEC']

new_df['Кол-во'] = new_df['Кол-во'].replace('', np.nan).astype('Int64')
new_df['Дата отчета SEC'] = pd.to_datetime(new_df['Дата отчета SEC'], format='%b %d %I:%M %p')
new_df['Дата отчета SEC'] = new_df['Дата отчета SEC'].dt.strftime('%d-%m %H:%M')
today_df = new_df[new_df['Дата отчета SEC'].str.contains(y_day)]
today_df['Сумма,$'] = pd.Series(['{:,.2f}'.format(val) for val in today_df['Сумма,$']],
                                index=today_df['Сумма,$'].index,  dtype = 'object')

if len(today_df['Тикер'].value_counts()) > 0:
    sale_df = today_df.loc[today_df['Сделка'].isin(['Sale'])]
    sale_df = sale_df.loc[:, 'Тикер': 'Сумма,$']
    sale_df2 = '       ' + sale_df.astype(str) + '       '
    sale_df2['Должность'] = '    ' + sale_df2['Должность'] + '    '
    sale_df2['Сумма,$'] = sale_df2['Сумма,$'].str.replace(".00", "", regex=False)

    data = np.vstack((sale_df2.columns.values, sale_df2.values.astype(str)))
    plot_table(data)
    plt.savefig('image_res/sale_top.jpg')

    tk_df = sale_df.drop_duplicates('Тикер')
    tk_df['Тикер'] = '$' + tk_df['Тикер'].astype(str)
    tickers = ' '.join(tk_df['Тикер'].tolist())

    files = {'photo': open('image_res/sale_top.jpg', 'rb')}

    send_photo_telegram(files, f'🔥🔥🔥 Продажи владельцев компаний (доля более 10%) на {y_day}-2021\n{tickers}')

else:
    send_text_telegram(f'Продажи владельцев компаний (доля более 10%) на {y_day}-2021 не обнаружены')

# top buy
finsider = Insider(option='top owner buy')
insider_df = finsider.getInsider()
new_df = insider_df.loc[insider_df['Ticker'].isin(N_ticker)]
new_df.columns = ['Тикер', 'Инсайдер', 'Должность', 'Дата', 'Сделка', 'Цена', 'Кол-во',
                  'Сумма,$', 'Остаток акций', 'Дата отчета SEC']

new_df['Кол-во'] = new_df['Кол-во'].replace('', np.nan).astype('Int64')
new_df['Дата отчета SEC'] = pd.to_datetime(new_df['Дата отчета SEC'], format='%b %d %I:%M %p')
new_df['Дата отчета SEC'] = new_df['Дата отчета SEC'].dt.strftime('%d-%m %H:%M')
today_df = new_df[new_df['Дата отчета SEC'].str.contains(y_day)]
today_df['Сумма,$'] = pd.Series(['{:,.2f}'.format(val) for val in today_df['Сумма,$']],
                                index=today_df['Сумма,$'].index,  dtype = 'object')

if len(today_df['Тикер'].value_counts()) > 0:
    buy_df = today_df.loc[today_df['Сделка'].isin(['Buy'])]
    buy_df = buy_df.loc[:, 'Тикер': 'Сумма,$']
    buy_df2 = '       ' + buy_df.astype(str) + '       '
    buy_df2['Должность'] = '    ' + buy_df2['Должность'] + '    '
    buy_df2['Сумма,$'] = buy_df2['Сумма,$'].str.replace(".00", "", regex=False)

    data = np.vstack((buy_df2.columns.values, buy_df2.values.astype(str)))
    plot_table(data)
    plt.savefig('image_res/buy_top.jpg')

    tk_df2 = buy_df.drop_duplicates('Тикер')
    tk_df2['Тикер'] = '$' + tk_df2['Тикер'].astype(str)
    tickers = ' '.join(tk_df2['Тикер'].tolist())

    files = {'photo': open('image_res/buy_top.jpg', 'rb')}

    send_photo_telegram(files, f'🔥🔥🔥 Покупки владельцев компаний (доля более 10%) на {y_day}-2021\n{tickers}')

else:
    send_text_telegram(f'Покупки владельцев компаний (доля более 10%) на {y_day}-2021 не обнаружены')
