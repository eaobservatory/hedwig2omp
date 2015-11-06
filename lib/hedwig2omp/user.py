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
import sqlite3

from hedwig2omp.config import get_config


class UserDB(object):
    def __init__(self):
        self.db = sqlite3.connect(get_config().get('database', 'file'))

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
            c.execute('INSERT INTO user (hedwig_id, omp_id) VALUES (?, ?)',
                      (hedwig_id, omp_id))

        self.db.commit()
