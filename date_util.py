from dateutil.parser import parse
import time


# 1.两组格式不同时间大小的比较(str_dt1='24 Aug 2018', str_dt2='2008-01-01')
def compare(str_dt1, str_dt2):

    dt1 = parse(str_dt1).strftime('%Y-%m-%d')
    dt2 = parse(str_dt2).strftime('%Y-%m-%d')
    fm_dt1 = time.strptime(dt1, "%Y-%m-%d")
    fm_dt2 = time.strptime(dt2, "%Y-%m-%d")

    return fm_dt1 > fm_dt2


result = compare('24 Aug 2018', '2008-01-01')
print(result)
