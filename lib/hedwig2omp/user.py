# Copyright (C) 2015-2024 East Asian Observatory
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

from omp.db.db import OMPDB
from omp.siteconfig import get_omp_siteconfig


class UserDB(object):
    def __init__(self):
        cfg = get_omp_siteconfig()

        self.db = OMPDB(
            server=cfg.get('database', 'server'),
            user=cfg.get('database', 'user'),
            password=cfg.get('database', 'password'))

        self.placeholder = '%s'

    def get_all_users(self):
        result = {}

        with self.db.db.transaction() as c:
            c.execute('SELECT hedwig_id, omp_id FROM omp.omphedwiguser')
            while True:
                row = c.fetchone()
                if row is None:
                    break

                result[row[0]] = row[1]

        return result

    def add_user(self, hedwig_id, omp_id):
        with self.db.db.transaction(read_write=True) as c:
            c.execute(
                'INSERT INTO omp.omphedwiguser (hedwig_id, omp_id)'
                ' VALUES ({0}, {0})'.format(self.placeholder),
                (hedwig_id, omp_id))
