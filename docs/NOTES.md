# NOTES
Notes for work todo and done.

## Generate table of WEB HTML bible book sources (DONE)
In the form:
    type    file    title

Command:
    sed -n "s|<li><a class='\(.*\)' href='\(.*\)'>\(.*\)</a></li>|\1\t\2\t\3|p" bibles/WEB/index.htm | tee bibles/WEB_SRCs.txt

## Tokenize HTML tags & Frequency (TODO)
* Generate tokens of HTML tags + attributes in WEB HTML bible book sources (Gen to Rev)
  `bin/generate.py WEB-URNs`
* Make an ordered frequency table of tokens
* Use results to determine TAGL ids we need to define
