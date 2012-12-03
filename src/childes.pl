#!/usr/bin/perl -w
use strict;
use XML::Parser;
use Data::Dumper;
use Switch;
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

my $message;      # Hashref containing infos on a message
my @stack;
my $tree;
my $curId;

### Options
# opt_t : do not merge trail off sentences ow merge
# opt_f : print fragment type words [[word/]] ow do not print
# opt_m : print tokens with empty pos using [[word/]] ow do not print
# opt_p : print pauses ow do not print
# opt_w : only print words
# opt_i : turns of debuging information such as sentence id, file name
# opt_o : print omitted words (none spoken)
# opt_s : concatinate shorthenings (intended not spoken)
# opt_u : print untransribed (ex xxx yyy)
# opt_r : use replacement (ex: gonna => going to)
#my ($opt_t, $opt_f, $opt_m, $opt_p, $opt_w, $opt_i, $opt_o, $opt_s, $opt_u, $opt_r) = (0,0,1,1,1,0,0,0,0,0);
my $opt_t = 0;
my $opt_f = 0;
my $opt_m = 0;
my $opt_p = 0;
my $opt_w = 0;
my $opt_i = 0;
my $opt_o = 0;
my $opt_s = 0;
my $opt_u = 0;
my $opt_r = 0;

# we should really check if it succeeded or not

my $parser = new XML::Parser ( Handlers => {   # Creates our parser object
Start   => \&hdl_start,
End     => \&hdl_end,
Char    => \&hdl_char,
Default => \&hdl_def,
});


# The Handlers
sub hdl_start{
    my ($p, $elt, %atts) = @_;
#    return if $elt eq 'shortening';
    $atts{'_str'} = '';
    $atts{'_elt'} = $elt;
    $atts{'_ch'} = [];
    $message = \%atts; 
    push(@stack, $message);
#    print "push $elt\n";
}

sub hdl_end{
    my ($p, $elt) = @_;
#    return if $elt eq 'shortening';
    my $obj = pop @stack;
#    print "pop $elt $obj->{'_str'}\n";
    if ( $#stack >= 0){
	push(@{$stack[$#stack]->{'_ch'}}, $obj);
    }
    $tree = $obj;
}

sub hdl_char {
    my ($p, $str) = @_;
    return if $str =~ /^\s+$/;
    $stack[$#stack]->{'_str'} .= $str;
}

sub hdl_def { }  # We just throw everything else

sub get_pos_c{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'c' {$pos .= "$_->{'_str'}:";}
	    else { warn("unhandled get_pos_c:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $pos .= "$_->{'_str'}" if @{$w->{'_ch'}} == 0;
    return $pos
}

sub get_pos_s{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 's' {$pos .= "$_->{'_str'}";}
	    else { warn("unhandled get_pos_s:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $pos .= "$_->{'_str'}" if @{$w->{'_ch'}} == 0;
    return $pos
}

sub get_shortening{
    my $w = shift;
    my $str = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 's' {$str .= "$_->{'_str'}";}
	    else { warn("unhandled get_shortening:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $str .= "$_->{'_str'}" if $opt_s == 1 && @{$w->{'_ch'}} == 0;
    return $str;
}

sub get_pos_stem{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'c' {$pos .= "$_->{'_str'}";}
	    else { warn("unhandled get_pos_stem:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $pos .= "$_->{'_str'}" if @{$w->{'_ch'}} == 0;
    return $pos
}

sub get_g_k{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'c' {$pos .= "$_->{'_str'}";}
	    else { warn("unhandled get_g_k:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $pos .= "$_->{'type'}" if @{$w->{'_ch'}} == 0;
    return $pos
}

sub get_g_overlap{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'c' {$pos .= "$_->{'_str'}";}
	    else { warn("unhandled get_g_overlap:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $pos .= "$_->{'type'}" if @{$w->{'_ch'}} == 0;
    return $pos
}

sub get_g_alternative{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'c' {$pos .= "$_->{'_str'}";}
	    else { warn("unhandled get_g_overlap:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    $pos .= "$_->{'type'}" if @{$w->{'_ch'}} == 0;
    return $pos
}

sub get_tagmarker{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'mor' {$pos .= get_word_mor($_);}
	    else { warn("unhandled get_g_tagmarker:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    
    my $str = "P_"."$_->{'type'}";
    return $str;
}

sub get_quotation{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'mor' {$pos .= get_word_mor($_);}
	    else { warn("unhandled get_g_tagmarker:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}}
    my $str .= "P_"."$_->{'type'}";
    return $str;
}

sub get_pos{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'c' {$pos .= get_pos_c($_).":";}
	    case 's' {$pos .= get_pos_s($_).":";}
	    else { warn("unhandled pos:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}
    }
    return $pos;
}

sub get_mw_mk{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	warn("unhandled get_mw_mk:$w->{'_elt'} type:$_->{'_elt'}");
    }
    $pos .= "$_->{'_str'}";
    return $pos;
}

sub get_mwc{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'pos' {$pos .= get_pos($_).":";}
	    case 'stem' {$pos .= get_pos_stem($_).":";}
	    case 'mk' {$pos .= get_mw_mk($_).":";}
	    case 'mw' {$pos .= get_mw($_).":";}
	    else { warn("unhandled[$curId] get_mw:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}
    }
    return $pos;
}

sub get_mw{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'pos' {$pos .= get_pos($_).":";}
	    case 'stem' {$pos .= get_pos_stem($_).":";}
	    case 'mk' {$pos .= get_mw_mk($_).":";}
	    case 'mpfx' {}#prefix no need to extract
	    else { warn("unhandled[$curId] get_mw:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}
    }
    return $pos;
}

sub get_word_mor{
    my $w = shift;
    my $pos = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'mw' {$pos .= get_mw($_);}
	    case 'mwc' {$pos .= get_mwc($_).":";}
	    case 'gra' {}
	    case 'mor-post' {}
	    case 'menx' {}
	    case 'ca-element' {}
	    else { warn("unhandled[$curId] word_mor:$w->{'_elt'} type:$_->{'_elt'}") ;}
	}
    }
    return $pos
}

sub get_word{
    my $w = shift;
    return "" if ($opt_f == 0 && defined $w->{'type'} && $w->{'type'} eq "fragment");
    return "" if ($opt_o == 0 && defined $w->{'type'} && $w->{'type'} eq "omission");
    return "" if ($opt_u == 0 && defined $w->{'untranscribed'});
    my ($str, $mor, $rep) = ($_->{'_str'}, "", "");

    foreach(@{$w->{'_ch'}}){
        switch($_->{'_elt'}){
	    case 'mor' { $mor = get_word_mor($_);}
	    case 'p' {warn("unhandled[$curId]  sub_word:type:$_->{'_elt'}") if $_->{'p'}{'drawl'}}
	    case 'shortening' {$str .= get_shortening($_);}
	    case 'replacement' {$rep = sub_g($_);}
	    case 'wk' {}
	    case 'pos'{}
	    case 'langs' {} #language tag
	    else { warn("unhandled[$curId] get_word:$w->{'_str'} type:$_->{'_elt'}") ;}
	}	
    }
#    print STDERR  "[[$str]]";
    if ($rep =~ /^(.*?)\/(.*?)$/){
	$mor = $2;
	$mor =~ s/ /_/g;
    }
    if($opt_r == 1 && $rep){return $rep;}
    elsif($mor){return $opt_w == 1 ?  "$str" : "$str/$mor";}
    elsif($str =~ /^P_/){return "$str/$mor";}
    elsif($opt_m == 1 && !$mor){return $opt_w == 1 ?  "$str" : "$str/$mor";}
    else {return "";}
}

sub sub_g{
    my $w = shift;
    my $stc = "";
    my $k = "";
    my $overlap = "";
    my $alternative = "";
    foreach(@{$w->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'w' {$stc .= get_word($_)." ";} #word
	    case 't' {my $tt = "P_".$_->{'type'}; $tt =~ s/ /_/g; $stc .= $tt." ";} #punctuation
	    case 'k' {$k = get_g_k($_);}
	    case 'error' {}
	    case 'quotation' { $stc .= get_quotation($_)." ";} #word
	    case 'tagMarker' {$stc .= get_tagmarker($_)." ";}
	    case 'overlap' {$overlap = get_g_overlap($_)." ";}
	    case 's' {$stc .= "P_".$_->{'type'}." "} #punctuation
	    case 'ga' {$overlap = get_g_alternative($_)." ";}
	    case 'g' {$stc .= sub_g($_)." ";}#stressing
	    case 'e' {} #action/skip
	    case 'r' {} #action/skip
	    case 'pause'{ $stc .= "P_".$_->{'symbolic-length'}." " if $opt_p == 1;} #pause of silence
	    else {warn("unhandled[$curId] sub_g:$w->{'_str'} type:$_->{'_elt'}") ;}
	}
    }
#    print "SUB_G IN:$stc\n";
    return $stc;
}

sub get_stc{
    my $s = shift;
    my $stc = "";
    $curId = $s->{'uID'};
    foreach(@{$s->{'_ch'}}){
	switch($_->{'_elt'}){
	    case 'w' { $stc .= get_word($_)." ";} #word
	    case 'tagMarker' { $stc .= get_tagmarker($_)." ";} #word
	    case 'quotation' { $stc .= get_quotation($_)." ";} #word
	    case 'freecode'{}
	    case 'linker' {}
	    case 'postcode' {}
	    case 't' {my $tt = "P_".$_->{'type'}; $tt =~ s/ /_/g; $stc .= $tt." ";} #punctuation
	    case 's' {$stc .= "P_".$_->{'type'}." ";}
	    case 'a' {} #action/skip
	    case 'e' {} #action/skip
	    case 'media' {} #media time stamps/skip
	    case 'internal-media' {} #media time stamps/skip
	    case 'g' {$stc .= sub_g($_);}#stressing
	    case 'pause'{ $stc .= "P_".$_->{'symbolic-length'}. " " if $opt_p == 1;} #pause of silence
	    else { warn("unhandled type:$curId type:$_->{'_elt'}") ;}
	}
    }
    #Filtering sentences
    if ($stc =~ /^P_\w+/){
	$stc = "";
    }
    return $stc
}

sub sub_parti{
    my $obj = shift;
    my %parti;
    foreach(@{$obj->{'_ch'}}){
	die("Missing role field\n") unless(defined $_->{'role'});
	if($_->{'role'} ne 'Child' && $_->{'role'} ne 'Target_Child' && $_->{'id'} ne 'CHI'){
	    $parti{$_->{'id'}} = $_->{'role'};
	    print STDERR "$_->{'id'}/$_->{'role'} ok\n";
	}
	else{
	    print STDERR "$_->{'id'}/$_->{'role'} ignore\n";
	}
    }
    return \%parti;
}

sub stc_loop{
    my $tree = shift;
    my ($parti, %conv);
    foreach(@{$tree->{'_ch'}}){
	if ($_->{'_elt'} eq 'Participants'){
	    $parti = sub_parti($_);
	    unless (%$parti){
		warn("No participants\n");
		last;
	    }
	}
	elsif ($_->{'_elt'} eq 'u' && defined $parti->{$_->{'who'}}){
	    my $stc = "";
	    if($opt_t == 1 && defined $conv{$_->{'who'}} && $conv{$_->{'who'}}[-1] =~ /P_trail_off\s+$/){
		my $s = pop @{$conv{$_->{'who'}}};
		$s =~ s/P_trail_off\s+$//;
		$stc = $s; 
	    }
	    $stc .= get_stc($_);
	    push(@{$conv{$_->{'who'}}}, $stc);	    
	    if($opt_t == 0 || $stc !~ s/P_trail_off\s+$//){
		if($opt_i == 1){
		    print "$curId $stc\n" if $conv{$_->{'who'}}[-1];
		}else{
		    print "$stc\n" if $conv{$_->{'who'}}[-1];
		}
	    }
	}
    }
}


###
#print Dumper($tree);

while(<>){
    next unless $_ =~ /\.xml$/;
    chomp;
    my $f = $_;
    warn("FILE:$f\n");
    print "FILE:$f\n" if $opt_i;
    $parser->parsefile($f);
    stc_loop($tree);
    $tree = {};
}


