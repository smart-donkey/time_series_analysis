import json,urllib.parse, urllib.request
import time
import csv
from datetime import date
from datetime import timedelta
import low_interface as api
from low_interface import call_raw_api
from yaml import dump, load
import numpy as np

url = 'https://sapi.k780.com'
date_format = '%Y%m%d'


def query_list(params=api.st_list_params):
    return call_raw_api(params)


def request_history_data(request_date, params=api.st_hist_api_params):
    params['date'] = request_date.strftime(date_format)
    return call_raw_api(params)


def query_all(start, end, file_name='st/history', symbol='sh601398', finished=[]):
    days = start - end
    with open('{}_{}_from_{}_to_{}'.format(file_name, symbol, start, end), 'w') as csv_file:
        writer = None
        for di in range(days.days):
            params = api.st_hist_api_params
            params['symbol'] = symbol
            query_date = start - timedelta(di)
            if query_date.isoweekday() in [6, 7]:
                print('skip date : {}'.format(query_date))
                continue
            results = request_history_data(query_date, params)
            if results and type(results) is not str:
                print(results)
                contents_dict = results['lists']
                contents_dict = contents_dict[list(contents_dict.keys())[0]]
                if writer is None:
                    writer = csv.DictWriter(csv_file, fieldnames=contents_dict.keys())
                    writer.writeheader()

                writer.writerow(contents_dict)

            time.sleep(7)

    finished.append(symbol)


if __name__ == '__main__':
    now = date.today()
    # stocklist = query_list()
    with open('log1.yaml', 'r') as f:
         stock_list = load(f)

    st = stock_list['lists']
    symbols = []
    for s in st:
        code = s['symbol']
        if code.find('sh6') > -1 or code.find('sz0') > -1:
            symbols.append(code)

    print(len(symbols))
    st = symbols
    np.random.seed(19)
    marks = np.random.choice(len(st), 500)
    marks = list(marks)

    parts = []
    for m in marks:
        print(m)
        print(st[m])
        parts.append(st[m])
    with open('total_list.yaml', 'w') as f:
        dump(parts, f)

    with open('finished_list.yaml', 'r') as f:
        finished_list = load(f)

    for m in marks:
        start = date(2017, 9, 30)
        interval = 100
        if st[m] in finished_list:
            continue
        query_all(start - timedelta(1), start - timedelta(interval + 1), symbol=st[m], finished=finished_list)
        print('finished list,', finished_list)
