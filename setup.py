#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "lyon"

"""
django-apidocs
--------------
`````
"""
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from setuptools import setup

version = '2.1.3'

# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# https://github.com/pypa/virtualenv/pull/259)

# python setup.py sdist upload

install_requires = ['Django', 'requests', 'six']

long_description = 'Django-Docs'

setup(
    name='django-apidocs',
    version=version,
    url='https://github.com/lyonyang/django-apidocs',
    license='BSD',
    author='Lyon Yang',
    author_email='lyon.yang@qq.com',
    maintainer='Lyon Yang',
    maintainer_email='lyon.yang@qq.com',
    description='Web API docs for Django',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'django_docs'
    ],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
    ],
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        # 'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
