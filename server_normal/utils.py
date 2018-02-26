import time
from datetime import datetime


# 对print函数增强，增加了一个时间str
def log(*args, **kwargs):
    format_time = '%Y/%m/%d %H:%M:%S'
    # localtime()默认的是参数是time.time()
    value = time.localtime(int(time.time()))
    dt = time.strftime(format_time, value)
    # 对于No Newline at End of File的问题
    # set "Ensure line feed at file end on Save" under "Editor."
    print(dt, *args, **kwargs)


# 可以用datetime模块试试
def change_time(t):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(t)
    dt = time.strftime(format, value)
    return dt
