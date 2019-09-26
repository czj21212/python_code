# -=-=-=-=-=-=-=-=-=-=-=
# coding=UTF-8
# __author__='Guo Jun'
# Version 1.0.0
# -=-=-=-=-=-=-=-=-=-=-=

#from ConnectDB import connDB, connClose, get_all_data
import urllib.request
from conn_sqlite import SqliteDB
import time

# http://finance.sina.com.cn/iframe/futures_info_cff.js
# http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=AL1809
# http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine5m?symbol=IF1809

# i = '002456.SZ'
# items = 'open, high, low, close'
# table = 'stk_price_forward'
# condition = 'where symbol = \'' + i + '\' and date >= \'2018-06-01\' order by date asc'
# symbol_data = get_all_data(items, table, condition)



def Update_Symbol_List():
    symbols_url = 'http://finance.sina.com.cn/iframe/futures_info_cff.js'
    url_page = urllib.request.urlopen(symbols_url).read().decode('gb2312')
    raw_list = [ i for i in url_page.split() if i.startswith('Array(')]
    raw_list.pop(0)    
    raw_data = []
    for i in raw_list:
        raw_data.append(i.replace('Array(','').replace(');','').replace('"','').split(','))
    sqllite = SqliteDB('tsdata')
    sqllite.insert('fur_info(name,symbol)',raw_data)
    sqllite.close()
    

def Get_Future_Price():
    sqllite = SqliteDB('tsdata')
    select_sql = 'SELECT symbol FROM fur_info;'
    symbol_list = sqllite.select(select_sql)    
#    symbol_list = ['BB2001']
    for symbol in symbol_list:
        if symbol.startswith('IF') or symbol.startswith('IC') or symbol.startswith('IH') or symbol.startswith('TF') or symbol.startswith('TS') or symbol.startswith('T1') :
            symbol_url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine5m?symbol=' + symbol
        else:
            symbol_url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=' + symbol
        try:
            symbol_page = urllib.request.urlopen(symbol_url, timeout=10).read().decode('utf-8')
            print(symbol)
            print(len(symbol_page))
            if len(symbol_page) == 2:
                continue
        #        print(symbol_page)
            symbol_page = symbol_page.replace('["','["' + symbol + '",').replace('[[','').replace(']]','').replace('"','').split('],[')
            symbol_data = []
            for i in symbol_page:
                symbol_data.append(i.replace('"','').split(',')) 
            sqllite.insert('fur_price_5m',symbol_data)
        except Exception as error:
            print(error)
            print(symbol_url)
        time.sleep(2)
        
    sqllite.close()


#Update_Symbol_List()
Get_Future_Price()