#python
import json,urllib.parse, urllib.request
import time
import csv
from datetime import date
from datetime import timedelta

url = 'https://sapi.k780.com'
date_format = '%Y%m%d'


hist_api_params = {
    'app': 'finance.shgold_history',
    'goldid': '1051',
    'date': '20170523',
    'appkey': '25610',
    'sign': '1c1ac1b1b72b808815b8cd3ffe0e49d5',
    'format': 'json',
}


def call_raw_api(params):
    print('dict params', params)
    params = urllib.parse.urlencode(params)
    print('encoded params', params)
    api_url = '%s?%s' % (url, params)
    f = urllib.request.urlopen(api_url)
    call_back = f.read()
    call_back = call_back.decode('utf8')
    json_results = json.loads(str(call_back))
    if json_results:
        if int(json_results['success']) == 1:
            return json_results['result']
        else:
            print(json_results['msg'])
            return None


def simple_test():
    params = {
        'app': 'finance.shgold_history',
        'goldid': '1051',
        'date': '20170523',
        'appkey': '25610',
        'sign': '1c1ac1b1b72b808815b8cd3ffe0e49d5',
        'format': 'json',
    }
    # params = urlencode(params)
    # print(params)
    print(call_raw_api(params))


def request_history_data(request_date, data_type):
    params = dict(hist_api_params)
    params['date'] = request_date.strftime(date_format)
    if data_type == 'silver':
        params['goldid'] = '1053'
    # print(params)
    return call_raw_api(params)
    # print(call_raw_api(hist_api_params))


def crawl_all(start, end, file_name='history', data_type='gold'):
    days = start - end
    with open('{}_{}_from_{}_to_{}'.format(data_type, file_name, start, end), 'w') as csv_file:
        writer = None
        for di in range(days.days):
            results = request_history_data(start - timedelta(di), data_type)
            if results:
                contents_dict = results[u'lists'][0]

                if writer is None:
                    writer = csv.DictWriter(csv_file, fieldnames=contents_dict.keys())
                    writer.writeheader()

                writer.writerow(contents_dict)

            time.sleep(80)

if __name__ == '__main__':
    # simple_test()
    now = date.today()
    crawl_all(now - timedelta(1), now - timedelta(100), data_type='silver')
