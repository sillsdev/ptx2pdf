#!/usr/bin/perl -w
# This little script answers a request https://community.scripture.software.sil.org/t/cross-references-in-reference-bible/3470/2 "
# * Prepend to the current note a null note with the (annontated) chapter if that is different to the last one. (e.g. \x - \xo Chapter 2\x* \x + \xo 1 \xt ...\*)
# * Only print the verse number if that is different to the last reference.
# * Entirely delete the \xo entry if it is identical to the last one.
#
# It assumes that all xo entries are in the format chapter:verse, and that verses in xref \xo entries are only numeric. 

use strict;
my $chapter='';
my $verse='';

$\=''; # Swallow whole file as one chunk
$/='';
sub beautify {
	my ($c,$v)=@_;
	if ($c ne $chapter) {
		$chapter=$c;
		$verse='';
		print "\\x - \\xo Chapter $c\\x*";
	}
	if ($v ne $verse) {
		$verse=$v;
		"\\xo $v";
	}
}

while(my $file=(<>)) {
	foreach my $chunk (split(/(\\x.*?\\x\*)/, $file)) {
		$chunk=~s/\\xo (\d+):(\d+)/beautify($1,$2)/e;
		print $chunk;
	}
}

