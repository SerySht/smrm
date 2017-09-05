from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='smrm',
    version='1.0',
    include_package_data=True,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
            'console_scripts':
                ['smrm = smrm.argparser:main']
            }
)
