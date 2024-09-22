WEB_SRCs := $(shell cat WEB_SRCs.txt)

html-tokens:
	@bin/html-tag-urns.py $(WEB_SRCs)
