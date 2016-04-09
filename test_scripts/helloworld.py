from tornado.web import RequestHandler
from tornado.web import Application
from tornado.ioloop import IOLoop


class MainHandler(RequestHandler):
    def get(self):
        self.write('hello world')


if __name__ == '__main__':
    app = Application(
        [
            (r'/', MainHandler)
        ]
    )
    app.listen(port=8000, address='0.0.0.0')
    IOLoop.current().start()
