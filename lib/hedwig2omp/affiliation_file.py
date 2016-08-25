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

import sys

from hedwig.util import get_logger

from hedwig2omp.config import get_config

logger = get_logger(__name__)


def write_affiliation_file(file_, affiliations, assignments):
    """
    Write an OMP affiliations file to the specified file handle.
    """

    # Make affiliation lookup table.
    affiliation_codes = {}
    config = get_config()
    for affiliation_code in config.options('affiliation_code'):
        affiliation_name = config.get('affiliation_code', affiliation_code)
        for affiliation in affiliations.values():
            if affiliation.name == affiliation_name:
                affiliation_codes[affiliation.id] = affiliation_code

    lines = []
    for (project, assignment) in assignments.items():
        for (affiliation, fraction) in assignment.items():
            if affiliation == 0:
                logger.warning(
                    'Project {} includes unknown assignment', project)
                continue

            code = affiliation_codes.get(affiliation)
            if code is None:
                if affiliation in affiliations:
                    affiliation = affiliations[affiliation].name
                logger.error('Unknown affiliation: {}', affiliation)
                sys.exit(1)

            lines.append((project, code, fraction))

    for line in lines:
        print(*line, file=file_)
