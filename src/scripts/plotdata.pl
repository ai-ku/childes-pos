#!/usr/bin/perl -w
use strict;
use Data::Dumper;
use Scalar::Util qw(looks_like_number);

my @colspec;
while(my $cx = shift) {
    my ($c, $x) = split(/=/, $cx);
    die unless defined $c and defined $x;
    $colspec[$c] = $x;
}

my (%cnt, %sum, %sumsq);
while(<>) {
    my @a = split;
    my $keep = 1;
    my ($x, $y);
    for (my $i = 0; $i <= $#a; $i++) {
	next if not defined $colspec[$i];
	if ($colspec[$i] eq 'x') {
	    $x = $a[$i];
	} elsif ($colspec[$i] eq 'y') {
	    $y = $a[$i];
	} elsif ($a[$i] ne $colspec[$i]) {
	    $keep = 0;
	    last;
	}
    }
    next unless $keep;
    die unless defined $x and defined $y;
    $cnt{$x}++;
    $sum{$x} += $y;
    $sumsq{$x} += $y * $y;
}

for my $x (sort {looks_like_number($a) ? $a <=> $b : $a le $b} keys %cnt) {
    my $n = $cnt{$x};
    my $m = $sum{$x} / $n;
    my $v = $sumsq{$x} / $n - $m * $m;
    printf "%s\t%g\t%g\n", $x, $m, sqrt($v);
}
