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

from collections import OrderedDict
import json

from hedwig.astro.coord import CoordSystem


def write_target_file(file_, targets):
    """
    Write an JSON file listing the targets for each project.
    """

    target_objects = OrderedDict()

    # Construct JSON "object" (i.e. a dictionary) for each target with
    # coordinates.
    for (proposal_code, proposal_targets) in targets.items():
        proposal_target_objects = []
        for target in proposal_targets.values():
            if ((target.x is None) or (target.y is None) or
                    (target.system is None)):
                continue

            proposal_target_objects.append({
                'name': target.name,
                'x': target.x,
                'y': target.y,
                'system': CoordSystem.get_name(target.system),
            })

        if proposal_target_objects:
            target_objects[proposal_code] = proposal_target_objects

    # Write the JSON file.
    json.dump(target_objects, file_, indent=4, separators=(',', ': '))

    # Add final line feed.
    print('', file=file_)
