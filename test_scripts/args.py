import json
from tornado.web import RequestHandler
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.log import app_log


class ArgumentHandler(RequestHandler):
    def get(self):
        self.write('hello {0}'.format(self.get_argument('name')))


class ArgumentsHandler(RequestHandler):
    def get(self):
        self.write('hello {0}'.format(', '.join(self.get_arguments('name'))))


class BodyHandler(RequestHandler):
    def post(self):
        body = json.loads(self.request.body.decode())
        app_log.warning(self.request.body.decode())
        self.write('hello {0}'.format(body['name']))


class PathArgsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write('hello {0}'.format(args[0]))


class PathKwargsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write('hello {0}'.format(kwargs['name']))


if __name__ == '__main__':
    app = Application(
            [
                (r'/', ArgumentHandler),
                (r'/args', ArgumentsHandler),
                (r'/body', BodyHandler),
                (r'/path/args/(.*)', PathArgsHandler),
                (r'/path/kwargs/(?P<name>.*)', PathKwargsHandler)
            ]
    )
    app.listen(port=8001, address='0.0.0.0')
    IOLoop.current().start()
