import gevent.monkey
gevent.monkey.patch_all()

import logging
import os
import secrets
import uuid

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options

from mqtt_feed import MqttBackend

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="enable or disable debug mode", type=bool)
define("cookie_key", default=secrets.token_urlsafe(32), help="cookie secret key", type=str)


class Application(tornado.web.Application):
    def __init__(self, feed):
        handlers = [
            (r"/websocket/([a-zA-Z0-9-_=]*)$", FortniteSocketHandler, dict(feed=feed)),
        ]
        settings = dict(
            default_handler_class=NotFoundHandler,
            cookie_secret=options.cookie_key,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class NotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        raise tornado.web.HTTPError(
            status_code=404,
            reason="Invalid resource path."
        )

class FortniteSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, feed):
        self.feed = feed
        self.feed.set_callback(self.send_update)

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self, room=None):
        if not room:
            return

        self.room = room
        self.feed.subscribe(self, room)

    def on_close(self):
        self.feed.unsubscribe(self, self.room)

    @classmethod
    def send_update(cls, client, message):
        logging.info("sending message to client %s", client)
        logging.info(tornado.escape.json_decode(message))
        try:
            client.write_message(tornado.escape.json_decode(message))
        except:
            logging.error("Error sending message", exc_info=True)

    # def send_updates(self, room, message):
    #     if room not in self.feed.clients:
    #         return

    #     logging.info("sending message to %d waiters", len(self.feed.clients[room]))
    #     for client in self.feed.clients[room]:
    #         self.send_update(client, message)


def main():
    feed = MqttBackend()
    feed.start()

    tornado.options.parse_command_line()
    app = Application(feed)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
