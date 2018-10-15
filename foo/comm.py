#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2018 cyber-life.cn
# thomas@cyber-life.cn
# @2018/05/3
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

import os
import sys
import uuid
import hashlib
import io
import random
import string
import time
import logging


class singleton(object):
    _singleton = None;
    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = object.__new__(cls);
        return cls._singleton;


#获取脚本文件的当前路径
def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    logging.info("path %r", path)
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        logging.info("isdir %r", path)
        return path
    elif os.path.isfile(path):
        logging.info("isfile %r", os.path.dirname(path))
        return os.path.dirname(path)
    else:
        logging.info("others %r", path)
        return path


# file
def split_path(full_path):
    pathname, filename = os.path.split(full_path)
    # double // as separator
    _id = pathname + os.sep + os.sep + filename
    return _id, pathname, filename


# file
def fstat_to_str(st):
    # posix.stat_result(st_mode=33188, st_ino=411445L, st_dev=45831, st_nlink=1,
    # st_uid=1000, st_gid=1000,
    # st_size=4L, st_atime=1525078682, st_mtime=1525078903, st_ctime=1525078903)
    return "%s %d %s %s %s %s %d %d %d %d" % (st.st_mode, st.st_ino, st.st_dev, st.st_nlink,
        st.st_uid, st.st_gid,
        st.st_size, st.st_atime, st.st_mtime, st.st_ctime)


# file
def md5sum(src, callback, length=io.DEFAULT_BUFFER_SIZE):
    calculated = 0
    md5 = hashlib.md5()
    with io.open(src, mode="rb") as fd:
        for chunk in iter(lambda: fd.read(length), b''):
            md5.update(chunk)
            calculated += len(chunk)
            callback(calculated)
    return md5


def hash_pwd(md5pwd, salt):
    md5salt = hashlib.md5(salt).hexdigest()
    ecrypted_pwd = hashlib.md5(md5pwd + md5salt).hexdigest()
    return ecrypted_pwd


# string
def generate_nonce_str(num):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))


def generate_md5(fp):
    m = md5()
    m.update(fp)
    return m.hexdigest()


# string
def generate_uuid_str():
    return str(uuid.uuid1()).replace('-', '')


# string
def name_to_uuid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name.encode('utf-8'))).replace('-', '')


# 生成交易码 W20170728104549633YX8K90
# 总计24位
# 1位 trade_type
# 14位 日期 20170728104549
# 3位 毫秒 633
# 6位 随机数 YX8K90
def generate_trade_no(trade_type):
    timestamp = time.time()
    msec = str(long(timestamp * 1000))[10:13]
    date = timestamp_short_datetime(timestamp)
    rand = generate_nonce_str(6)
    return trade_type + date + str(msec) + rand


def timestamp_short_datetime(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    _format = '%Y%m%d%H%M%S'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _value)
    return _dt


# 时间格式转换
def timestamp_to_date(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    _format = '%Y/%m/%d'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _value)
    return _dt


# 时间格式转换
def timestamp_to_datehour(value):
    #_format = '%Y-%m-%d %H:%M:%S'
    _format = '%Y/%m/%d/%H'
    # value is timestamp(int), eg: 1332888820
    _value = time.localtime(value)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _value)
    return _dt


# 时间格式转换
def datemin_to_timestamp(dt):
     # dt is string
     time.strptime(dt, '%m/%d/%Y %H:%M')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     # "2012-03-28 06:53:40" to timestamp(int)
     _timestamp = time.mktime(time.strptime(dt, '%m/%d/%Y %H:%M'))
     return int(_timestamp)


# 时间格式转换
def current_timestamp():
    return int(time.time())
