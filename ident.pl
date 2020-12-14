#!/usr/bin/env perl
use strict;
use warnings;
my $valid = 'ABCDEFGHJKLMNSTUWXYZ';
sub alpha_to_num {
	my $alpha = $_[0];
	my $sum = 0;
	for (my $key = 0; $key < length($alpha); $key++) {
		my $ch = substr($alpha, $key, 1);
		my $ord = index($valid, $ch);
		return 0 if $ord == -1;
		$sum = $sum * length($valid) + $ord + 1;
	}
	return $sum
}
while (<>) {
    my $obj_prefix;
    my $obj_class;
    my $obj_family;
    my $obj_number;
    my $obj_suffix;
    my $rev_major;
    my $rev_minor;
    my $rev_patch;
    my $rev_preliminary;
    my $rev_devstring;
	# The first regexp matches legacy style preliminary R-states, e.g. PD6
	if (/^(?:(\d*)[\/_]|)(\d{3})[:_](?:(\d{2})[ _]|)(\d{3,5})(?:[\/_](\d*)|)[ _]P([$valid]+)(\d+)(?:[ _-](.*)|$)/) {
		$obj_prefix=$1+0 if $1;
		$obj_class=$2+0;
		$obj_family=$3+0 if $3;
		$obj_number=$4+0;
		$obj_suffix=$5+0 if $5;
		$rev_major=alpha_to_num($6);
		$rev_preliminary=$7+0;
		$rev_devstring=$8;
		chomp $rev_devstring if $8;
	# The second takes care of all other valid forms
	} elsif (/^(?:(\d*)[\/_]|)(\d{3})[:_](?:(\d{2})[ _]|)(\d{3,5})(?:[\/_](\d*)|)[ _](?:P(\d+)|R|)([$valid]+)(?:(\d*)|)(?:([$valid]+)|)(?:[ _-](.*)|$)/) {
		$obj_prefix=$1+0 if $1;
		$obj_class=$2+0;
		$obj_family=$3+0 if $3;
		$obj_number=$4+0;
		$obj_suffix=$5+0 if $5;
		$rev_major=alpha_to_num($7);
		$rev_minor=$8+0 if $8;
		$rev_patch=alpha_to_num($9) if $9;
		$rev_preliminary=$6+0 if $6;
		$rev_devstring=$10;
		chomp $rev_devstring if $10;
	} else {
		$obj_class=0;
		$obj_number=0;
		$rev_major=0;
		$rev_devstring=$_;
		chomp $rev_devstring;
	}
	print "obj_prefix: $obj_prefix\n" if $obj_prefix;
	print "obj_class: $obj_class\n";
	print "obj_family: $obj_family\n" if $obj_family;
	print "obj_number: $obj_number\n";
	print "obj_suffix: $obj_suffix\n" if $obj_suffix;
	print "rev_major: $rev_major\n";
	print "rev_minor: $rev_minor\n" if $rev_minor;
	print "rev_patch: $rev_patch\n" if $rev_patch;
	print "rev_preliminary: $rev_preliminary\n" if $rev_preliminary;
	print "rev_devstring: \"$rev_devstring\"\n" if $rev_devstring;
}
