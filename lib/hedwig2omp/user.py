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

from contextlib import closing

from hedwig2omp.config import get_config


class UserDB(object):
    def __init__(self):
        config = get_config()
        driver = config.get('database', 'driver')

        if driver == 'sqlite':
            import sqlite3

            self.db = sqlite3.connect(config.get('database', 'file'))
            paramstyle = sqlite3.paramstyle

        elif driver == 'mysql':
            import mysql.connector

            self.db = mysql.connector.connect(
                host=config.get('database', 'host'),
                database=config.get('database', 'database'),
                user=config.get('database', 'user'),
                password=config.get('database', 'password'))
            paramstyle = mysql.connector.paramstyle

        else:
            raise Exception('Unknown database type "{}"'.format(driver))

        if paramstyle == 'qmark':
            self.placeholder = '?'

        elif paramstyle == 'pyformat':
            self.placeholder = '%s'

        else:
            raise Exception('Unknown parameter style "{}"'.format(paramstyle))

    def get_all_users(self):
        result = {}

        with closing(self.db.cursor()) as c:
            c.execute('SELECT hedwig_id, omp_id FROM user')
            while True:
                row = c.fetchone()
                if row is None:
                    break

                result[row[0]] = row[1]

        return result

    def add_user(self, hedwig_id, omp_id):
        with closing(self.db.cursor()) as c:
            c.execute(
                'INSERT INTO user (hedwig_id, omp_id)'
                ' VALUES ({0}, {0})'.format(self.placeholder),
                (hedwig_id, omp_id))

        self.db.commit()
