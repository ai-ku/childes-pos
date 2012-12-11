#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: framerun.pl runid seed data_name frame_type train_iteration};

my $runid = shift or die $usage;
my $seed = shift or die $usage;
my $data = shift or die $usage;
my $iter = shift or die $usage;
my $tmp = tempdir("framerun-XXXX", CLEANUP => 0);
#print STDERR "$runid $seed $data $frame $tmp $iter\n";
my $mike_out = "$tmp/mike.out";
my $mike_err = "$tmp/mike.err";

my $tm = time;
my @minfo = split(' ', `cat $data.info`);
my $datasizes = join(" -d ", @minfo[4 .. $#minfo]);
my $runmike = "mike_childes -v -f $data -i $minfo[2] -o $minfo[3] -seed $seed -iter $iter -d $datasizes > $mike_out 2> $mike_err";
#print STDERR "$runmike\n";
system($runmike);
my @data = ("anne","aran","eve","naomi","nina","peter");
my @res = split(' ', `cat $mike_out`);
$tm = time - $tm;

for(my $i = 0 ; $i < @data; $i++){
    print join("\t", $runid, $seed, $data[$i], $res[$i], $tm, $iter, $minfo[2], $minfo[3])."\n";
}
