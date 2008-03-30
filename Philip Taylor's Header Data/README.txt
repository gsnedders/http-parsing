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

This describes an XML format for storing data relating to HTTP headers.


Notational Conventions
----------------------

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in BCP 14, [RFC2119], as scoped to those conformance
targets.


Documents
---------

This format is described in terms of [XML1.0]. Documents MUST be valid according
to the DOCTYPE given in the appendix of this document. The order of elements in
the document is irrelevant, and any parsers MUST NOT assign any meaning
dependant on the order.

THE "survey" ELEMENT
--------------------

The "survey" element represents a survey of HTTP headers. It MUST be the root
element of all conforming documents. It MUST contain no elements apart from the
"processed", "redirect", "header", and "error" elements. It MUST contain no
character data apart from any that matches the "S" production in [XML10].


THE "processed" ELEMENT
-----------------------

The "processed" element represents the start of a IRI [RFC3987] being processed.
The IRI is specified by the "uri" attribute. The "uri" attribute MUST match the
"IRI" specification in [RFC3987]. The element MUST have no content.