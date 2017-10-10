#python
import json,urllib.parse, urllib.request
import time
import csv
from datetime import date
from datetime import timedelta

url = 'https://sapi.k780.com'
date_format = '%Y%m%d'

app_key = '25610'
sign = '1c1ac1b1b72b808815b8cd3ffe0e49d5'


st_list_params = {
  'app' : 'finance.stock_list',
  'category' : 'hs',
  'appkey' : app_key,
  'sign' : sign,
  'format' : 'json',
}

st_hist_api_params = {
  'app' : 'finance.stock_history',
  'symbol' : 'sh600016',
  'date' : '20171009',
  'appkey' : app_key,
  'sign' : sign,
  'format' : 'json',
}

def call_raw_api(params):
    # print('dict params', params)
    params = urllib.parse.urlencode(params)
    print('encoded params', params)
    api_url = '%s?%s' % (url, params)

    results = query_url(api_url)
    if results == -404:
        time.sleep(20)
        # retry only once
        results = query_url(api_url)

    json_results = results
    if json_results is None or json_results == -404:
        return None

    if json_results:
        if int(json_results['success']) == 1:
            return json_results['result']
        else:
            print(json_results['msg'])
            return json_results['msg']

def query_url(api_url):
    try:
        with urllib.request.urlopen(api_url) as f:
            call_back = f.read()
            call_back = call_back.decode('utf8')
            json_results = json.loads(str(call_back))
            return json_results
    except urllib.error.URLError as ex:
        return -404
    except:
        print('unexpected error')
        return None