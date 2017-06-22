# Copyright (C) 2017 East Asian Observatory
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
from hedwig.facility.jcmt.type import \
    JCMTAncillary, JCMTInstrument, JCMTRequest, JCMTWeather
from hedwig.type.collection import ResultCollection
from hedwig.type.simple import Target


def filter_object(obj_):
    if isinstance(obj_, ResultCollection):
        return [filter_object(x) for x in obj_.values()]

    elif isinstance(obj_, dict):
        return OrderedDict((k, filter_object(v)) for (k, v) in obj_.items())

    elif isinstance(obj_, list):
        return [filter_object(x) for x in obj_]

    elif isinstance(obj_, JCMTRequest):
        result = obj_._replace(
            instrument=JCMTInstrument.get_name(obj_.instrument),
            ancillary=(None if (obj_.ancillary == 0) else
                       JCMTInstrument.get_name(obj_.ancillary)),
            weather=JCMTWeather.get_name(obj_.weather),
        )._asdict()

        result['instrument_ancillary'] = \
            JCMTInstrument.get_name_with_ancillary(
                obj_.instrument, obj_.ancillary)

        return result

    elif isinstance(obj_, Target):
        return obj_._replace(
            system=CoordSystem.get_name(obj_.system))._asdict()

    elif isinstance(obj_, tuple) and hasattr(obj_, '_asdict'):
        return filter_object(obj_._asdict())

    else:
        return obj_


def default_object(obj_):
    return str(obj_)


def write_json_file(file_, proposal_details):
    json.dump(
        filter_object(proposal_details), file_,
        indent=4, separators=(',', ': '),
        default=default_object)
