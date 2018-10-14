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
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from comm import *
from global_const import *
from base_handler import *

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger
from image_verify import generate_verify_image


# /api/image-verify
class ApiImageVerifyXHR(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)

        _id = str(uuid.uuid1()).replace('-', '')
        _date = timestamp_date(time.time())
        path = cur_file_dir()
        logging.info("got path %r", path)
        if not os.path.exists(path + "/static/image-verify/" + _date):
            os.makedirs(path + "/static/image-verify/" + _date)

        # To save it
        filepath = path + "/static/image-verify/" + _date + "/" + _id + '.gif'

        mstream, strs = generate_verify_image(save_img=True, filepath=filepath)
        logging.info("got code %r", strs)

        img_url = self.request.protocol + "://" + self.request.host
        img_url = img_url + '/static/image-verify/' + _date + "/" + _id + '.gif'
        logging.info("got img_url %r", img_url)

        self.set_status(200) # Success
        self.write(JSON.dumps({"err_code":200,"err_msg":"Success","code":strs,"image_url":img_url}))
        self.finish()
