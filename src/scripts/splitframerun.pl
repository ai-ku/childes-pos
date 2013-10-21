#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;

my $usage = q{Usage: framerun.pl runid seed foldid frame_type train_iteration fold dataName};

my $runid = shift or die $usage;
my $seed = shift;
my $foldId = shift;
my $frame = shift or die("missing frame-> $usage");
my $iter = shift or die("missing iter-> $usage");
my $fold = shift or die("missing fold-> $usage");
my $dataName = shift or die("missing dataname-> $usage");
my @data = ("anne","aran","eve","naomi","nina","peter");
@data = ($dataName) if ($dataName ne "all");
my $tmp = tempdir("FRAME-XXXX", CLEANUP => 1);
#print STDERR "$runid $seed $frame $tmp $iter\n";
my $mike_out = "$tmp/mike.out";
my $mike_err = "$tmp/mike.err";
my $tm = time;
my (@trsizes, @tesizes) = ((),());
my ($trtotal, $tetotal, $total) = (0,0,0);
my ($cattr,$catte) = ("cat ","cat ");
foreach my $dd (@data){
    my $trsplit = "crossval.py -v -seed $seed -tarFold $foldId -foldNum $fold -d $dd.fre.gz 2> $tmp/$dd.split.err | gzip > $tmp/$dd.fsp.gz";
    system($trsplit);
    print STDERR "$trsplit\n";
    my $testtrain =  "zcat $tmp/$dd.fsp.gz | split.py  2> $tmp/$dd.te > $tmp/$dd.tr";
#    print STDERR "$testtrain\n";
    system($testtrain);
    $cattr .= "$tmp/$dd.tr ";
    $catte .= "$tmp/$dd.te ";
    my @tesize = split(" ",`wc -l $tmp/$dd.te`);
    my @trsize = split(" ",`wc -l $tmp/$dd.tr`);
    push(@trsizes,$trsize[0]);
    push(@tesizes,$tesize[0]+$tetotal);
    $trtotal += $trsize[0];
    $tetotal += $tesize[0];
    $total += $trsize[0] + $tesize[0];
#    print STDERR "$dd tr:$trsize[0] t:$trtotal te:$tesize[0] t:$tetotal ALL:$total\n";
}

$cattr .= " | gzip > $tmp/alltr.gz";
$catte .= " | gzip > $tmp/allte.gz";
system($cattr);
system($catte);
system("echo -1 |gzip > $tmp/foo.gz");
system("zcat $tmp/allte.gz $tmp/foo.gz $tmp/alltr.gz | gzip > $tmp/all.gz");
#print STDERR "tr:$cattr\nte:$catte\n";
my $tomike = "zcat $tmp/all.gz | tomikesparse.py $frame  2> $tmp/all.info | split.py  2> $tmp/allte | gzip > $tmp/alltr.gz";
system($tomike);
#print STDERR "$tomike\n";
my @minfo = split(' ', `cat $tmp/all.info`);
my $datasizes = join(" -d ", @tesizes);
my $runmike = "mike_childes -f $tmp/alltr.gz -i $minfo[1] -o $minfo[2] -seed $seed -d $datasizes -iter $iter -t $tmp/allte > $mike_out 2> $mike_err";
#print STDERR "$runmike\n";
system($runmike);
if (@data == 1) {
  # if we have only one data perform the analysis
  my $convert = "zcat $tmp/allte.gz | cut -f1,3,4 | gzip > $tmp/tmpanal.gz";
  system($convert);
  my $analysis = "idx2tag.py $tmp/tmpanal.gz $tmp/mike.err > $data[0].$frame.fold$foldId.out 2> $tmp/analysis.err";
  system($analysis);
}

my @res = split(' ', `cat $mike_out`);
$tm = time - $tm;

for(my $i = 0 ; $i < @data; $i++){
     print join("\t", $runid, $seed, $foldId, $data[$i], $frame, $res[$i], $tm, $iter, $minfo[0], $minfo[1], $minfo[2], $trsizes[$i])."\n";
}
