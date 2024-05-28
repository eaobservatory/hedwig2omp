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

try:
    from configparser import ConfigParser
except:
    from ConfigParser import SafeConfigParser as ConfigParser


def write_project_ini(file_, telescope, semester, projects):
    """
    Write an OMP project definition file in "ini" format to the given
    file handle.

    For example::

        with open('{}.ini'.format(semester), 'wb') as file_:
            write_project_ini(file, 'JCMT', semester, projects)

    `projects` should be a list of `Project` namedtuples.
    """

    config = ConfigParser()

    config.add_section('info')
    config.set('info', 'semester', semester)
    config.set('info', 'telescope', telescope)

    for project in projects:
        code = project.code
        config.add_section(code)
        if project.continuation is not None:
            config.set(code, 'continuation', project.continuation)

        if project.country is not None:
            config.set(code, 'country', project.country)

        if project.pi is not None:
            config.set(code, 'pi', project.pi)
            config.set(code, 'pi_affiliation', project.pi_affiliation)

        if project.cois is not None:
            config.set(code, 'coi', ','.join(project.cois))
            config.set(code, 'coi_affiliation', ','.join(project.coi_affiliation))

        if project.title is not None:
            config.set(code, 'title', project.title)

        config.set(code, 'band', ','.join(str(x) for x in project.bands))
        config.set(code, 'allocation', str(project.allocation))
        config.set(code, 'tagpriority', str(project.tagpriority))

        if project.tagadjustment is not None:
            config.set(code, 'tagadjustment', str(project.tagadjustment))

        if project.support is not None:
            config.set(code, 'support', project.support)

        if project.expiry is not None:
            config.set(
                code, 'expiry', project.expiry.strftime('%Y-%m-%dT%H:%M:%S'))

    config.write(file_)
