# Copyright (c) 2016, Hugo Herter
# All rights reserved.

import os

from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.md') as file:
    long_description = file.read()

setup(name='React-to-Redis',
      version='0.1',
      description='Propagate updates from your Redis hashes to the state of your React components in Real-Time via WebSockets',
      long_description=long_description,
      author='Hugo Herter',
      author_email='git@hugoherter.com',
      url='https://github.com/hoh/reloadr',
      packages=['react_to_redis'],
      package_data={'react_to_redis': ['react-to-redis.js', 'index.html']},
      install_requires=[
          'aiohttp',
          'asyncio_redis',
          ],
      license='MIT',
      platform='any',
      keywords="reload hot code reloading",
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.4',
                   'Operating System :: POSIX :: Linux',
                   'Intended Audience :: Developers',
                   ],
      )
