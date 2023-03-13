#!/usr/bin/perl -w
use strict;
use File::Basename;
use File::Spec;

my @modes=qw/doc simple/;
if ($#ARGV<0) {
  print STDERR "usage $0 [-m mode [-m mode]] dir\n dir specifies the output directory for merged files\n";
  exit(1);
}
while ($ARGV[0]=~/-m(.*)/) {
  shift;
  push @modes,$1||shift;
}
my $outdir=$ARGV[0];
if (! -d $outdir) {
  mkdir($outdir) || die($outdir.':'.$!);
}
my $exedir=dirname(__FILE__);
my $rootdir= File::Spec->catfile(File::Spec->updir(File::Spec->updir($exedir)),'test','projects');
my @source=qw/OGNT WEBorig WSG WSGdev WSGBTpub/;
my @entries;
my @counts;

foreach my $source (@source) {
  my $dir;
  $dir=File::Spec->catfile($rootdir,$source);
  print $dir."\n";
  my $DIR;	
  opendir($DIR,$dir);
  foreach my $entry (readdir($DIR)) {
    next if ($entry !~ /U?SFM$/i);
    print $entry;
    my $id=substr($entry,0,2);
    print $id;
    if ($id =~/[0-9][0-9]/ and $id <=70) {
      if (defined($counts[$id])) {
	$counts[$id]++;
	push @{$entries[$id]},[$source, File::Spec->catfile($dir,$entry)];
      } else {
	$counts[$id]=1;
	$entries[$id]=[[$source, File::Spec->catfile($dir,$entry)]];
      }
    }
  }
}

foreach my $k (grep {defined($counts[$_]) && $counts[$_]>1} (1..$#counts)) {
  my $n=$counts[$k]-1;
  print($k.":".$n."\n");
  while($n>0) {
    my $m=$n-1;
    while ($m>=0) {
      my $o=$entries[$k][$m][0]."+".$entries[$k][$n][0]."_".$k;
      print ("$m,$n:$o\n");
      foreach my $mode (@modes){	
	system(File::Spec->catfile($exedir,"usfmerge"),"-o",File::Spec->catfile($outdir,$o."-$mode.usfm"),"-m",$mode,$entries[$k][$m][1],$entries[$k][$n][1]);
      }
      --$m;
    }
    --$n;
  }
}
