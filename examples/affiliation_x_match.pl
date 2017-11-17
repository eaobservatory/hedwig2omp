#!/local/perl/bin/perl

use strict;

use IO::File;
use JSON;

my %nonsense_members = map {$_ => 1} (
    'TOP-SCOPE collaborators',
    'TOPSCOPE collaborators',
);

match_affiliations($ARGV[0]);


sub match_affiliations {
    my ($filename) = @_;

    # Read proposal information file.
    my $info;
    do {
        my $f = new IO::File($filename, 'r');
        local $/ = undef;
        $info = decode_json <$f>;
        $f->close();
    };

    # Go through all proposals and collect information about affiliations.
    my %affiliation_names = ();
    my %coi_affiliations = ();

    foreach my $proposal_code (sort keys %$info) {
        my $proposal = $info->{$proposal_code};
        my $proposal_state = $proposal->{'state'};
        print STDERR "Reading info for proposal $proposal_code ($proposal_state)\n";

        my $pi_affiliation = $proposal->{'member_pi'}{'affiliation_name'};
        $affiliation_names{$pi_affiliation} = 1;

        foreach my $coi (@{$proposal->{'member_cois'}}) {
            my $coi_name = $coi->{'person_name'};

            if (exists $nonsense_members{$coi_name}) {
                print STDERR "Skipping nonsense member '$coi_name'\n";
                next;
            }

            my $coi_affiliation = $coi->{'affiliation_name'};
            $affiliation_names{$coi_affiliation} = 1;

            $coi_affiliations{$pi_affiliation}->{$coi_affiliation} ++;
        }
    }

    # Convert affiliation names to a sorted list.
    my @affiliation_names = sort keys %affiliation_names;

    local $, = ',';
    local $\ = "\n";

    # Write CSV file.
    print '"PI affiliation"', map {"\"$_\""} @affiliation_names;

    foreach my $pi_affiliation (@affiliation_names) {
        print "\"$pi_affiliation\"",
            map {$coi_affiliations{$pi_affiliation}->{$_} // 0} @affiliation_names;
    }
}
