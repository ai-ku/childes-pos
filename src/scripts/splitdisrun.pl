#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;
my $usage = q{Usage: splitdisrun.pl seed foldid iters fold data-name nsub hiddenRatio};
my $seed = shift; 
my $foldId = shift;
my $iter = shift or die("missing iter-> $usage");
my $fold = shift or die("missing fold-> $usage");
my $dataName = shift or die("missing dataname-> $usage");
my $nsub = shift or die("missing nsub-> $usage"); 
my $hiddenRatio = shift; 
my @data = ("anne","aran","eve","naomi","nina","peter");
@data = ($dataName) if ($dataName ne "all");
my $tmp = tempdir("DIS-XXXX", CLEANUP => 1);
my $mike_out = "$tmp/mike.out";
my $mike_err = "$tmp/mike.err";
my $tm = time;
my (@trsizes, @tesizes) = ((),());
my ($trtotal, $tetotal, $total) = (0,0,0);
my ($cattr,$catte) = ("cat ","cat ");

foreach my $dd (@data){
    my $subs = $dd.".sub.gz";
    my $wordsub_out = "$tmp/$dd.pairs";
    my $wordsub_seed = $foldId;
    my $wordsub = "norm.py $nsub > $wordsub_out"; 
    my $cmd = "zcat $subs | " . $wordsub;
    system($cmd);
    my $combine_out = "$tmp/$dd.dis.gz";
    my $combine = "zcat $dd.fre.gz | cut -f1,3,4 | paste - $wordsub_out | gzip > $combine_out";
    system($combine);
    my $trsplit = "crossval.py -w -v -seed $seed -tarFold $foldId -foldNum $fold -d $combine_out 2>$tmp/$dd.wsp.err | split.py 2> $tmp/$dd.te > $tmp/$dd.tr";
#    print STDERR "$trsplit\n";
    system($trsplit);
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
system("echo -1 | gzip > $tmp/foo.gz");
system("zcat $tmp/allte.gz $tmp/foo.gz $tmp/alltr.gz | gzip > $tmp/all.gz");
my $tomike = "zcat  $tmp/all.gz | sub2mikeDis.py 2> $tmp/all.info | split.py 2> $tmp/mikeallte > $tmp/mikealltr";
system($tomike);
my @minfo = split(' ', `cat $tmp/all.info`);
my $datasizes = join(" -d ", @tesizes);

my $runmike = "mike_childes -f $tmp/mikealltr -i $minfo[1] -o $minfo[2] -seed $seed -d $datasizes -iter $iter -t $tmp/mikeallte -r $hiddenRatio > $mike_out 2> $mike_err";
system($runmike);

#### Split answer to individual files to analyze
open(ANS, "$tmp/mike.err") or die("missing mikenet output");
my ($line, $pos) = (0, 0);
open(CUR, ">$tmp/$data[$pos].ans");
while(<ANS>) {
  chomp;
  if ($_ !~ /^(\d+)\s(\d+)$/) {
    print STDERR "SKIP: $_\n"; 
    next;
  }
  if ($pos < @tesizes- 1 && $line == $tesizes[$pos]) {
    close(CUR);
    $pos += 1;
    open(CUR, ">$tmp/$data[$pos].ans");
  } 
  print CUR "$1 $2\n";
  $line += 1;
}
 
my $printTag = @data == 1 ? "" : "all.";
foreach(@data) {
  system("gzip $tmp/$_.te");
  my $analysis = "idx2tag.py $tmp/$_.te.gz $tmp/$_.ans > $_.$printTag"."dis.fold$foldId.out 2> $tmp/$_.dis.fold$foldId.err";
  system($analysis);
}
my @res = split(' ', `cat $mike_out`);
$tm = time - $tm;
for(my $i = 0 ; $i < @data; $i++){
    print join("\t", $seed, $foldId, $data[$i], $res[$i + 1], $tm, $iter, $minfo[0], $minfo[1], $minfo[2], $trsizes[$i], $res[0])."\n";
}
