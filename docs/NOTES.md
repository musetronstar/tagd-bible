# NOTES
Notes for work todo and done.

## Generate table of WEB HTML bible book sources (DONE)
In the form:

    order   type    file    title

Command:
```bash    
sed -n "s|<li><a class='\(.*\)' href='\(.*\)'>\(.*\)</a></li>|\1\t\2\t\3|p" bibles/WEB/index.htm \
    | grep -v 'xx' | awk '{ printf("%02d\t%s\n", NR, $0) }' | tee docs/WEB_SRCs.tsv
```
## Tokenize HTML tags & Frequency (DONE)
* Generate tokens of HTML tags + attributes from WEB HTML bible book sources (Gen to Rev)
* Make an ordered frequency table of tokens
```bash    
bin/generate.py WEB-URNs | sort | uniq -c | sort -nr | tee docs/WEB_URNs.txt
```

## Generate TAGL to express WEB Bible content
* Use URNs to determine TAGL ids we need to define
* Create handler functions that define those ids
* Create `tagl/00-WEB-bootstrap.tagl` file
* Create `tagl/{01..n}-<WEB_book_title>`.tagl for each book
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
