# Copyright (C) 2016 East Asian Observatory
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

from hedwig.file.csv import CSVWriter
from hedwig.type.enum import PublicationType


def write_prev_prop_pub(file_, prev_proposals):
    """
    Write a CSV file of previous proposal publication information.
    """

    writer = CSVWriter()

    writer.add_row([
        'Submitted proposal',
        'Referenced proposal',
        'Publication type',
        'Publication description',
        'Publication author',
        'Publication year',
        'Publication title',
    ])

    for (this_proposal_code, proposals) in prev_proposals.items():
        for proposal in proposals.values():
            for publication in proposal.publications:
                writer.add_row([
                    this_proposal_code,
                    proposal.proposal_code,
                    PublicationType.get_name(publication.type),
                    publication.description,
                    publication.author,
                    publication.year,
                    publication.title,
                ])

    file_.write(writer.get_csv())
