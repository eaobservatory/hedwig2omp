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

import re
from ConfigParser import SafeConfigParser


def write_project_ini(file_, telescope, semester, projects):
    """
    Write an OMP project definition file in "ini" format to the given
    file handle.

    For example::

        with open('{}.ini'.format(semester), 'wb') as file_:
            write_project_ini(file, 'JCMT', semester, projects)

    `projects` should be a list of `Project` namedtuples.
    """

    config = SafeConfigParser()

    config.add_section('info')
    config.set('info', 'semester', semester)
    config.set('info', 'telescope', telescope)

    for project in projects:
        code = project.code
        config.add_section(code)
        config.set(code, 'country', project.country)
        config.set(code, 'pi', project.pi)
        config.set(code, 'coi', ','.join(project.cois))
        config.set(code, 'title', re.sub('[^ -~]', '?', project.title))
        config.set(code, 'band', ','.join(str(x) for x in project.bands))
        config.set(code, 'allocation', str(project.allocation))
        config.set(code, 'tagpriority', str(project.tagpriority))
        config.set(code, 'support', project.support)

    config.write(file_)
