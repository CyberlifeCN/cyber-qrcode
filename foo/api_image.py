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

from comm import *
from global_const import *
from base_handler import *

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger
from image_verify import generate_verify_image


@swagger.model()
class ImageResp:
    def __init__(self, errCode, errMsg, code, imgUrl):
        self.errCode = errCode
        self.errMsg = errMsg
        self.code = code
        self.imgUrl = imgUrl


# /api/image-verify
class ApiImageVerifyXHR(tornado.web.RequestHandler):
    @swagger.operation(nickname='post')
    def post(self):
        """
            @description: 生成图片校验码

            @rtype: L{ImageResp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.info("POST %r", self.request.uri)

        _id = generate_uuid_str()
        timestamp = current_timestamp()
        _datehour = timestamp_to_datehour(timestamp)
        path = cur_file_dir()
        logging.debug("got path %r", path)
        if not os.path.exists(path + "/static/image-verify/" + _datehour):
            os.makedirs(path + "/static/image-verify/" + _datehour)

        # To save it
        filepath = path + "/static/image-verify/" + _datehour + "/" + _id + '.gif'
        mstream, _code = generate_verify_image(save_img=True, filepath=filepath)
        img_url = self.request.protocol + "://" + self.request.host
        img_url = img_url + '/static/image-verify/' + _datehour + "/" + _id + '.gif'

        logging.info("Success[200]: generate image-verify code=[%r] img_url=[%r]", _code, img_url)
        self.set_status(200) # Success
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","code":_code,"imageUrl":img_url}))
        self.finish()
