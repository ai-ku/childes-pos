#!/usr/bin/perl -w
use strict;
use File::Temp qw/tempdir/;
my $usage = q{Usage: splitwordsubrun.pl  runid seed foldid nsub iters fold data-name hiddenRatio};
my $runid = shift or die("missing runid -> $usage");
my $seed = shift; 
my $foldId = shift;
my $nsub = shift or die("missing nsub-> $usage");
my $iter = shift or die("missing iter-> $usage");
my $fold = shift or die("missing fold-> $usage");
my $dataName = shift or die("missing dataname-> $usage");
my $hiddenRatio = shift; 
my @data = ("anne","aran","eve","naomi","nina","peter");
@data = ($dataName) if ($dataName ne "all");
my $tmp = tempdir("WSUB-XXXX", CLEANUP => 0);
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
    my $wordsub = "awk '{for (i=0;i< $nsub;i++) print \$0}' |\	wordsub -s $wordsub_seed | perl -lane '\@a = split; \$c++;\$subs .= \$a[1] . \" \";if (\$c == $nsub){print \"\$subs\"; \$c =0; \$subs = \"\";}' > $wordsub_out";
    my $cmd = "zcat $subs | " . $wordsub;
    system($cmd);
    my $combine_out = "$tmp/$dd.wsub.gz";
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

my $tomike = "zcat  $tmp/all.gz | sub2mikeSimple.py 2> $tmp/all.info | split.py 2> $tmp/mikeallte | gzip > $tmp/mikealltr.gz";
system($tomike);
my @minfo = split(' ', `cat $tmp/all.info`);
my $datasizes = join(" -d ", @tesizes);

my $runmike = "mike_childes -f $tmp/mikealltr.gz -i $minfo[1] -o $minfo[2] -seed $seed -d $datasizes -iter $iter -t $tmp/mikeallte -r $hiddenRatio > $mike_out 2> $mike_err";
system($runmike);
if (@data == 1) {
  # if we have only one data perform the analysis
  my $analysis = "idx2tag.py $tmp/allte.gz $tmp/mike.err > $data[0].wsub$nsub.fold$foldId.out 2> $tmp/$data[0].wsub$nsub.fold$foldId.err";
  system($analysis);
}
my @res = split(' ', `cat $mike_out`);
$tm = time - $tm;
for(my $i = 0 ; $i < @data; $i++){
    print join("\t", $runid, $seed, $foldId, $nsub, $data[$i], $res[$i + 1], $tm, $iter, $minfo[0], $minfo[1], $minfo[2], $trsizes[$i], $res[0])."\n";
}
