#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: framerun.pl runid seed data_name frame_type train_iteration};

my $runid = shift or die $usage;
my $seed = shift or die $usage;
my $data = shift or die $usage;
my $frame = shift or die $usage;
my $iter = shift or die $usage;
my $tmp = tempdir("framerun-XXXX", CLEANUP => 1);
#print STDERR "$runid $seed $data $frame $tmp $iter\n";
my $mike_info = "$tmp/mike.info";
my $mike_data = "$tmp/wmike.gz";
my $mike_out = "$tmp/mike.out";
my $mike_err = "$tmp/mike.err";
my %frames = ("fre"=>"fre", "fle"=>"fre", "ps"=>"fre", "pr"=>"fre", "apr"=>"prbi", "aps"=>"psbi");
my $label = defined $frames{$frame} ? $frames{$frame} : "";
die("label is $label \n") unless $label;
my $tomike = "tomike.py $data.$label.gz $frame 2> $mike_info | gzip > $mike_data";
my $tm = time;
#print STDERR "$tomike\n";
system($tomike);
my @minfo = split(' ', `cat $mike_info`);
my $runmike = "mike_childes -f $mike_data -i $minfo[2] -o $minfo[3] -seed $seed -iter $iter > $mike_out 2> $mike_err";
#print STDERR "$runmike\n";
system($runmike);

my @res = split(' ', `cat $mike_out`);
$tm = time - $tm;
print join("\t", $runid, $seed, $frame, $res[0], $tm, $iter)."\n";
