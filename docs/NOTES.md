# NOTES
Notes for work todo and done.

## Generate table of WEB HTML bible book sources (DONE)
In the form:

    type    file    title

Command:
```bash    
sed -n "s|<li><a class='\(.*\)' href='\(.*\)'>\(.*\)</a></li>|\1\t\2\t\3|p" bibles/WEB/index.htm | tee docs/WEB_SRCs.txt
```
## Tokenize HTML tags & Frequency (TODO)
* Generate tokens of HTML tags + attributes from WEB HTML bible book sources (Gen to Rev)
* Make an ordered frequency table of tokens
```bash    
bin/generate.py WEB-URNs | sort | uniq -c | sort -nr | tee docs/WEB_URNs.txt
```
* Use results to determine TAGL ids we need to define
