# -*- coding:utf-8 -*-

import setuptools
from distutils.core import setup

setup(
    name='forcetv-pcs',
    version='0.0.2',
    author='iubzxin',
    author_email='641015302@qq.com',
    url='https://github.com/iubzxin/forcetv-pcs',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'xmltodict',
    ],
    zip_safe=True,
)
