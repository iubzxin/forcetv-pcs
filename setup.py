# -*- coding:utf-8 -*-

import setuptools
from distutils.core import setup

setup(
    name='force',
    version='0.0.1',
    author='iubzxin',
    author_email='641015302@qq.com',
    url='https://github.com/iubzxin/Force_streaming_system_interface',
    packages = setuptools.find_packages(),
    install_requires=[
        'requests',
        'xmltodict',
    ],
    zip_safe=True,
)
