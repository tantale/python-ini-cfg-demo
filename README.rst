Ini Cfg Demo
============

Example of project with two levels of configuration files:

* LEVEL 1: read the configuration from the sources/application's folder (virtualenv)
* LEVEL 2: read the configuration from the user HOME

Python project structure
------------------------

According to the reference [Packaging and Distributing Projects](https://packaging.python.org/distributing/)
a (modern) Python project should have the following structure.
In the package directory, I add a ``__main__.py`` for the main entry point and a ``IniCfgDemo.ini`` for configuration.

Here is the structure::

    python-ini-cfg-demo/
    +-- MANIFEST.in
    +-- README.rst
    +-- setup.py
    +-- setup.cfg
        src/
        \-- ini_cfg_demo/
            +-- __init__.py
            +-- __main__.py
            \-- IniCfgDemo.ini

Project's configuration
-----------------------

You must add a ``package_data`` entry in you ``setup.py`` to include "IniCfgDemo.ini" in your Source Distribution.

For exemple, here is a small ``setup.py``::

    from distutils.core import setup
    
    from setuptools import find_packages
    
    setup(
        name='my_app',
        version='0.1.0',
        url="http://url/to/your/project",
        author="My NAME",
        author_email="my@email.com",
        packages=find_packages("src"),
        package_dir={'': 'src'},
        package_data={
            'ini_cfg_demo': ['IniCfgDemo.ini'],
        },
    )

For backward compatibility with Python 2.6, you also need a ``MANIFEST.in`` file.

For instance, we can include all ``*.ini`` files::

    include src/ini_cfg_demo/*.ini

To check your configuration, run the following command::

    python setup.py sdist

Default configuration for logging
---------------------------------

The ``IniCfgDemo.ini`` store the default configuration for logging.

    [formatters]
    keys=default
    
    [formatter_default]
    format=%(asctime)s:%(levelname)s:%(message)s
    class=logging.Formatter
    
    [handlers]
    keys=console
    
    [handler_console]
    class=logging.StreamHandler
    formatter=default
    args=tuple()
    
    [loggers]
    keys=root
    
    [logger_root]
    level=DEBUG
    formatter=default
    handlers=console

It has only one logger (the **root** logger), with default handlers and formatters.

Main application
----------------

The ``__main__.py`` is the entry point of the application.

Here is the source code of ``__main__.py``::

    # -*- coding: utf-8 -*-
    import logging.config
    import os.path
    
    import sys
    
    WIN = sys.platform.startswith('win')
    
    
    def _posixify(name):
        return '-'.join(name.split()).lower()
    
    
    def get_app_dir(app_name, roaming=True, force_posix=False):
        if WIN:
            key = roaming and 'APPDATA' or 'LOCALAPPDATA'
            folder = os.environ.get(key)
            if folder is None:
                folder = os.path.expanduser('~')
            return os.path.join(folder, app_name)
        if force_posix:
            return os.path.join(os.path.expanduser('~/.' + _posixify(app_name)))
        if sys.platform == 'darwin':
            return os.path.join(os.path.expanduser(
                '~/Library/Application Support'), app_name)
        return os.path.join(
            os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
            _posixify(app_name))
    
    
    def run_ini_cfg_demo():
        # LEVEL 1: read the configuration from the sources/application's folder (virtualenv)
        ini1_path = os.path.join(os.path.dirname(__file__), "IniCfgDemo.ini")
        logging.config.fileConfig(ini1_path)
        logging.info("Starting...")
    
        # LEVEL 2: read the configuration from the user HOME
        ini2_path = get_app_dir("IniCfgDemo")
        logging.debug('Reading configuration from "{ini2_path}...'.format(ini2_path=ini2_path))
        try:
            logging.config.fileConfig(ini2_path)
        except KeyError:
            logging.warning('Bad logging configuration in "{ini2_path}...'.format(ini2_path=ini2_path))
    
        logging.info("Running...")
    
    
    if __name__ == '__main__':
        run_ini_cfg_demo()

You can add this entry point in your ``setup.py``, like this::

    entry_points={
        'console_scripts': [
            'ini_cfg_demo = ini_cfg_demo.__main__:run_ini_cfg_demo',
        ],
    },

To test the entry point, you can install it with ``pip``::

    pip install -e .

Then you can test your application::

    ini_cfg_demo
    
    2016-07-16 15:47:35,613:INFO:Starting...
    2016-07-16 15:47:35,613:DEBUG:Reading configuration from "/Users/my_name/Library/Application Support/IniCfgDemo...
    2016-07-16 15:47:35,613:WARNING:Bad logging configuration in "/Users/my_name/Library/Application Support/IniCfgDemo...
    2016-07-16 15:47:35,613:INFO:Running...

*Note: the ``ini_cfg_demo`` was launched in a Mac OSX*.

Her it is.
