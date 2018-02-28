from jinja2 import Environment, FileSystemLoader
import os.path
import time
from datetime import datetime


# 对print函数增强，增加了一个时间str
# 再次增强log函数，增加了输出到文本的功能
def log(*args, **kwargs):
    format_time = '%Y/%m/%d %H:%M:%S'
    # localtime()默认的是参数是time.time()
    value = time.localtime(int(time.time()))
    dt = time.strftime(format_time, value)
    # 对于No Newline at End of File的问题
    # set "Ensure line feed at file end on Save" under "Editor."
    with open('log.txt', 'a', encoding='utf-8') as f:
        # 不要用f=open() 和 f.close() 的组合，容易忘写 f.close()
        print(dt, *args, **kwargs, file=f)


# jinja模板增强
path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)
