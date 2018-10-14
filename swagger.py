# _*_ coding: utf-8_*_
#
# genral application route config:
# simplify the router config by dinamic load class
# by thomas
# @2018/05/15

import json
import router

import tornado.ioloop
from tornado.web import RequestHandler, HTTPError
from tornado_swagger import swagger

from foo import comm
from foo import api_client
from foo import api_auth
from foo import api_client_auth


DEFAULT_REPRESENTATION = "application/json"
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404

swagger.docs()


@swagger.model()
class PropertySubclass:
    def __init__(self, sub_property=None):
        self.sub_property = sub_property


@swagger.model()
class Item:
    """
        @description:
            This is an example of a model class that has parameters in its constructor
            and the fields in the swagger spec are derived from the parameters to __init__.
        @notes:
            In this case we would have property1, name as required parameters and property3 as optional parameter.
        @property property3: Item description
        @ptype property3: L{PropertySubclass}
        @ptype property4: C{list} of L{PropertySubclass}
    """
    def __init__(self, property1, property2=None, property3=None, property4=None):
        self.property1 = property1
        self.property2 = property2
        self.property3 = property3
        self.property4 = property4

    def format_http(self):
        return {
            "property1": self.property1,
            "property2": self.property2,
            "property3": self.property3,
            "property4": self.property4,
        }

    @staticmethod
    def item_from_dict(item_dict):
        if item_dict is None:
            return None

        t = Item(None)
        t.property1 = item_dict.get('property1')
        t.property2 = item_dict.get('property2')
        t.property3 = item_dict.get('property3')
        t.property4 = item_dict.get('property4')

        return t

    @classmethod
    def test_classmethod(cls):
        pass


items = {}


@swagger.model()
class App:
    """
        @description:
            This is an example of a app class that has parameters in its constructor
            and the fields in the swagger spec are derived from the parameters to __init__.
        @notes:
            In this case we would have appname, name as required parameters and info as optional parameter.
        @property ver: app version
        @property info: app description
    """
    def __init__(self, appname, ver, info=None):
        self.appname = appname
        self.ver = ver
        self.info = info

    def format_http(self):
        return {
            "appname": self.appname,
            "ver": self.ver,
            "info": self.info,
        }

    @staticmethod
    def item_from_dict(item_dict):
        if item_dict is None:
            return None

        t = App(None)
        t.appname = item_dict.get('appname')
        t.ver = item_dict.get('ver')
        t.info = item_dict.get('info')

        return t

    @classmethod
    def test_classmethod(cls):
        pass


@swagger.model()
class Resp:
    """
        @description:
            This is an example of a app class that has parameters in its constructor
            and the fields in the swagger spec are derived from the parameters to __init__.
        @notes:
            In this case we would have appname, name as required parameters and info as optional parameter.
        @property errCode: 200/400/401/403/404/408/409/412/500
        @property errMsg: Success/Bad Request/No Authorization/Not Found/Conflict/Server Error
        @property rs: result set json
    """
    def __init__(self, errCode, errMsg, rs=None):
        self.errCode = errCode
        self.errMsg = errMsg
        self.rs = rs

    def format_http(self):
        return {
            "errCode": self.errCode,
            "errMsg": self.errMsg,
            "rs": self.rs,
        }

    @staticmethod
    def item_from_dict(item_dict):
        if item_dict is None:
            return None

        t = App(None)
        t.errCode = item_dict.get('errCode')
        t.errMsg = item_dict.get('errMsg')
        t.rs = item_dict.get('rs')

        return t

    @classmethod
    def test_classmethod(cls):
        pass


def make_app():
    return swagger.Application(router.map(), autoreload=True,
        cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=")

if __name__ == "__main__":
    app = make_app()
    app.listen(7001)
    tornado.ioloop.IOLoop.current().start()
