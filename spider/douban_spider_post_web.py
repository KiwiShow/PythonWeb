import os
import requests
from pyquery import PyQuery as pq

'''
1.Downloader下载器  requests(urllib2 urllib urllib3)
2.html页面 -> 结构化的页面 HtmlParser  pyquery(lxml)
3.DataModel
'''
class Model(object):
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def cached_url(url):
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)

        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }

        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movie_from_div(div):
    e = pq(div)
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()

    return m


def movie_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.item')
    movies = [movie_from_div(i) for i in items]
    return movies


def download_image(url):
    folder = 'img'
    name = url.split('/')[-1]
    path = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(path):
        return
    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) 
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
    }
    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)


def up_to_web(title, movies):
    url = 'http://localhost:5000/signin'
    data = {'username': 'ddd', 'password': '444'}
    s = requests.Session()
    s.post(url, data)
    template = '## No: {}  {} \r\nscore={} \r\nquote=({}) \r\n'
    content = ''
    for m in movies:
        content += template.format(m.ranking, m.name, m.score, m.quote)
    url_2 = 'http://localhost:5000/tweet/add?token=test_token&board_id=4'
    data_2 = {'title': title, 'content': content, 'board_id':4}
    s.post(url_2, data_2)


def main():
    # for i in range(0, 250, 25):
    url = 'https://movie.douban.com/top250?start={}'.format(0)
    movies = movie_from_url(url)
    up_to_web('douban_film', movies)
    print('top250 movies', movies)
    [download_image(m.cover_url) for m in movies]


if __name__ == '__main__':
    main()
