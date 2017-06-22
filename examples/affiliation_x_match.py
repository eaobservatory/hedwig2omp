#!/usr/bin/env python2

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from collections import defaultdict
import csv
import json
import logging
import sys

nonsense_members = set((
    'TOP-SCOPE collaborators',
    'TOPSCOPE collaborators',
))

logger = logging.getLogger()


def main(filename):
    # Read proposal information file.
    with open(filename, 'r') as file_:
        info = json.load(file_)

    # Go through all proposals and collect information about affiliations.
    affiliation_names = set()
    coi_affiliations = defaultdict(lambda: defaultdict(int))

    for proposal_code in sorted(info.keys()):
        proposal = info[proposal_code]
        proposal_state = proposal['state']
        logger.debug(
            'Reading info for proposal %s (%s)',
            proposal_code, proposal_state)

        pi_affiliation = proposal['member_pi']['affiliation_name']
        affiliation_names.add(pi_affiliation)

        for coi in proposal['member_cois']:
            coi_name = coi['person_name']

            if coi_name in nonsense_members:
                logger.warning('Skipping nonsense member "%s"', coi_name)
                continue

            coi_affiliation = coi['affiliation_name']
            affiliation_names.add(coi_affiliation)

            coi_affiliations[pi_affiliation][coi_affiliation] += 1

    # Change affiliation names to a sorted list.
    affiliation_names = sorted(affiliation_names)

    # Write CSV file.
    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(
        ['PI affiliation'] +
        affiliation_names)

    for pi_affiliation in affiliation_names:
        writer.writerow(
            [pi_affiliation] +
            [coi_affiliations[pi_affiliation][x] for x in affiliation_names])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1])
