# -*- coding:utf-8 -*-

import hashlib
import logging
import json
import requests
import time
import xmltodict
from copy import deepcopy
from urllib import urlencode


class ForceTvException(Exception):

    """
    generic force streaming system api exception
    code list:
        4 - Database operation failed.
        9 - Authentication failed.
        10 - Channels don't exist.
        11 - Nonexistent method.
        12 - Other errors.
    """

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class ForceTv(object):

    """
    A python implementation of the force streaming system interface
    The document address:
        https://www.docin.com/p-508238174.html
    Methods list:
        query_server_list
        query_channel_info
        add_channel_ftds
        del_channel_ftds
        set_channel_ftds
        sync_all_channel
        del_film
        add_film
        add_channel_fcdn
        del_channel_fcdn
        set_channel_fcdn
        add_channel_fsrs
        del_channel_fsrs
        set_channel_fsrs
        query_channel_fsrs
    """

    def __init__(self, server, username='', password='', proxy=None, timeout=3):
        """
        Parameters:
            server: Base URI for force streaming web interface
            username: Username used to login into Force Streaming System, default: ''
            password:  Password used to login into Force Streaming System, default: ''
            proxy: Using proxy access, default: None (It's passing a parameter,
            it's not doing anything to it)
            timeout: optional connect and read timeout in seconds, default: 3
        """
        self._url = server if server.endswith('/admin') else server + '/admin'
        self._proxy = {} if proxy is None else proxy

        if username and password:
            day = time.strftime('%Y-%m-%d')
            sign = "{}@{}{}".format(username, password, day)
            md5 = hashlib.md5().update(sign)
            self._params = {'time': day, 'key': md5.hexdigest()}
        else:
            self._params = {}

        self._timeout = timeout
        self._method_prefix = "o_if_"

    def do_request(self, method, **kwargs):
        request_data = deepcopy(self._params)
        request_data['cmd'] = method
        request_data.update(kwargs)
        uri = "{0}?{1}".format(self._url, urlencode(request_data))
        logging.debug("Request: url={}".format(uri))
        try:
            response = requests.get(url=uri, proxies=self._proxy, timeout=self._timeout)
            xml_dict = xmltodict.parse(response.content, encoding='utf-8')
            ret = json.loads(json.dumps(xml_dict))[method]
            ret_code = int(ret['@ret'])
            ret_msg = ret['@reason']
        except KeyError:
            logging.debug('Nonexistent method {0}.'.format(method))
            raise ForceTvException(11, 'Nonexistent method {0}'.format(method))
        except Exception as e:
            logging.debug("Other errors: {}".format(e))
            raise ForceTvException(12, e)
        if ret_code > 0:
            logging.info("Request errors: {}".format(ret_msg))
            raise ForceTvException(ret_code, ret_msg)
        logging.debug("Response Body: {}".format(json.dumps(ret, indent=4, separators=(',', ': '))))
        return ret

    def __getattr__(self, attr):
        """Dynamically create an object class (ie: query_server_list)"""
        def run(**kwargs):
            method = self._method_prefix + attr if not attr.startswith(self._method_prefix) else attr
            return self.do_request(method=method, **kwargs)

        return run
