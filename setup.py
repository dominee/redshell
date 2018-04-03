#!/usr/bin/env python

from setuptools import setup

setup(name='redshell',
      version='1.0',
      description='A RedTeam shell',
      author='Dominee Fromhell',
      author_email='dominee@hell.sk',
      url='https://github.com/dominee/redshell',
      packages=['redshell', 'redshell.builtins'],
      entry_points="""
      [console_scripts]
      redshell = redshell.shell:main
      """,
      )
