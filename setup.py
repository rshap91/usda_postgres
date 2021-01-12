#!/usr/bin/env python
from setuptools import setup
import os

description = 'Demo data analysis tool written in python for exploring USDA food data.'

setup(name='usda_explorer',
      description=description,
      long_description=description,
      author='Rick Shapiro',
      author_email='rick.shapirony@gmail.com',
      packages=['usda_explorer'],
      install_requires=[
          'numpy>=1.15.4',
          'pandas>=0.23.4',
          'sqlalchemy',
          'psycopg2>=2.7.1',
          'matplotlib>=2.2.2',
          'seaborn>=0.9'
	 ],
     entry_points = {
        'console_scripts': [
            'usda_explore = usda_explorer.__main__:main'
        ]
    },
    include_package_data=True
)
