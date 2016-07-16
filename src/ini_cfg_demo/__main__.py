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
