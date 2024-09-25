#!/usr/bin/perl

# Generate TSV of:
#	order    title    type    index    file01.htm [filenn.htm ...]
#
# Where
#   order: '0' padded book order number from 01 to 81
#          Old Testament + Apocrypha + New Testament
#   title: Book Title 
#   type:  'oo' Old Testaments
#          'aa' Apocrypha
#          'nn' New Testament
#   index: HTML source containing chapter index
#   file:  HTML sources for each book chapter

use strict;
use warnings;

# return array of book chapter file names given book index file name
sub book_chapter_list {
	my $book_idx_fname = shift;
	my @book_chapters;
	my $fname = "bibles/WEB/$book_idx_fname";

	open my $fp, $fname or die "failed to open $fname $!";

	while (my $ln = <$fp>) {
		chomp $ln;
		my ($ch_file) =
			$ln =~ /<li><a href='(.*\.htm)'>[^<]*<\/a><\/li>/ or next;
		push(@book_chapters, $ch_file);
	}

	return @book_chapters;
}

my %types = (
	'oo' => 1,
	'aa' => 1,
	'nn' => 1
);

# starting index contains books and types
my $fname = 'bibles/WEB/index.htm';
my $order = 0;

open my $fp, $fname or die "failed to open $fname $!";

while (my $ln = <$fp>) {
	chomp $ln;
	my ($type, $book_idx_fname, $title) =
		$ln =~ /<li><a class='(.*)' href='([0-9]?[A-Z]+)[0-9]{2,3}.htm'>(.*)<\/a><\/li>/ or next;
	exists $types{$type} or next;
	# workaround Apocryphal Psalm 151 that breaks our regex
	$book_idx_fname = $book_idx_fname eq "PS"
		? "PS2.htm" : $book_idx_fname.".htm";
	my @chapter_files = book_chapter_list($book_idx_fname);
	printf( "%02s\t%s\t%s\t%s\t%s\n",
		++$order, $type, $title, $book_idx_fname, join(' ', @chapter_files) );
}
