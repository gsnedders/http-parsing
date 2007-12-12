This gives the headers of ~15k pages as parsed by HttpClient, specifically by
<http://jakarta.apache.org/httpcomponents/httpclient-3.x/apidocs/org/apache/
commons/httpclient/HttpMethod.html#getResponseHeaders()>.

This does not include any non-200 responses, and any US-ASCII control characters
(with the exception of 0x09, 0x0A, and 0x0D) are replaced by a 0x20 (space)
character.

It may not be totally grouped by URI, as it's processed multithreadedly.