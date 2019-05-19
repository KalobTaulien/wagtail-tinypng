# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='wagtailtinypng',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Allow image compression through the Wagtail admin using tinypng.com.',
    long_description='For installation instructions see https://github.com/KalobTaulien/wagtail-tinypng',
    url='https://github.com/KalobTaulien/wagtail-tinypng',
    author='Kalob Taulien',
    author_email='kalob@kalob.io',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords='development',
    install_requires=[
        'wagtail>=2.3.0',
        'Django>=2.0',
        'tinify>=1.5.1'
    ]
)
