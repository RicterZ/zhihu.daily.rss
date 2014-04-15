import web
import jinja2 as jj
import urllib2
import json

urls = ('/feed', 'FeedHandler',)

class FeedHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        api_url = 'http://news.at.zhihu.com/api/1.2/news/latest'
        daily_data = self.request(api_url)
        news = daily_data['news']
        for new in news:
            new['content'] = self.request(new['url'])['body']

        return self.render("feed.xml", data=daily_data)

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)

    def request(self, url):
        headers = {'User-Agent': 'ZhihuSB/250.0'}
        request = urllib2.Request(url, headers=headers)
        return json.loads(urllib2.urlopen(request).read())


app = web.application(urls, globals())
application = web.application(urls, globals()).wsgifunc()
env = jj.Environment(loader=jj.FileSystemLoader('templates'), autoescape=True)
if __name__ == "__main__":
    app.run()