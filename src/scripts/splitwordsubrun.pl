#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: mikerun.pl runid seed nsub data-name frame train_iterations};
my $runid = shift or die $usage;
my $seed = shift or die $usage;
my $nsub = shift or die $usage;
my $iter = shift or die $usage;
my $ratio = shift or die $usage;
#my @data = ("anne","aran","eve","naomi","nina","peter");
my @data = ("peter");
my $tmp = tempdir("mikerun-XXXX", CLEANUP => 0);
my $mike_out = "$tmp/mike.out";
my $mike_err = "$tmp/mike.err";
my $tm = time;
my (@trsizes, @tesizes) = ((),());
my ($trtotal, $tetotal, $total) = (0,0,0);
my ($cattr,$catte) = ("cat ","cat ");

foreach my $dd (@data){
    my $trsplit = 	"rsplit.py $seed $dd.fre.stat  $dd.fre.gz $ratio 2> $tmp/$dd.wsp | gzip > $tmp/$dd.fsp.gz";
#    print STDERR "$trsplit\n";
    system($trsplit);
    my $subs = $dd.".sub.gz";
    my $wordsub_out = "$tmp/$dd.pairs.gz";
    my $wordsub = "awk '{for (i=0;i< $nsub;i++) print \$0}' |\	wordsub -s $seed | perl -lane '\@a = split; \$c++;\$subs .= \$a[1] . \" \";if (\$c == $nsub){print \"\$a[0] \$subs\"; \$c =0; \$subs = \"\";}' |gzip > $wordsub_out";
    my $cmd = "zcat $subs | " . $wordsub;
#    print STDERR "$cmd\n";
    system($cmd);
    my $combine = "combine_sub.py $tmp/$dd.wsp $wordsub_out > $tmp/$dd.tr 2> $tmp/$dd.te";
#    print STDERR "$combine\n";
    system($combine);
    $cattr .= "$tmp/$dd.tr ";
    $catte .= "$tmp/$dd.te ";
    my @tesize = split(" ",`wc -l $tmp/$dd.te`);
    my @trsize = split(" ",`wc -l $tmp/$dd.tr`);
    push(@trsizes,$trsize[0]);
    push(@tesizes,$tesize[0]+$tetotal);
    $trtotal += $trsize[0];
    $tetotal += $tesize[0];
    $total += $trsize[0] + $tesize[0];
#    print STDERR "$dd tr:$trsize[0]/$trtotal te:$tesize[0]/$tetotal\n";
}
$cattr .= " | gzip > $tmp/alltr.gz";
$catte .= " | gzip > $tmp/allte.gz";
system($cattr);
system($catte);
system("echo -1 |gzip > $tmp/foo.gz");
system("zcat $tmp/allte.gz $tmp/foo.gz $tmp/alltr.gz | gzip > $tmp/all.gz");

my $tomike = "sub2mikeSimple.py $tmp/all.gz 2> $tmp/all.info | split.py 2> $tmp/mikeallte | gzip > $tmp/mikealltr.gz";
system($tomike);
my @minfo = split(' ', `cat $tmp/all.info`);
my $datasizes = join(" -d ", @tesizes);

my $runmike = "mike_childes -v -f $tmp/mikealltr.gz -i $minfo[2] -o $minfo[3] -seed $seed -d $datasizes -iter $iter -t $tmp/mikeallte > $mike_out 2> $mike_err";
system($runmike);
my @res = split(' ', `cat $mike_out`);
$tm = time - $tm;
for(my $i = 0 ; $i < @data; $i++){
    print join("\t", $runid, $seed, $nsub, $data[$i], $res[$i], $tm, $iter, $minfo[2], $minfo[3])."\n";
}

