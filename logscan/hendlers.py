import os
import json
import logging
from base64 import urlsafe_b64encode
from tornado.web import RequestHandler, HTTPError
from kazoo.exceptions import NoNodeError


class RestMixin:
    def jsonify(self, **kwargs):
        self.set_header('content-type', 'application/json')
        self.write(json.dumps(kwargs))

    def get_payload(self):
        try:
            return json.loads(self.request.body.decode())
        except Exception as e:
            raise HTTPError(400, log_message=str(e))


class WatcherHandler(RestMixin, RequestHandler):
    def post(self, *args, **kwargs):
        payload = self.get_payload()
        try:
            filename = urlsafe_b64encode(payload['filename'].encode())
            app_id = payload['app_id']
            self.application.zk.ensure_path(os.path.join(self.application.options.root, app_id, filename.decode()))
            self.jsonify(code=200, message='{0} added'.format(payload['filename']))
        except KeyError:
            raise HTTPError(400)
        except Exception as e:
            raise HTTPError(500, log_message=str(e))

    def delete(self, *args, **kwargs):
        filename = urlsafe_b64encode(self.get_argument('filename').encode()).decode()
        app_id = self.get_argument('app')
        recursive = self.get_argument('recursive', None) is not None
        try:
            path = os.path.join(self.application.options.root, app_id, filename)
            logging.info(path)
            self.application.zk.delete(path,
                                       recursive=recursive)
            self.jsonify(code=200, message='{0} deleted'.format(self.get_argument('filename')))
        except NoNodeError:
            raise HTTPError(404)
        except Exception as e:
            raise HTTPError(500, log_message=str(e))