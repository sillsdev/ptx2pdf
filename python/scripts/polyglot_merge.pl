#!/usr/bin/perl -w
# This file is copyright (c) SIL 2006-2021
# It is provided as-is, with no express or implied guarantee that it will do anything.
# It is in extended beta test, please check its output carefully.
#
# You may use it and distribute it under terms of the Perl Artistic Licence 2.0:
# https://www.perlfoundation.org/artistic-license-20.html
#
use strict;
my $logging=0;
my $maxcols=0;
my (@chunkline,@chunkdata,@pos);
my %active; # all active tokens;
my $activeheading=4;  # level to set active{heading} to
my $activepar=4;  # level to set the active{par} to
my $maxactive=5;
my $fragment=3; # level to set the verse fragment to
my $savelimit=0;
my @usingcl=(0,0);
my @scores; # how important is a potential break-point on each side?
my %chunkscore;
my %chunkcounts;
my %isparag; # are these tokens paragraph marks
my %isheading; # level of section (needed if we're skipping stuff)
my %majorheading; # are these tokens major sections 
my %keep_with_chapter;
my @ranges=();
my @sides=('L','R','A','B','C','D');
my @chunk=("","");
my $startposition='000::000::000::000:::::';
my @position;
my @numeric=(0,1,1,1,0,0,0,0); # which positions have numbers
my @inrange;
my @partype=('','');
my @heading;
my @headingstack=(['','','',''],['','','']);
my @oldhead=(['','','',''],['','','']);
my @first_inrange; # Shortcut to the start of interesing data
my $logfile=undef;
my $debug="merge.dbg" ;#undef; # ".diglot.dbg";
if (defined($ENV{'DEBUG'})) {
	$debug=$ENV{'DEBUG'};
}
# Could do this in less memory, but it's way easier like this
sub readfile {
	my ($name)=@_;
	my @result;
	logit(undef,"Opening $name");
	open(FILE,"<",$name) || die($name.": $!");
	my $firstline=<FILE>;
	local $/;
	$/=undef;
	if ($firstline=~/\\c\s*0\s*$/) {
		logit(undef,"Swallowing first line $firstline");
		$firstline='';
	} else {
		logit(undef,"First line $firstline");
	}
	if (defined($debug)) {
		print DBG "Active: ".join(',',keys %active)."\n";
	}
	my $re='(\\\\(?:'.join("|",keys(%active)).")\\b)";
	@result=map {s/\r\n/\n/g;s/\x{FEFF}//;$_} map {split(/$re/)} ($firstline,<FILE>);
	close(FILE);
	if (defined($debug)) {
		foreach my $l (0..$#result) {
			printf DBG ("%06d: %s\n",$l,$result[$l]);
		}
	}
	logit(undef,"Closed $name");
	return @result;
}

sub makeheading {
	my ($s,$n,$ht,$major)=@_;
	$isheading{$s}=$n+1;
	$active{$s}=$ht;
	if ($major) {
		$majorheading{$s}=1;
	}
	if ($s =~ s/2$/1/) { # if there's a X2 then make X1 equivalent to the previous level
		$isheading{$s}=$n;
		$active{$s}=$ht; # 
	}
}
	
sub logit { # Gerneral purpose logging routine
	my ($side)=shift(@_);
	if ($logging) {
		if (defined($side)) {
			print LOG (join(" ",$sides[$side],$position[$side],@_)."\n") if (defined($logfile));
			print DBG (join(" ",$sides[$side],$position[$side],@_)."\n") if (defined($debug));
		} else {
			print LOG (join(" ",@_)."\n") if (defined($logfile));
			print DBG (join(" ",@_)."\n") if (defined($debug));
		}
	}
}

sub updpos { # generate an updated position array
	my ($idx,$val,$aryref)=@_;
	${$aryref}[$idx]=$val;
	while($idx<=$maxactive) { 
		++$idx;
		if ($numeric[$idx]) {
			$$aryref[$idx]='000';
		} else {
			$$aryref[$idx]='_';
		}
	}
}

sub isnewverse { # read ahead to see if what follows is more of the same verse or a new verse 
	#Return codes:
	# 0 - not going with new verse, 
	# 1 - going with new verse, 
	# 2 - going with a new verse, is a major section title which then transitions to a normal one 
	my ($code,$dref,$posref)=@_;
	my $ofs=1;# [0] will be the content of a section, but needs testing for paragraph.
	my $returncode=1; 
	if ($isparag{$code}) {
		$ofs=0;
	}
	if ($majorheading{$code}) {
		print DBG "Major heading\n" if (defined($debug));
	}
	while ($ofs<=$#${dref}) { 
		my $ctxt=$$dref[$ofs++];
		print DBG "context is $ctxt\n" if (defined($debug));
		if ($ctxt !~ /^\s*$/ and $ctxt !~/^\s*\\/) {
			# Text here. Mid-verse section
			$$posref[$fragment]++;
			return(0);
		} elsif ($ctxt =~/^\\([cv])$/) {
			# Section that goes with whatever follows.
			my $tmpcode=$1;
			my $tmpidx=$active{$tmpcode};
			my ($val)= ($$dref[$ofs++]=~m/^\s*(\d+)\D/);
			$val=sprintf("%03d",$val);
			updpos($tmpidx,$val,$posref);
			return($returncode);
		} elsif ($ctxt =~/^\s*\\(\S+)/) {
			my $tmpcode=$1;
			if ($isheading{$tmpcode}) {
				$ofs++; # Skip heading text
				if ($majorheading{$code} and !$majorheading{$tmpcode}) {
					$returncode=2;
					print DBG "- found drop to normal heading\n" if (defined($debug));
				}
			} elsif (!$isparag{$tmpcode}) {
				# some non-paragraph code, probably just markup
				$$posref[$fragment]++;
				return(0);
			}
		}
	}
}

sub ref_to_pos { # Create a unique position identifier from a reference
	my ($ref)=@_;
	my @range;
	foreach my $idx (0..$maxactive) {
		$range[$idx]='';
	}
	if ($ref =~ /(\d+):(\d+)/) {
		$range[1]=sprintf("%03d",$1);
		$range[2]=sprintf("%03d",$2);
		$ref=join('::',@range);
	} else {
		printf STDERR ("Could not decode reference '%s'\n",$ref);
		exit(2);
	}
	return($ref);
}
my %inrange_cache;

sub inrange {
	my ($ref)=@_;
	if (!defined($inrange_cache{$ref})) {
		$inrange_cache{$ref}=_inrange($ref);
	}
	logit(undef,"Inrange?",$ref,':',$inrange_cache{$ref});
	return($inrange_cache{$ref});
}
sub _inrange { # Because we may only want a selection of the input files.
	my ($ref)=@_;
	if ($#ranges==-1) {
		return 1;
	}
	#print ("Inrange: $ref\n");
	foreach my $range (@ranges) {
		my ($startref,$stopref)=split("-",$range,2);
		if (!defined($startref) or $startref eq "") {
			$startref="0:0";
		} 
		if (!defined($stopref) or $stopref eq "") {
			$stopref="999:999";
		} 
		my $start=ref_to_pos($startref);
		my $stop=ref_to_pos($stopref);
		if ($ref ge $start) {
			if ($ref le $stop) {
				return 1;
			}
		}
		my (@startpos,@curpos);
		@startpos=split('::',$start);
		@curpos=split('::',$ref);
		if ($startpos[1] eq $curpos[1] and $curpos[2] eq $startpos[2] ) {
			return 1;
		}
	}
#	if ($curpos[1] eq '000' and $curpos[2] eq '000') {
#		return 1;
#	}
	#logit(undef,$ref,"Out of range");
	return 0;
}

my $notext;
my %chunksc; # full vs empty chunk count
sub do_output {
	my ($pos,$chunkref)=@_;
	logit(undef,"Output of $pos");
	map {
		if ($_=~/^(?:\\p\b|\\m\b|\n|\s)+$/) {
			$_='';
		};
	} @$chunkref;
	if (($maxcols+1)==grep {$$chunkref[0] eq ""} (0..$maxcols) ) {
		printf DBG ("skipping output at $pos since it's boring\n") if (defined($debug));
		printf LOG ("skipping output at $pos since it's boring\n") if (defined($logfile));
		return(0);
	}
	foreach my $oside (0..$maxcols) {
		#logit($oside,"chunk:",$$chunkref[$oside]);
		if (($$chunkref[$oside]//"") ne "") {
			if (defined($notext)) {
				if ($notext == $oside) {
					# NB there is presently some magic with \p that it enables diglot switching to work. \par doesn't do it, nor does an empty line
					printf STDOUT ("Problem: \\no%stext followed by \\%stext?",$sides[$notext],$sides[$oside]) ;
					printf OUT "\n\\polyglotcolumn %s\n%s",$sides[$oside],$$chunkref[$oside];
					$chunksc{$sides[$oside]}++;
				}  else {
					printf OUT "\n%s",$$chunkref[$oside];
					$chunksc{$sides[$oside]}++;
				}
			} else {
				printf OUT "\\p\n\\polyglotcolumn %s\n%s",$sides[$oside],$$chunkref[$oside];
				$chunksc{$sides[$oside]}++;
			}
			$notext=undef;
		}
	}
	print OUT "\\polyglotendcols\n";
	foreach my $s (0..$maxcols) {
		$$chunkref[$s]="";
	}
	#print OUT "----------------------------------"."\n";
}

my %modes = ( # options and their help-file description
   v => 'matching verses',
   c => 'matching chapters',
   p => 'matching paragraph breaks',
   );

my $mode='p';
my $priority_side=0;
my $separatesections=0;
my $clsections=0;
my $sectionstack;
my $outfile="-";
my $usage="\nUsage: $0 [-mode|options]  File1 File2 File3\n"
	. "Read LeftFile and RightFile, merging them according to the selected mode)\n " 
	. "Mode may be any ONE of :\n " 
	. join("\n ",map {'-'.$_." \t:".$modes{$_}.(($_ eq $mode)?" (default)":"") } (keys %modes)) . "\n"
	. "Options are:\n "
	. "-L file\t: Log to file\n"
	. "-R 11:25-25:12\t Only ouput specified range\n"
	. "-s \tSplit off section headings into a separate chunk (makes verses line up)\n"
	. "-C \tIf \\cl is used, consider the chapter mark to be a heading\n"
	. "-S 60,45,45,10\t Use an uneven scoring for each file. A potential break-point becomes a real (forced) break-point if the total score is 100 or ore. This example will force a break any time the first column has a break that coincides with one in the second or third column, or if any three columns agree.columns.\n"
	. "-o file\t: Output to file\n";
###########################
# Option parsing
###########################
while ($#ARGV>=0 and $ARGV[0]=~/^-(.)(.*)/) {
	shift;
	my ($Flag,$Rest)=($1,$2);
	my $done=0;
	do {
		if (defined($modes{$Flag})) {
			$mode=$Flag;
			#print ("Mode set to $mode\n");
		} elsif ($Flag eq 'o') {
			if ($Rest ne "") {
				$outfile=$Rest;
			} else {
				$outfile=shift;
			}
		} elsif ($Flag eq 'L') {
			if ($Rest ne "") {
				$logfile=$Rest;
			} else {
				$logfile=shift;
			}
		} elsif ($Flag eq 'C') {
			$clsections=1;
		} elsif ($Flag eq 's') {
			$separatesections=1;
		} elsif ($Flag eq 'R') {
			my $range;
			if ($Rest ne "") {
				$range=$Rest;
			} else {
				$range=shift;
			}
			push @ranges,$range;
		} elsif ($Flag eq 'S') {
			if ($Rest ne "") {
				@scores=split(/,\s*/,$Rest);
			} else {
				@scores=split(/,\s*/,shift);
			}
		} elsif ($Flag eq '-') {
			$done=1;
		} else {
			print "'$Flag' unknown\n";
			print $usage;
			exit(1);
		}
		($Flag,$Rest)=split("",$Rest,2);
		$Rest="" if (undef($Rest));
	} while (!$done and defined($Flag) and $Flag ne "");
}

if ($#ARGV<1) {
	print "Need some input files! (". ($#ARGV+1) ." supplied)\n$usage";
	exit(1);
}

# Read the input files
if (defined($logfile)) {
	print STDERR ("Openning log file $logfile\n");
	open(LOG,'>',$logfile) || die($!);
	$logging=1;
} 

if (defined($debug)) {
	print STDERR ("Openning debug file $debug\n");
	open(DBG,'>',$debug) || die($!);
} 

if ($outfile eq '-') {
	open(OUT,'>& STDOUT');
} else {
	open(OUT,'>',$outfile);
}

my @data;
my @chunks;



###########################
# Applying options
###########################
my $side=0;
my $otherside=1;
my @required=(); # A list of regexps that must ALL be true to allow  a break
# These 'active' numbers define if the sfm is active and where code goes in the position register
if ($mode=~/[cvplr]/) {
	$active{'c'}=1; 
	$active{'v'}=0;
	push @required,'\d+::\d*(?:[1-9][0-9]|[02-9]:|1:.*H)' # Prevent breaking at (before) verse 1
}
if ($mode=~/[vplr]/) {
	$active{'v'}=2;
}
if ($clsections) {
	$active{'cl'}=-1;
}
my @paragraphmarks = qw/p q m q1 q2 q3 pm pm1 pm2 li/;
map {$isparag{$_}=1} @paragraphmarks;

if ($mode=~/[plr]/) {
	map {$active{$_}=$activepar} @paragraphmarks;
	# breaking is permitted either at a section, a paragraph or at a new chapter
	push @required, '(?:P|H|^::\d+::000::)'; 
}


{
	my @inactivesections=qw/mt mt2/; # Sections that don't count as active but should be noticed...
	my @majorheadings=qw/ms mr/;#  active major sections (in order of decreasing importance)
	my @sectionheadings = qw/s s2 s3/; #  active sections (in order of decreasing importance)
	my $n=0;
	foreach my $s (@inactivesections) {
		makeheading($s,$n,-1,1);
		++$n;
	}
	foreach my $s (@majorheadings) {
		makeheading($s,$n,$activeheading,1);
		++$n;
	}
	foreach my $s (@sectionheadings) {
		makeheading($s,$n,$activeheading,0);
		++$n;
	}
}

my $defaultscore=(101/($#ARGV+1));
foreach my $nr (0..$#ARGV) {
	my $file=$ARGV[$nr];
	push @data,[readfile($file)];
	$position[$nr]=$startposition;
	$chunk[$nr]='';
	$chunks[$nr]=['start',''];
	$inrange[$nr]=1;
	$partype[$nr]='';
	$maxcols=$nr;
	if($nr>$#sides){
		$sides[$nr]=$sides[$nr-1];
		$sides[$nr]++
	}
	if(!$scores[$nr]) {
		$scores[$nr]=$defaultscore;
	}
}

if ($mode eq 'r') {
  $priority_side=1; # default value is 0 (left)
}

logit(undef,sprintf("Configuration status is:\n  Section headers:%s\n  active SFM codes:%s\n",($separatesections?"special block":"combined with following"),join(", ",map {$_."(".$active{$_}.")"} sort keys %active)));
my @hold=("",""); # interpreted things we don't want to output yet.

my @chapter;
my (%breakafter,%breakbefore);

sub sideswitch {
	$side++;
	$side%=($maxcols+1);
}
#
# apply range limits and index data
#
$side=0;
while( 0<scalar( grep {$#{$data[$_]}>=0} (0..$maxcols ) )) {
	while ($#{$data[$side]}==-1) {
		logit($side,"End of File");
		sideswitch();
	}
	my $score=$scores[$side];
	my $cl=shift(@{$data[$side]});
	print DBG ($side,':',$cl) if (defined($debug));
	my $what;
	if ($cl =~ m/^\s*\\(\S+)/) {
		my $code=$1;
		if (!defined($code)) {
			die("problem interpreting data $cl\n");
		}
		my ($oldpos,$newpos,$earlyreclaim);
		if (defined($active{$code})) {
			print STDERR "+";
			my $idx=$active{$code};
			my @pos=split('::',$position[$side],-$maxactive);
			logit($side,'Interpreting code',$code);
			if ($code =~ /^cl$/) { # only get here if cl set to active.
				if ($pos[1] eq '000' || $position[2] gt '000') {
					logit($side,'Usingcl');
					$usingcl[$side]=1;
				} else {
					$idx=$active{'s'}; # Treat it as a section title
					$code='s'; 
				}
			}
			if ($code =~ /^[cv]$/) {
				($what)= (${$data[$side]}[0]=~m/^\s*(\S+)/);
				if (!defined($what)) {
					print("Unrecognised chapter or verse in ".${$data[$side]}[0] );
				}
				if ($what=~/(\d+[a-z]?)-(\d+[a-z]?)/) { # a range.. hmm 
					$what=$1;
				}
				$what=sprintf("%03d",$what);
			} elsif ($isparag{$code}) {
				$partype[$side]=$cl; # Remember this in case we resume later.
				#see if this paragraph is followed by text or section/verse 
				if (isnewverse($code,$data[$side],\@pos)) {
					$what='P'; # verse-end (probably) break-point.
				} else {
					$what='p'; # middle of verse.
				}
			} elsif ($isheading{$code}) {
				# Need to read ahead to find out what this is.
				my $test=isnewverse($code,$data[$side],\@pos);
				# Do we consider reclaimed headings as part of this heading?
				# If so, set earlyreclaim=0; 
				if ($majorheading{$code}) {
					$earlyreclaim=0;
				} else {
					$earlyreclaim=2;# reclaimed headings are probably major...
				}
				if ($test==1) { # normal heading preceding verse
					$what='H';
				} elsif ($test==2) { # this is a major heading preceding a normal heading
					$what='HH';
					$earlyreclaim=0;
				} else { # mid-verse heading
					$what='h';
				}
				my $l=$isheading{$code};
				my $ctxt=$data[$side][0];
				$headingstack[$side][$l]=$cl.$ctxt; # remember the heading
				print LOG ($code,$l,$ctxt) if (defined($logfile));
				splice(@{$headingstack[$side]},$l,9,$cl.$ctxt); # chop off the tail of the array;
				logit($side,"headingstack($side) now: ".join(', ', map {$_//''} @{$headingstack[$side]}));
				if (!$inrange[$side]) {
					$cl='';
					shift @{$data[$side]};
				}
			} else {
				$what=$code;
			}
			if ($idx>=0) { # idx is short hand for active{code}
				# Put chapter mark and whatever non-active stuff follows it to one side.
				if (${$data[$side]}[0] =~ /^\s*\d+\s+\\nb/) {
					logit($side,'\\nb found after \\c Not breaking');
					updpos($idx,$what,\@pos);
					$what='N'; # alter things so update that follows to mark the par as nobreakable
					$idx=$activepar;
				} else {
					if ($code eq 'c') {
						if (${$data[$side]}[1]!~/^\\cl/) {
							$chapter[$side]=$cl . shift @{$data[$side]};
							$cl='';
						} else {
							$chapter[$side]=$cl . join("",splice @{$data[$side]},0,3);
							$cl='';
							logit($side,"storing chapter and cl",$chapter[$side]);
							if ($clsections) {
								$clsections++;
							}
						}
					}
				}
				if (!defined($what)) {
					die("EH?");
				}
				#logit(undef,$idx,$what);
				# Incrementing chapter empties verses, and so on.
				updpos($idx,$what,\@pos);
				$oldpos=$position[$side];
				$newpos=join('::',@pos);
				$position[$side]=$newpos;
				logit($side,"Idx: ".$#{$chunks[$side]});
				my $inr=inrange($newpos);
				my $wasinr=$inrange[$side];
				if ($wasinr and !$inr) {
					logit($side,"Gone out of range - remembering the headingstack.");
					@{$oldhead[$side]}=(@{$headingstack[$side]});
				}
				# Reclaim chapter marking and headers
				if ($inr and !$wasinr ) {
					my ($cur,$old)=($headingstack[$side],$oldhead[$side]);
					my $reclaim='';
					my (@tmppos)=(@pos);
					# We declare the headingstack to be at current position but with 'H' as the section code, just like real major section headers.
					if ($tmppos[$activeheading] eq '_') {
						$tmppos[$activeheading]='H';
					}
					my $chk=$#{$cur};
					if ($earlyreclaim==2) {
						$tmppos[$activeheading]='HH';
						$chk--;
						#early reclaim==2 means output the previous stack, not this value
					}
					my $sectpos=join('::',@tmppos);
					logit($side,"Gone into range - using the headingstack:");
					for my $n (1..$chk) { # stacklevel n=0 is empty, so isheading returns a non-zero integer
						if (defined($$cur[$n])) {
							if ($$cur[$n] ne ($$old[$n]//"")) {
								print LOG "$n - $$cur[$n] changed\n" if (defined($logfile));
								$reclaim.=$$cur[$n];
							} else {
								print LOG "$n - $$cur[$n] not changed\n" if (defined($logfile));
							}
						}
					}
					print LOG "$reclaim";

					if($earlyreclaim) {
						push @{$chunks[$side]},$sectpos,$reclaim; # straight to output chunk
						$reclaim='';
						if($earlyreclaim ==2) {
							$cl=$$cur[$#{$cur}].$cl;
						} 
					} else {
						$cl=$reclaim.$cl;
					}
					@{$oldhead[$side]}=(@{$headingstack[$side]});
				}
				if ($clsections==2) {
					my (@tmppos)=(@pos);
					updpos($activeheading,'HH',\@pos); 
					my $sectpos=join('::',@pos);
					logit($side,"new position:",$sectpos);
					
					push @{$chunks[$side]},$sectpos,$chapter[$side]; # straight to output chunk
					logit($side,"writing chunk for chapter, cl:",$chapter[$side]);
					if (defined($chunkscore{$sectpos})) {
						$chunkscore{$sectpos}+=$score;
					} else  {
						$chunkscore{$sectpos}=$score;
					}
					$chapter[$side]=undef;
					$clsections=1;
				}
				if ($code eq 'v' and defined($chapter[$side]) and $inr) {
					$cl=$chapter[$side].$partype[$side]."\n".$cl;
					$chapter[$side]=undef;
				}
				if ($oldpos ne $newpos) {
					if ($inr) {
						printf DBG ("$oldpos -> $newpos\n");
						unless(!$wasinr) { # Surely the start of a cut-point ought to always be an acceptable break-point?
							foreach my $search (@required) {
								if ($newpos !~/$search/) {
									$score=0;
								}
							}
						}
						if ($score>0) {
							$chunkcounts{$newpos}+=1;
						}
						if (defined($chunkscore{$newpos})) {
							$chunkscore{$newpos}+=$score;
							if($chunkcounts{$newpos}>$maxcols) {
								$chunkscore{$newpos}+=100; #All columns agree.
							}
						} else {
							$chunkscore{$newpos}=$score;
							$chunkcounts{$newpos}=1;
						}
						my $idx=$#{$chunks[$side]};
						logit($side,"New chunk started",$idx-1, $newpos);
						 if ($idx>0) {
							logit($side,"Previous chunk:",${$chunks[$side]}[$idx]);
						}
						my $par='';
						if ($oldpos=~/::P::/ and $partype[$side] ne '\\p') {
							$par=$partype[$side];
						}
						push @{$chunks[$side]},$position[$side],$par.$cl if ($inr and $cl ne "");
					}
					$inrange[$side]=$inr;
					next;
				}
			}
		} else {
			print STDERR ".";
		}
	}
	my $idx=$#{$chunks[$side]};
	${$chunks[$side]}[$idx].=$cl if ($inrange[$side]);
}

print DBG ("\nScore rules:".join(',',@scores)) if (defined($debug));
print DBG ("\nKey results:\n") if (defined($debug));
my @chunklist;
my @tmp=sort {$a cmp $b}  keys %chunkscore;
foreach my $n (0 .. $#tmp) {
	my $key =$tmp[$n] ;
	if ($key=~/::H+::/) {
		if ($chunkscore{$tmp[$n+1]}>99) {
			$chunkscore{$key}+=100; # Bring break before heading.
			if (!$separatesections) {
				$chunkscore{$tmp[$n+1]}=0; # and suppress post-heading break.
			}
		}
		print STDERR ("H");
	} else {
		print STDERR ("@");
	}
	print DBG ($key,' : '. $chunkscore{$key},"\n") if (defined($debug));
	if ($chunkscore{$key}>99) {
		push @chunklist,$key;
	}
}



foreach my $side (0..$maxcols) {
	$data[$side]=0;
}
foreach my $chunk (@chunklist,"999::999::999::") {
	my @combined;
	foreach my $side (0..$maxcols) {
		$combined[$side]='';
	}
	foreach my $side (0..$maxcols) {
		do {
			$data[$side]++;
			$combined[$side].=${$chunks[$side]}[$data[$side]];
			$data[$side]++;
		} while ($data[$side]<=$#{$chunks[$side]} and (${$chunks[$side]}[$data[$side]] lt  $chunk));
	}
	$,=', ';
	print DBG $chunk,@data,$chunks[$side][$data[$side]],"\n" if (defined($debug));
	do_output($position[$side],\@combined);
}
	
exit(0);
