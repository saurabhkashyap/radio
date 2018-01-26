"""
    cloudplayer.radio.socket
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by the cloudplayer team
    :license: Apache-2.0, see LICENSE for details
"""
import json

import tornado.websocket
import tornado.options as opt


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, request, application, on_open=None, on_close=None):
        super().__init__(request, application)
        self.on_open = on_open
        self.on_close = on_close

    def set_default_headers(self):
        headers = [
            ('Access-Control-Allow-Credentials', 'true'),
            ('Access-Control-Allow-Headers', 'Accept, Content-Type, Origin'),
            ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
            ('Access-Control-Allow-Origin', self.allowed_origin),
            ('Access-Control-Max-Age', '600'),
            ('Content-Language', 'en-US'),
            ('Content-Type', 'application/json'),
            ('Pragma', 'no-cache'),
            ('Server', 'cloudplayer')
        ]
        for header, value in headers:
            self.set_header(header, value)

    def open(self):
        self.on_open(self.ws_connection)

    def on_close(self):
        self.on_close()

    def check_origin(self, origin):
        return origin in opt.options['allowed_origins']

    @property
    def allowed_origin(self):
        proposed_origin = self.request.headers.get('Origin')
        if proposed_origin in opt.options['allowed_origins']:
            return proposed_origin
        return opt.options['allowed_origins'][0]

    @tornado.gen.coroutine
    def options(self, *_, **__):
        self.finish()
