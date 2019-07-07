#! /usr/bin/env python
# -*- coding:utf-8 -*-

import time
import urllib
import hashlib
import logging
import requests

class ForceInter(object):

    """
    文档地址: https://www.docin.com/p-508238174.html
    原力FTDS动态管理接口
    接口使用HTTP方式进行交互, 其具体地址为: fdbs.ini 配置的manager_ips.
    注意:
        当涉及大量频道信息更改时, 不建议使用接口, 而建议直接修改数据库, 完成后调用同步接口
    """

    def __init__(self, api, username=None, password=None):
        self._api = api
        self._user = username
        self._pwd = password

    def __requests(self, params):
        auth_params = {
            'time': None,
            'key': None,
        }
        if self._user is not None and self._pwd is not None:
            day = time.strftime('%Y-%m-%d')
            sign = '{}@{}{}'.format(self._user, self._pwd, day)
            auth_params['time'] = day
            md5 = hashlib.md5().update(sign)
            auth_params['key'] = md5.hexdigest()

        params.update(auth_params)

        uri = '{}?{}'.format(self._api.rstrip('?'), urllib.urlencode(params))
        print uri
        logging.info('Send requests. url={}'.format(uri))
        try:
            response = requests.get(url=uri)
        except Exception, e:
            print e
            logging.info('Requests error. errmsg={}'.format(e))
        else:
            print response.status_code
            print response.text

    def query_server_list(self):

        # 读取服务器工作状态
        params = {
            'cmd': "o_if_query_server_list"
        }

        return self.__requests(params)

    def query_channel_info(self, fid):

        # 读取频道信息
        params = {
            'cmd': "o_if_query_channel_info",
            'id': fid,
        }

        return self.__requests(params)

    def add_channel_ftds(self, fid, ftds_id, ftds_id_url=None):

        # 为一个频道添加FTDS服务器
        params = {
            'cmd': "o_if_add_channel_ftds",
            'id': fid,
            'ftdsid': ftds_id,
            'ftds_url_{}'.format(ftds_id): ftds_id_url,
        }

        return self.__requests(params)

    def del_channel_ftds(self, fid, ftds_id):

        # 为一个频道删除FTDS服务器
        params = {
            'cmd': "o_if_del_channel_ftds",
            'id': fid,
            'ftdsid': ftds_id,
        }

        return self.__requests(params)

    def set_channel_ftds(self, fid, ftds_id, ftds_id_url=None):

        # 为一个频道重置FTDS服务器
        params = {
            'cmd': "o_if_set_channel_ftds",
            'id': fid,
            'ftdsid': ftds_id,
            'ftds_url_{}'.format(ftds_id): ftds_id_url,
        }

        return self.__requests(params)

    def sync_all_channel(self):

        # 全局同步全部频道
        params = {
            'cmd': "o_if_sync_all_channel",
        }

        return self.__requests(params)

    def del_film(self, fid):

        # 删除频道
        params = {
            'cmd': "o_if_delfilm",
            'id': fid,
        }

        return self.__requests(params)

    def add_film(self, name, url, ftds_id, vod=True, ai_cdn=0):

        # 添加频道
        if vod:
            vod = 1
            ptl = 'file'
            url = 'file:///' + url.lstrip('file:///')
        else:
            vod = 0
            ptl = 'http'

        params = {
            'cmd': "o_if_addfilm",
            'name': name,
            'url': url,
            'ptlimpl': 'std',
            'vod': vod,
            'ptl': ptl,
            'ai_cdn': ai_cdn,
            'ftdsid': ftds_id,
        }

        return self.__requests(params)


t = ForceInter(api='http://192.99.54.111:56789/admin')
print t.add_film(name='test', ftds_id=11111, url='test')