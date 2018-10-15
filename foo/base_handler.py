#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016-2017 7x24hs.com
# thomas@7x24hs.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.web
import logging
import time
import sys
import os
import uuid
import random
import hashlib
from hashlib import md5
import string
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

from comm import *
from global_const import *


class UnauthorizedXHR(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200) # Service Error
        self.write(JSON.dumps({"errCode":401,"errMsg":"Unauthorized"}))
        self.finish()
        return


class UrlNotFoundXHR(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200) # Service Error
        self.write(JSON.dumps({"errCode":404,"errMsg":"Not Found This URL"}))
        self.finish()
        return


class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        # super(BaseHandler, self).write_error(status_code, **kwargs)
        logging.error("%d [Service Error]: %r", status_code, self.request.uri)
        if status_code == 404:
            self.set_status(200) # Service Error
            self.write(JSON.dumps({"errCode":404,"errMsg":"Not Found This Page"}))
            self.finish()
            return
        else:
            self.set_status(200) # Service Error
            self.write(JSON.dumps({"errCode":500,"errMsg":"Service Error"}))
            self.finish()
            return


    def get_access_token(self):
        access_token = self.get_secure_cookie("access_token")
        if access_token:
            logging.debug("got access_token=[%r] from cookie", access_token)
            return access_token
        else:
            try:
                access_token = self.request.headers['Authorization']
                access_token = access_token.replace('Bearer ','')
                logging.debug("got access_token=[%r] from headers", access_token)
                return access_token
            except:
                logging.warn("got access_token=[null] from headers")
                return None


    def get_session_ticket(self):
        access_token = self.get_access_token()
        if not access_token:
            return None
        session_ticket = auth_access_token_dao.auth_access_token_dao().find(access_token)
        return session_ticket


class AuthorizationHandler(BaseHandler):
    def get_current_user(self):
        # Aspect-oriented programming
        logging.debug("AuthInterceptor %r", self.request.uri)
        self.set_secure_cookie("login_next", self.request.uri)

        session_ticket = self.get_session_ticket()
        if session_ticket:
            if session_ticket.has_key("expires_at"):
                expires_at = session_ticket["expires_at"]
                _timestamp = int(time.time())
                if int(expires_at) > _timestamp:
                    if session_ticket["scope"] == SESSION_TICKET_ADMIN:
                        logging.info("AuthInterceptor[200]: %r", self.request.uri)
                        return session_ticket
                    else:
                        logging.warn("AuthInterceptor[401]: %r", self.request.uri)
                        return None
                else:
                    logging.warn("AuthInterceptor[401]: %r", self.request.uri)
                    return None
            else:
                logging.warn("AuthInterceptor[401]: %r", self.request.uri)
                return None
        else:
            logging.warn("AuthInterceptor[401]: %r", self.request.uri)
            return None
