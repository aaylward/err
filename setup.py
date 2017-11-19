#!/usr/bin/env python3

from distutils.core import setup

setup(name='pytip',
      version='1.0',
      description='A toy http server',
      author='Andy',
      author_email='aaylward@gmail.com',
      packages=['pytip'],
      install_requires=[
          "python-magic >= 0.4.13",
      ],
     )

