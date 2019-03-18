from distutils.core import setup
import setuptools

setup(
    name='Trello Stats',
    version='0.1',
    packages=['trello_stats',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=[
          'requests',
          'pandas',
          'argparse',
          'tabulate'
    ],
)