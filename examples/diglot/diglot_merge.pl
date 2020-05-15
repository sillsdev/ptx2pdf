#!/usr/bin/perl -w
# This file is copyright (c) SIL 2006-2020
# It is provided as-is, with no express or implied guarantee that it will do anything.
# It is in extended beta test, please check its output carefully.
#
# You may use it and distribute it under terms of the Perl Artistic Licence 2.0:
# https://www.perlfoundation.org/artistic-license-20.html
#
use strict;
my $logging=0;
my (@leftdata, @rightdata);
my (@chunkline,@chunkdata,@pos);
my %active; # all active tokens;
my $activeheading=4;  # level to set active{heading} to
my $activepar=4;  # level to set the active{par} to
my $maxactive=5;
my $fragment=3; # level to set the verse fragment to
my $savelimit=0;
my @usingcl=(0,0);
my %isparag; # are these tokens paragraph marks
my %isheading; # level of section (needed if we're skipping stuff)
my %majorheading; # are these tokens major sections 
my %keep_with_chapter;
my @ranges=();
my @sides=('left','right');
my @chunk=("","");
my @position=('::000::000::000:::::','::000::000::000:::::');
my @numeric=(0,1,1,1,0,0,0,0); # which positions have numbers
my @inrange=(1,1);
my @partype=('','');
my @heading;
my @headingstack=(['','','',''],['','','']);
my @oldhead=(['','','',''],['','','']);
my @first_inrange; # Shortcut to the start of interesing data
my $debug=undef; # ".diglot.dbg";
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
	if ($firstline=~/\\c\s*0\s*$/) {
		logit(undef,"Swallowing first line $firstline");
		$firstline='';
	} else {
		logit(undef,"First line $firstline");
	}
	my $re='(\\\\(?:'.join("|",keys(%active)).")\\b)";
	@result=map {s/\r\n/\n/g;s/\x{FEFF}//;$_} map {split(/$re/)} ($firstline,<FILE>);
	close(FILE);
	#foreach my $l (0..$#result) {
		#printf DBG ("%06d: %s\n",$l,$result[$l]);
	#}
	logit(undef,"Closed $name");
	return @result;
}

sub logit { # Gerneral purpose logging routine
	my ($side)=shift(@_);
	if ($logging) {
		if (defined($side)) {
			print LOG (join(" ",$sides[$side],$position[$side],@_)."\n");
			print DBG (join(" ",$sides[$side],$position[$side],@_)."\n") if (defined($debug));
		} else {
			
			print LOG (join(" ",@_)."\n");
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
			my ($val)= ($$dref[$ofs++]=~m/^\s*(\S+)/);
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
my %chunksc;
sub do_output {
	my ($pos,$chunkref)=@_;
	logit(undef,"Output of $pos");
	map {
		if ($_=~/^(?:\\p\b|\\m\b|\n|\s)+$/) {
			$_='';
		};
	} @$chunkref;
	if ($$chunkref[0] eq "" and $$chunkref[1] eq "") {
		printf DBG ("skipping output at $pos since it's boring\n") if (defined($debug));
		printf LOG ("skipping output at $pos since it's boring\n");
		return(0);
	}
	foreach my $oside (0,1) {
		my $otherside=1-$oside;
		#logit($oside,"chunk:",$$chunkref[$oside]);
		if (($$chunkref[$oside]//"") ne "") {
			if (defined($notext)) {
				if ($notext == $oside) {
					# NB there is presently some magic with \p that it enables diglot switching to work. \par doesn't do it, nor does an empty line
					printf STDOUT ("Problem: \\no%stext followed by \\%stext?",$sides[$notext],$sides[$oside]) ;
					printf OUT "\\p\n\\%stext\n%s",$sides[$oside],$$chunkref[$oside];
					$chunksc{$sides[$oside]}++;
				}  else {
					printf OUT "\n%s",$$chunkref[$oside];
					$chunksc{$sides[$oside]}++;
				}
			} else {
				printf OUT "\\p\n\\%stext\n%s",$sides[$oside],$$chunkref[$oside];
				$chunksc{$sides[$oside]}++;
			}
			$notext=undef;
		} else {
			printf OUT "\\p\\no%stext\n",$sides[$oside];
			$notext=$oside;
			my $little=substr($$chunkref[$otherside],0,10);
			logit(undef,$sides[$otherside].' starts "'.$little.'"');
			if (${$chunkref}[$otherside] =~ /\\s/) {
				$chunksc{'no'.$sides[$oside]."_s"}++;
			} else {
				$chunksc{'no'.$sides[$oside]}++;
			}
		}
	}
	$$chunkref[0]="";
	$$chunkref[1]="";
	#print OUT "----------------------------------"."\n";
}

my %modes = ( # options and their help-file description
   l => 'Left master: splitting right page at each left text paragraph',
   r => 'Right master: splitting left page at each right text paragraph',
   v => 'matching verses',
   c => 'matching chapters',
   p => 'matching paragraph breaks',
   );

my $mode='v';
my $priority_side=0;
my $separatesections=0;
my $clsections=0;
my $sectionstack;
my $logfile=undef;
my $outfile="-";
my $usage="\nUsage: $0 [-mode|options] LeftFile RightFile\n"
	. "Read LeftFile and RightFile, merging them according to the selected mode)\n " 
	. "Mode may be any ONE of :\n " 
	. join("\n ",map {'-'.$_." \t:".$modes{$_}.(($_ eq $mode)?" (default)":"") } (keys %modes)) . "\n"
	. "Options are:\n "
	. "-L file\t: Log to file\n"
	. "-R 11:25-25:12\t Only ouput specified range\n"
	. "-s \tSplit off section headings into a separate chunk (makes verses line up)\n"
	. "-C \tIf \cl is used, consider the chapter mark to be a heading\n"
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
		} else {
			print "$Flag unknown\n";
			print $usage;
			exit(1);
		}
		($Flag,$Rest)=split("",$Rest,2);
		$Rest="" if (undef($Rest));
	} while (!$done and defined($Flag) and $Flag ne "");
}

if ($#ARGV!=1) {
	print $usage;
	exit(1);
}

my ($leftfile,$rightfile)=@ARGV;


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

###########################
# Applying options
###########################
my $side=0;
my $otherside=1;
my @data=(\@leftdata,\@rightdata);
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
		$isheading{$s}=$n+1; # >=1 so we can test it...
		$active{$s}=-1; # 
		$majorheading{$s}=1;
		if ($s =~ s/2$/1/) { # if there's a X2 then make X1 equivalent to the previous level
			$isheading{$s}=$n;
			$active{$s}=-1; # 
		}
		++$n;
	}
	foreach my $s (@majorheadings) {
		$isheading{$s}=$n+1;
		$active{$s}=$activeheading;
		$majorheading{$s}=1;
		if ($s =~ s/2$/1/) { # if there's a X2 then make X1 equivalent to the previous level
			$isheading{$s}=$n;
			$active{$s}=$activeheading; # 
		}
		++$n;
	}
	foreach my $s (@sectionheadings) {
		$isheading{$s}=$n+1;
		$active{$s}=$activeheading;
		if ($s =~ s/2$/1/) { # if there's a X2 then make X1 equivalent to the previous level
			$isheading{$s}=$n;
			$active{$s}=$activeheading; # 
		}
		++$n;
	}
}


if ($mode eq 'r') {
  $priority_side=1; # default value is 0 (left)
}

logit(undef,sprintf("Configuration status is:\n  Section headers:%s\n  active SFM codes:%s\n",($separatesections?"special block":"combined with following"),join(", ",map {$_."(".$active{$_}.")"} sort keys %active)));
my @hold=("",""); # interpreted things we don't want to output yet.

my @chapter;
my (%breakafter,%breakbefore);
my @chunks=(['start',''],['start','']); 

# Read the input
@leftdata=readfile($leftfile);
@rightdata=readfile($rightfile);
#
# Classify chunks of data
#
while($#leftdata>=0 or $#rightdata>=0) {
	if ($#{$data[$side]}==-1) {
		logit($side,"End of File");
		$otherside=$side;
		$side++;
		$side%=2;
	}
	my $cl=shift(@{$data[$side]});
	my $what;
	if ($cl =~ m/^\\(\S+)/) {
		my $code=$1;
		if (!defined($code)) {
			die("problem interpreting data $cl\n");
		}
		my ($oldpos,$newpos,$earlyreclaim);
		if (defined($active{$code})) {
			$earlyreclaim=1;
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
				print LOG ($code,$l,$ctxt);
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
				my $ok=1; # is a break here OK?
				# Put chapter mark and whatever non-active stuff follows it to one side.
				if (${$data[$side]}[0] =~ /^\s*\d+\s+\\nb/) {
					$ok=0; # don't break here
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
							$ok=2;
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
								print LOG "$n - $$cur[$n] changed\n";
								$reclaim.=$$cur[$n];
							} else {
								print LOG "$n - $$cur[$n] not changed\n";
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
					logit($side,"new position:",join('::',@pos));
					push @{$chunks[$side]},$sectpos,$chapter[$side]; # straight to output chunk
					logit($side,"writing chunk for chapter, cl:",$chapter[$side]);
					$chapter[$side]=undef;
					$clsections=1;
				}
				if ($code eq 'v' and defined($chapter[$side]) and $inr) {
					$cl=$chapter[$side].$partype[$side]."\n".$cl;
					$chapter[$side]=undef;
				}
				if ($oldpos ne $newpos) {
					# Check for oldpos being a break point, so
					# the new chunk starts after a break.

					foreach my $search (@required) {
						if ($oldpos !~ /$search/ and $newpos !~/$search/) {
							if ($inr and !$wasinr) {
								logit($side,$search,"not found but overriding");
							} else {
								$ok=0;
								logit($side,$search,"not found in",$newpos ,"or", $oldpos);
							}
						}
					}
					# special case: don't want to split off the
					# final \p from a section, or bad things
					# happen.
						
					if ($breakbefore{$newpos.$side}) {
						logit($side,"breakbefore $newpos.$side was set");
						$ok=1;
					}
					if (($oldpos =~ /::H/) and $newpos =~ /::P::/) {
						logit($side,"$oldpos was section. not splitting.");
						$ok=0;
					}
					if ($oldpos =~ /::N::/) {
						$ok=0;
						logit($side,"after NB, must not break");
					}
					if ($breakafter{$oldpos.$side}) {
						logit($side,"breakafter $oldpos.$side was set");
						$ok=1;
					}
					#if ($pos[1] gt '000' and !$first_inrange[$side] and $inr) {
					#	logit($side,"First inrange verse");
					#	my $ofs=+1;
					#	if (!$ok) {
					#		$ofs=-1;
					#	}
					#	$first_inrange[$side]=$#{$chunks[$side]}+$ofs;
					#}
					$inrange[$side]=$inr;
					if ($ok) { 
						my $idx=$#{$chunks[$side]};

						logit($side,"New chunk started",$idx-1, $newpos);
						 if ($idx>0) {
							logit($side,"Previous chunk:",${$chunks[$side]}[$idx]);
						}

						my $par='';
						if ($oldpos=~/::P::/ and $partype[$side] ne '\\p') {
							$par=$partype[$side];
						}
						push @{$chunks[$side]},$position[$side],$par.$cl if $inr;
						if (($side==0 and $mode eq 'l') or ($side==1 and $mode eq 'r')) {
							$breakafter{$oldpos.$otherside}=1;
							$breakbefore{$newpos.$otherside}=1;
							logit($side,"Setting breakafter $oldpos$otherside");
						}
						next;
					}
				}
			}
		} 
	}
	my $idx=$#{$chunks[$side]};
	${$chunks[$side]}[$idx].=$cl if ($inrange[$side]);
	logit($side,'swap?');
	if ($side==$priority_side and $#{$data[$side]}>=0) {
		next; # what happens if we read all the priority side
	}
	# Make sure that we read priority_side first by switching away less soon
	if ($side==$priority_side) { 
		if ($position[$otherside] lt $position[$side]) {
			if ($#{$data[$otherside]} >=0 ) {
				$otherside=$side;
				$side++;
				$side%=2;
			}
		}
	} else {
		if ($position[$otherside] le $position[$side]) {
			if ($#{$data[$otherside]} >=0 ) {
				$otherside=$side;
				$side++;
				$side%=2;
			}
		}
	}
}

my $ok=1;
my @combined=("","");
@position=('start','start');
my @prevposition=('','');
my @nextposition=('','');
#
#Always include the file header, which is always chunks[][1]
#
foreach my $side (0,1) {
	$chunk[$side]=${$chunks[$side]}[1];
}

do_output($position[$side],\@chunk);

# print files and chunks to DBG
# don't clean here as chunks may be joined before output
for my $side (0,1) {
	print DBG "$side\n" if (defined($debug));
	print DBG @{$chunks[$side]} if (defined($debug));
}

print DBG ("-----------------\n") if (defined($debug));
# Combine chunks and output them.
# When the chunk references (positions) line up then its time for a new
# grouping. 
#logit(undef,sprintf("First inrange: %s,%s\n",@first_inrange));
my @idx=(2,2);
#logit(undef,sprintf("First index: %s,%s\n",@idx));
# get previous position, in case of it being a heading, along with present and next positions
foreach my $side (0,1) {
	#if ($idx[$side]>=2) {
		#$prevposition[$side]=${$chunks[$side]}[$idx[$side]-2];
		#if ($prevposition[$side]=~/::[Hh]::/) {
			#$heading[$side]=$chunks[$side][$idx[$side]-1];
		#}
	#}
	$position[$side]=${$chunks[$side]}[$idx[$side]];
	$nextposition[$side]=${$chunks[$side]}[$idx[$side]+2];
}
my @maxidx=map {$#{$chunks[$_]}} (0,1);
#
# Main loop for output
#
if ($position[0] ne $position[1]) {
	logit(undef,"Unexpected event: Starting references are not identical\n".$position[0]."!=".$position[1]);
	warn("Unexpected event: Starting references are not identical\n".$position[0]."!=".$position[1]);
}

# OUTER loop: position[1] == position[2]...  keep going while there's data left;
@heading=('','');
OUTER: while ($idx[0]<$maxidx[0] or $idx[1]<$maxidx[1]) {
	logit(undef,"Outer: L".$position[0],"R".$position[1],"Ln".$nextposition[0],"Rn".$nextposition[1]);
	#print ("Idxes:",$idx[0]," ",$idx[1]);
	my $washeading;
	# check if the previous chunk was a section heading
	$washeading=0;
	foreach my $side (0,1) {
		if ($prevposition[$side] =~ /::[hH]+::/) {
			$washeading=1;
		} 
	}

	if ($washeading) {
		logit(undef,"Using heading(s)");
		if ($separatesections) {
			if ($#heading>1) {
				my @h1=splice(@heading,2,2);
				do_output($position[$side]."majorsection",\@h1);
			}
			do_output($position[$side]."section",\@heading);
		} else {
			@combined=@heading;
		}
		@heading=('','');
	}

	my ($side,$otherside)=(2,2);

	#
	#If the loop below won't trigger for this chunk then output both chunks here
	#
	if ($nextposition[0] gt $nextposition[1]) {
		$side=1;
		$otherside=0;
		logit(undef,'Using side',$sides[$side],"since it's behind");
	} elsif ($nextposition[0] lt $nextposition[1]) {
		$side=0;
		$otherside=1;
		logit(undef,'Using side',$sides[$side],"since it's behind");
	} else {
		next OUTER; # current chunks end at the same place, so drop out to output routine.
	}
	
# 
	#middle loop
	MIDDLE:while (($nextposition[$side] ne $nextposition[$otherside]) and ($idx[$side]<$maxidx[$side])) {
		#inner loop
		INNER:while ($nextposition[$side] lt $nextposition[$otherside] and ($idx[$side] < $maxidx[$side])) {
			logit(undef,"Inner : L:".$position[0],"R:".$position[1],"Ln".$nextposition[0],"Rn".$nextposition[1]);
			if ($position[$side] =~/::([Hh]+)::/) {
				my $htype=$1;
				my $ofs=0;
				if ($htype eq 'HH') {
					$ofs=2;
				}
				logit($side,"Adding to heading. $ofs");
				$heading[$side+$ofs].=${$chunks[$side]}[$idx[$side]+1];
				logit($side,"-Ch-".$idx[$side]);
			} else {
				logit($side,"Adding chunk for output");
				if ($#heading>1 and defined($heading[$side+2])) {
					$heading[$side]=$heading[$side+2].$heading[$side];
					$heading[$side+2]='';
				}
				$combined[$side].=$heading[$side].${$chunks[$side]}[$idx[$side]+1];
				print DBG ($sides[$side].$position[$side],$combined[$side]) if (defined($debug));
				logit($side,"-C-".$idx[$side]);
				$heading[$side]="";
			}
			# Increment counters for this side
			$idx[$side]+=2;
			$prevposition[$side]=$position[$side];
			$position[$side]=$nextposition[$side];
			if (($idx[$side]+2)<=$maxidx[$side]) {
				$nextposition[$side]=${$chunks[$side]}[$idx[$side]+2];
				#printf STDERR "Read idx %d=%s\n", $idx[$side]+2,$nextposition[$side];
			} else { 
				$nextposition[$side]='999::999::';
				#printf STDERR "EOD idx %d=%s\n", $idx[$side]+2,$nextposition[$side];
			}
		}
		logit($side,"Swapping sides");
		#printf STDERR ("Swapping sides %s %s\n",$position[0],$position[1]);
		$otherside=$side;
		$side++;
		$side%=2;
	} # End of Middle loop
	logit(undef,"EOM : L:".$position[0],"R:".$position[1],"Ln".$nextposition[0],"Rn".$nextposition[1]);
} continue {
	# 
	if ($nextposition[0] eq $nextposition[1]) {
		foreach my $side (0,1) { 
			if ($position[$side] =~/::([hH]+)::/) {
				my $htype=$1;
				my $ofs=0;
				if ($htype eq 'HH') {
					$ofs=2;
				}
				logit($side,"Adding to heading . $ofs");
				$heading[$side+$ofs].=${$chunks[$side]}[$idx[$side]+1];
				logit($side,"-Ah-".$idx[$side]);
			} else {
				logit($side,"Adding chunk for output");
				if ($#heading>1 and defined($heading[$side+2])) {
					$heading[$side]=$heading[$side+2].$heading[$side];
					$heading[$side+2]='';
				}
				$combined[$side].=$heading[$side].${$chunks[$side]}[$idx[$side]+1];
				print DBG ($sides[$side].$position[$side],$combined[$side]) if (defined($debug));
				logit($side,"-A-".$idx[$side]);
				$heading[$side]="";
			}
			# and now increment the position ;
			$idx[$side]+=2;
			$prevposition[$side]=$position[$side];
			$position[$side]=$nextposition[$side];

			if (($idx[$side]+2)<=$maxidx[$side]) {
				$nextposition[$side]=${$chunks[$side]}[$idx[$side]+2];
				#printf STDERR "%s: Read idx %d=%s\n", $sides[$side], $idx[$side]+2,$nextposition[$side];
			} else {
				logit($side,'Hit end-stop');
				$nextposition[$side]='999::999::';
			}
		}
		logit(undef,"Outputting chunk");
		do_output($prevposition[0],\@combined);
	}
}

do_output($nextposition[0],\@combined);
do_output($nextposition[1],\@combined);

foreach my $ref (keys %chunksc) {
	logit(undef,'END',$ref,$chunksc{$ref});
}

foreach my $lr (@sides) {
	my $nolr='no'.$lr;
	next if (!defined($chunksc{$nolr}));
	if ($chunksc{$nolr} > 0.1*$chunksc{$lr}) {
		printf STDERR ("WARNING: probably corrupt output (%.0f%% of %s chunks are empty)\n", 
			100*$chunksc{$nolr}/($chunksc{$lr}+$chunksc{$nolr}),$lr);
	}
}

