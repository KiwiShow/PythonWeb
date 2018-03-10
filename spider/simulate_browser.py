import os
from selenium import webdriver
from pyquery import PyQuery as pq

driver = webdriver.PhantomJS()

'''
1.Downloader下载器  webkit -> phantom.js -> selenium
2.html页面 -> 结构化的页面 HtmlParser  pyquery(lxml)
3.DataModel

selenium 模拟js加载，操作，还可以模拟点击
'''
class Model(object):
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n {}>'.format(name, '\n  '.join(properties))
        return s


class RecommendItem(Model):
    def __init__(self):
        self.title = ''
        self.cover_url = ''
        self.abstract = ''


def cached_url(url):
    folder = 'cached_zh'
    filename = url.rsplit('/')[-2] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)

        driver.get(url)
        with open(path, 'wb') as f:
            f.write(driver.page_source.encode())
        content = driver.page_source
        return content


def item_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = RecommendItem()
    m.abstract = e(".post_box_main .text").text()
    m.name = e(".title_box a").text()
    m.cover_url = e('.post_box_img img').attr('src')
    return m


def item_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e(".post_box")
    return [item_from_div(i) for i in items]


def main():
    for i in range(0, 10):
        items = item_from_url("http://zhizhizhi.com/gn/{}/".format(i))
        print(items)
    driver.close()


if __name__ == '__main__':
    main()
