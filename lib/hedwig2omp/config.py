# Copyright (C) 2015 East Asian Observatory
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful,but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

from __future__ import absolute_import, division, print_function, \
    unicode_literals

try:
    from configparser import ConfigParser
except:
    from ConfigParser import SafeConfigParser as ConfigParser

import os


config = None


def get_config():
    global config

    if config is None:
        dir_ = os.environ.get('HEDWIG2OMP_DIR', os.getcwd())
        file_ = os.path.join(dir_, 'etc', 'hedwig2omp.ini')
        config = ConfigParser()
        config.read(file_)

    return config
