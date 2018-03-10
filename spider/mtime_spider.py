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
    folder = 'mtime'
    if url.find('index') == -1:
        filename = '1.html'
    else:
        filename = url.split('-', 1)[-1].split('.')[0] + '.html'
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


def movie_from_li(li):
    e = pq(li)
    m = Movie()
    m.name = e('.px14').find('a').text()
    m.score = e('.total').text() + e('.total2').text()
    m.quote = e('.mt3').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.number').find('em').text()

    return m


def movie_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('#asyncRatingRegion')('li')
    movies = [movie_from_li(i) for i in items]
    return movies


def download_image(url):
    folder = 'img_mtime'
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


def main():
    for i in range(1, 11):
        if i == 1:
            url = 'http://www.mtime.com/top/movie/top100/'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i)
        movies = movie_from_url(url)
        print('top100 movies', movies)
        [download_image(m.cover_url) for m in movies]


if __name__ == '__main__':
    main()
