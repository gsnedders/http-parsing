# Utilities
validate:
	xmllint --valid --noout draft-sneddon-http-parsing-00.xml

show-parsed:
	xmllint draft-sneddon-http-parsing-00.xml

# Output
ALL_OUTPUTS=draft-sneddon-http-parsing-00.html draft-sneddon-http-parsing-00.txt

%.html: %.xml
	xml2rfc $< $@

%.txt: %.xml
	xml2rfc $< $@

html: draft-sneddon-http-parsing-00.html
txt: draft-sneddon-http-parsing-00.txt
all: $(ALL_OUTPUTS) validate

# Clean
.PHONY: clean
clean:
	rm -f $(ALL_OUTPUTS)