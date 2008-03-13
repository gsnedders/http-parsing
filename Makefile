# Utilities
commit: validate
	hg commit

validate:
	xmllint --valid --noout http-parsing.xml

show-parsed:
	xmllint http-parsing.xml

# Output
ALL_OUTPUTS=http-parsing.html http-parsing.txt

%.html: %.xml
	xml2rfc $< $@

%.txt: %.xml
	xml2rfc $< $@

html: http-parsing.html
txt: http-parsing.txt
all: $(ALL_OUTPUTS)

# Clean
.PHONY: clean
clean:
	rm -f $(ALL_OUTPUTS)