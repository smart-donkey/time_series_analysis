import json,urllib.parse, urllib.request
import time
import csv
from datetime import date
from datetime import timedelta
import low_interface as api
from low_interface import call_raw_api


url = 'https://sapi.k780.com'
date_format = '%Y%m%d'


def query_list(params=api.st_list_params):
    return call_raw_api(params)


def request_history_data(request_date, params=api.st_hist_api_params):
    params['date'] = request_date.strftime(date_format)
    return call_raw_api(params)


def query_all(start, end, file_name='history', symbol='sh601398'):
    days = start - end
    with open('{}_from_{}_to_{}'.format(file_name, start, end), 'w') as csv_file:
        writer = None
        for di in range(days.days):
            params = api.st_hist_api_params
            params['symbol'] = symbol
            results = request_history_data(start - timedelta(di), params)
            if results:
                contents_dict = results[u'lists'][0]
                if writer is None:
                    writer = csv.DictWriter(csv_file, fieldnames=contents_dict.keys())
                    writer.writeheader()

                writer.writerow(contents_dict)

            time.sleep(80)

if __name__ == '__main__':
    now = date.today()
    query_all(now - timedelta(1), now - timedelta(5), symbol='sh601398')
