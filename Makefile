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

# Uploader
.PHONY: upload
upload: sftp_upload_batch.tmp $(ALL_OUTPUTS)
	sftp -b $< serveradmin@gsnedders.com@gsnedders.com:domains/stuff.gsnedders.com/html
	rm $<

.PHONY: sftp_upload_batch.tmp
sftp_upload_batch.tmp:
	echo $(ALL_OUTPUTS) | tr " " "\12" | sed -e "s/^/put /g" > $@

# Clean
.PHONY: clean
clean:
	rm -f $(ALL_OUTPUTS)