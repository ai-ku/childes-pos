#!/usr/bin/perl

use strict;
while(<>){
    chomp;
    my @line = split;
    foreach my $l (@line){
	next if !$l;
        if ($l =~ /(.*?)\/(.*?):/){
	    print "$1\t$2\n";
	}elsif($l =~ /^P/){
	    print "$l\t<U>\n";
	}
	else {die("$l\n");}
    }
}
