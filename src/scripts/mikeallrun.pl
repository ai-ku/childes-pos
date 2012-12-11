#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: mikerun.pl runid seed nsub data-name frame train_iterations};
my $runid = shift or die $usage;
my $seed = shift or die $usage;
my $nsub = shift or die $usage;
my $iter = shift or die $usage;
my @data = ("anne","aran","eve","naomi","nina","peter");
my $tmp = tempdir("mikerun-XXXX", CLEANUP => 0);
my $tm = time;
foreach my $dd (@data){
    my $subs = $dd.".sub.gz";
    my $wordsub_out = "$tmp/$dd.pairs.gz";
    my $wordsub = "awk '{for (i=0;i< $nsub;i++) print \$0}' |\	wordsub -s $seed | perl -lane '\@a = split; \$c++;\$subs .= \$a[1] . \" \";if (\$c == $nsub){print \"\$a[0] \$subs\"; \$c =0; \$subs = \"\";}' |gzip > $wordsub_out";
    my $cmd = "zcat $subs | " . $wordsub;
#    print STDERR "cmd:$cmd\n";
    system($cmd);
}

my $mike_info = "$tmp/mike.info";
my $wordsub_mike = "$tmp/all.gz";
my $mike_out = "$tmp/mike.out";
my $mike_err = "$tmp/mike.err";
my $allData = join(" ", @data);
my $tomike = "sub2mike.py $tmp/ $allData 2> $mike_info | gzip > $wordsub_mike";

#print STDERR "tomike:$tomike\n";
system($tomike);
my @minfo = split(' ', `cat $mike_info`);
my $datasizes = join(" -d ", @minfo[4 .. $#minfo]);

my $runmike = "mike_childes -f $wordsub_mike -i $minfo[2] -o $minfo[3] -seed $seed -iter $iter -d $datasizes > $mike_out 2> $mike_err";
system($runmike);
$tm = time - $tm;
my @res = split(' ', `cat $mike_out`);
for(my $i = 0 ; $i < @data; $i++){
    print join("\t", $runid, $seed, $nsub, $data[$i], $res[$i], $tm, $iter, $minfo[2], $minfo[3])."\n";
}
