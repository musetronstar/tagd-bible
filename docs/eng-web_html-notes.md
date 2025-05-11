# World English Bible with Deuterocanon Notes

We downloaded files from [World English Bible with Deuterocanon](https://ebible.org/find/show.php?id=eng-web)

## HTML

HTML sources extracted from zip file.
[Zipped mobile HTML](https://ebible.org/Scriptures/eng-web_html.zip)

`WEB-src-indexes.tsv` is a Tab Separated Value (TSV) file
containing no headers.

## Header Columns

```tsv
order    title    type    index    file01.htm [filenn.htm ...]
```

The example `file01.htm` above is the *book file*
followed by `[filenn.html ...]` which is each *chapter file* for that book.

## Column Definitions:

```
    order: '0' padded book order number from 01 to 81
           Old Testament + Apocrypha + New Testament
    title: Book Title 
    type:  'oo' Old Testaments
           'aa' Apocrypha
           'nn' New Testament
    index: HTML source containing chapter index
    file:  HTML sources for each book chapter
```

## TAGL Files

Create `tagl/{01..n}-<WEB_book_title>`.tagl for each book.

  Examples:
```
01-Genesis.tagl
...
14-2_Chronicles.tagl
...
47-1_Maccabees.tagl
...
66-Colossians.tagl
...
81-Revelation.tagl
```

Note that due to the inclusion of the Deuterocanon/Apocrypha, Revelation is not book 66.
