headers.xml gives the headers of ~15k pages as parsed by HttpClient,
specifically by <http://jakarta.apache.org/httpcomponents/httpclient-3.x/apidocs
/org/apache/commons/httpclient/HttpMethod.html#getResponseHeaders()>. It does
not include any non-200 responses, and any US-ASCII control characters (with the
exception of 0x09, 0x0A, and 0x0D) are replaced by a 0x20 (space) character. It
may not be grouped by URI fully, as it is not processed by a single thread.

headers2.xml gives the headers of ~125K pages as parsed by HttpClient,
specifically by <http://jakarta.apache.org/httpcomponents/httpclient-3.x/apidocs
/org/apache/commons/httpclient/HttpMethod.html#getResponseHeaders()>. Headers
are only included for 200 responses.


DATA FORMAT
===========

INTRODUCTION
------------

This describes an XML format for storing surveys relating to HTTP headers.


Notational Conventions
----------------------

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in BCP 14, [RFC2119], as scoped to those conformance
targets.


Documents
---------

This format is described in terms of [XML10]. Documents MUST be valid according
to the DOCTYPE given in the appendix of this document. The order of elements in
the document is irrelevant, and any parsers MUST NOT assign any meaning
dependant on the order. The data for a single URI MAY occur multiple times.

THE "survey" ELEMENT
--------------------

The "survey" element represents a survey of HTTP headers. It MUST be the root
element of all conforming documents. It MUST contain no elements apart from the
"processed", "redirect", "header", and "error" elements. It MUST contain no
character data apart from any that matches the "S" production in [XML10].


THE "processed" ELEMENT
-----------------------

The "processed" element represents the start of a IRI [RFC3987] being processed.
The IRI MUST be specified by the "uri" attribute. The "uri" attribute MUST match
the "IRI" specification in [RFC3987]. The element MUST have no content.


THE "redirect" ELEMENT
----------------------

The "redirect" element represents a redirect. This MUST be a redirect caused by
a 3xx HTTP status code. It MAY merge multiple redirects into one element (e.g.,
a 301 followed by a 307 may be a single redirect). The original URI MUST be
specified by the "uri" attribute. The URI it is redirected to MUST be specified
by the "destination" attribute. Both the "uri" and the "destination" attribute
MUST match the "IRI" specification in [RFC3987]. The element MUST have no
content.


THE "header" ELEMENT
--------------------

The "header" element represents an HTTP header. The "uri" attribute MUST be the
IRI that the header came from, and MUST match the "IRI" specification in
[RFC3987]. The "name" attribute MUST specify the field-name of the header. The
"value" attribute MUST specify the field-value of the header.


THE "error" ELEMENT
-------------------

The "error" element represents an error message. The "uri" attribute MUST be the
IRI that the error occurred while trying to fetch/parse. The "type" attribute
MUST case-sensitively match "io" if the error occurred at the I/O level; it
MUST case-sensitively match "http" if the request resulted in an HTTP error;
otherwise, it MUST case-sensitively match "other". There MAY be a "code"
attribute except if the "type" attribute is case-sensitively equal to "http"
in which case it MUST be present and MUST equal the status code of the response.
There MAY be a "message" attribute providing human-readable information about
the error.


REFERENCES
----------

[RFC2119]: Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
[RFC3987]: Duerst, M. and M. Suignard, "Internationalized Resource Identifiers (IRIs)", RFC 3987, January 2005.
[XML10]: Bray, T., Paoli, J., Sperberg-McQueen, C.M., Maler, E., and F. Yergeau, "Extensible Markup Language (XML) 1.0 (Fourth Edition)", World Wide Web Consortium Recommendation REC-xml, August 2006, <http://www.w3.org/TR/2006/REC-xml-20060816/>.


APPENDIX A: DOCTYPE
-------------------

<!ELEMENT survey (processed | redirect | header | error)*>

<!ELEMENT processed EMPTY>
<!ATTLIST processed
	uri	CDATA	#REQUIRED>

<!ELEMENT redirect EMPTY>
<!ATTLIST redirect
	uri	CDATA	#REQUIRED
	destination	CDATA	#REQUIRED>

<!ELEMENT header EMPTY>
<!ATTLIST header
	uri	CDATA	#REQUIRED
	name	CDATA	#REQUIRED
	value	CDATA	#REQUIRED>

<!ELEMENT error EMPTY>
<!ATTLIST error
	uri	CDATA	#REQUIRED
	type	(io|http|other)	#REQUIRED
	message	CDATA	#IMPLIED
	code	CDATA	#IMPLIED>
	