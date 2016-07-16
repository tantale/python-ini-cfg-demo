from __future__ import absolute_import
from __future__ import print_function

import io
import re
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='ini_cfg_demo',
    version='0.1.0',
    author='Laurent LAPORTE',
    author_email='tantale.solutions@gmail.com',
    url='https://github.com/tantale/python-ini-cfg-demo',
    description="Example of project with two levels of configuration files",
    long_description='%s\n%s' % (
        read('README.rst'),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    platforms=["Linux", "Windows", "OS X"],
    license="MIT License",
    keywords="configuration ini demonstration python setup application installation",
    packages=find_packages("src"),
    package_dir={'': 'src'},
    package_data={
        'ini_cfg_demo': ['IniCfgDemo.ini'],
        '': ["LICENCE.rst"]
    },
    entry_points={
        'console_scripts': [
            'ini_cfg_demo = ini_cfg_demo.__main__:run_ini_cfg_demo',
        ],
    },
)
