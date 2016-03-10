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

from textwrap import fill
import re

from hedwig.type import FormatType

paragraph_break = re.compile('\n\n+')


def write_notes_file(file_, notes):
    """
    Write a text file containing notes recorded by the TAC along with
    their decisions.
    """

    is_first = True
    for (proposal_code, note) in notes.items():
        if is_first:
            is_first = False
        else:
            print('', file=file_)

        print(proposal_code, file=file_)

        if note.format != FormatType.PLAIN:
            print('    Not plain text: please view online.', file=file_)

        else:
            first_paragraph = True
            for paragraph in paragraph_break.split(
                    note.text.replace('\r', '')):
                if first_paragraph:
                    first_paragraph = False
                else:
                    print('', file=file_)

                print(fill(
                    paragraph, width=75,
                    initial_indent='    ', subsequent_indent='    ',
                    break_long_words=False, break_on_hyphens=False
                ), file=file_)
