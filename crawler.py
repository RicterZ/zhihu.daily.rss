"""
A crawler of Zhihu Daily. Run as a scheduled task every hour.
"""
import os
import web
import json
import urllib2


def parser_zhihu():
    """Parse Zhihu Daily API to JSON data"""
    api_url = 'http://news.at.zhihu.com/api/1.2/news/latest'
    daily_data = request(api_url)
    news = daily_data['news']
    for new in news:
        new['content'] = request(new['url'])['body']
    return daily_data


def request(url):
    """Resuest urls with headers"""
    headers = {'User-Agent': 'ZhihuNotMoe/2333'}
    request = urllib2.Request(url, headers=headers)
    return json.loads(urllib2.urlopen(request, timeout=30).read())


def save_data(data):
    """Save data to the database"""
    db.update('json_raw_data', where='id=1', data=json.dumps(data))


# Connent to the database.
db = web.database(dbn='sqlite', db='zhihu.db3')


# Create zhihu.db3 if it don't exist.
if not os.path.exists('./zhihu.db3'):
    db.query('''
        create table json_raw_data (
            id int(4) primary key not null,
            data longtext default null
        );
    ''')
    db.insert('json_raw_data', id=1, data=None)


if __name__ == '__main__':
    data = parser_zhihu()
    save_data(data)
