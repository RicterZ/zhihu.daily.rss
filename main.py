import web
import jinja2 as jj
import urllib2
import json

urls = ('/feed', 'FeedHandler',)

class FeedHandler(object):
    def GET(self):
        web.header('Content-type', "text/xml; charset=utf-8")
        daily_data = db.select('json_raw_data', where='1', what='data')[0].data
        return self.render("feed.xml", data=json.loads(daily_data))

    def render(self, template, **kwargs):
        return env.get_template(template).render(**kwargs)


# uWSGI
application = web.application(urls, globals()).wsgifunc()

app = web.application(urls, globals())
db = web.database(dbn='sqlite', db='zhihu.db3')
env = jj.Environment(loader=jj.FileSystemLoader('templates'), autoescape=True)

if __name__ == "__main__":
    app.run()