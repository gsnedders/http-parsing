#!/usr/bin/env python
import re
import sqlite3
from gzip import GzipFile

try:
	import xml.etree.cElementTree as ElementTree
except ImportError:
	import xml.etree.ElementTree as ElementTree

# Regular expressions:
# Basic rules
OCTET = r"[\x00-\xFF]"
CHAR = r"[\x00-\x7F]"
UPALPHA = r"[A-Z]"
LOALPHA = r"[a-z]"
ALPHA = r"(?:" + UPALPHA + "|" + LOALPHA + ")"
DIGIT = r"[0-9]"
CTL = r"[\x00-\x19\x7F]"
CR = r"\x0D"
LF = r"\x0A"
SP = r"\x20"
HT = r"\x09"
DQUOTE = r"\x22"
CRLF = CR + LF
LWS =  r"(?:(?:" + CRLF + ")?[" + SP + HT + "]+)"
TEXT = r"(?:[\x20-\xFF]|" + LWS + ")"
HEX = r"[A-Fa-f0-9]"
seperators = r"[()<>@,;:\\\"/[\]?={}" + SP + HT + "]"
token = r"[!#$%&'*+\-\.^_`|~0-9A-Za-z]+"
qdtext = r"(?:[\x21\x23-\x5B\x5D-\x7E\x80-\xFF]|" + LWS + ")"
quotedPair = r"(?:\\" + CHAR + ")"
quotedString = r'"(?:' + qdtext + '|' + quotedPair + ')*"'
ctext = r"(?:[\x20-\x27\x30-\xFF]|" + LWS + ")"
comment = r"\((?:" + ctext + "|" + quotedPair + ")*\)"

# Implicit LWS
implicitLWS = LWS + "*"

# HTTP Version
HTTPVersion = r"HTTP/[1-9]+" + DIGIT + "*\.[1-9]+" + DIGIT + "*"

# Uniform Resource Identifiers
# Alias of what we already have
alpha = ALPHA
loalpha = LOALPHA
upalpha = UPALPHA
digit = DIGIT
hex = HEX

# Start the real building
alphanum = r"(?:" + alpha + "|" + digit + ")"
escaped = r"%" + hex + hex
mark = r"[\-_.!~*'()]"
unreserved = r"(?:" + alphanum + "|" + mark + ")"
reserved = r"[;/?:@&=+$,]"
uric = r"(?:" + reserved + "|" + unreserved + "|" + escaped + ")"
fragment = uric + "*"
query = uric + "*"
pchar = r"(?:" + unreserved + "|" + escaped + "|[:@&=+$,])"
param = pchar + "*"
segment = pchar + "*(?:;" + param + ")*"
path_segments = segment + "(?:/" + segment + ")*"
port = digit + "*"
IPv4address = digit + "+\." + digit + "+\." + digit + "+\." + digit + "+"
toplabel = "(?:" + alpha + "|" + alpha + "(?:" + alphanum + "|-)*" + alphanum + ")"
domainlabel = "(?:" + alphanum + "|" + alphanum + "(?:" + alphanum + "|-)*" + alphanum + ")"
hostname = "(?:" + domainlabel + ".)*" + toplabel + "\.?"
host = "(?:" + hostname + "|" + IPv4address + ")"
hostport = host + "(?::" + port + ")?"
userinfo = "(?:" + unreserved + "|" + escaped + "|[;:&=+$,])*"
server = "(?:(?:" + userinfo + "@)?" + hostport + ")?"
reg_name = "(?:" + unreserved + "|" + escaped + "|[$,;:@&=+])+"
authority = "(?:" + server + "|" + reg_name + ")"
scheme = alpha + "(?:" + alpha + "|" + digit + "|[+\-.])*"
rel_segment = "(?:" + unreserved + "|" + escaped + "|[;@&=+$,])+"
abs_path = "/" + path_segments
rel_path = rel_segment + "(?:" + abs_path + ")?"
net_path = "//" + authority + "(?:" + abs_path + ")?"
uric_no_slash = "(?:" + unreserved + "|" + escaped + "|[;?:@&=+$,])"
opaque_part = uric_no_slash + uric + "*"
hier_part = "(?:" + net_path + "|" + abs_path + ")(?:\?" + query + ")?"
relativeURI = "(?:" + net_path + "|" + abs_path + "|" + rel_path + ")(?:\?" + query + ")?"
absoluteURI = scheme + ":(?:" + hier_part + "|" + opaque_part + ")"
URIreference = "(?:" + absoluteURI + "|" + relativeURI + ")?(?:#" + fragment + ")?"

# HTTP URL
httpURL = "http://" + host + "(?::" + port + ")?(?:" + abs_path + "(?:\?" + query + ")?)?"

# Full Date
wkday = r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
weekday = r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
month = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
time = DIGIT + "{2}:" + DIGIT + "{2}:" + DIGIT + "{2}"
date1 = DIGIT + "{2}" + SP + month + SP + DIGIT + "{4}"
date2 = DIGIT + "{2}-" + month + "-" + DIGIT + "{2}"
date3 = month + SP + "(?:" + DIGIT + "{2}|" + SP + DIGIT + ")"
rfc1123Date = wkday + "," + SP + date1 + SP + time + SP + "GMT"
rfc850Date = weekday + "," + SP + date2 + SP + time + SP + "GMT"
asctimeDate = wkday + SP + date3 + SP + time + SP + DIGIT + "{4}"
HTTPdate = "(?:" + rfc1123Date + "|" + rfc850Date + "|" + asctimeDate + ")"

# Delta seconds
deltaSeconds = DIGIT + "+"

# Character sets
charset = token

# Content coding
contentCoding = token

# Transfer coding
attribute = token
value = "(?:" + token + "|"+ quotedString + ")"
parameter = attribute + "=" + value
transferExtension = token + "(?:;" + parameter + ")*"
transferCoding = "(?:[Cc][Hh][Uu][Nn][Kk][Ee][Dd]|" + transferExtension + ")"

# Media type
type = token
subtype = token
mediaType = type + "/" + subtype + "(?:;" + parameter + ")*"

# Product token
productVersion = token
product = token + "(?:/" + productVersion + ")?"

# Quality value
qvalue = r"(?:0(?:\." + DIGIT + "{0,3})?|1(?:\.0{0,3})?)"

# Language tags
primaryTag = ALPHA + "{1,8}"
subtag = ALPHA + "{1,8}"
languageTag = primaryTag + "(?:" + subtag + ")*"

# Entity tags
weak = r"[Ww]/"
opaqueTag = quotedString
entityTag = "(?:" + weak + ")?" + opaqueTag

# Range units
bytesUnit = "[Bb][Yy][Tt][Ee][Ss]"
otherRangeUnit = token
rangeUnit = "(?:" + bytesUnit + "|" + otherRangeUnit + ")"

# Message header rules
fieldName = token
fieldValue = r"(?:" + TEXT + "|" + quotedString + "|" + LWS + ")*"

# Accept header
mediaRange = r"(?:(?:" + type + "|*)/*|" + type + "/" + subtype + ")(?:;" + parameter + ")*"
acceptExtension = ";" + token + "(?:=(?:" + token + "|" + quotedString + "))?"
acceptParams = ";q=" + qvalue + "(?:" + acceptExtension + ")*"
accept = 

# Compile anchored versions of what we need
fieldNameCompiled = re.compile("^" + fieldName + "$")
fieldValueCompiled = re.compile("^" + fieldValue + "$")

# Dictionary of headers and their regular expressions
headers = {"accept": acceptCompiled,}

class Database(object):
	""" Class for interfacing with header database"""
	
	self.unknown = -1
	self.invalid = 0
	self.valid = 1
	
	def __init__(self, db_conn):
		""" Creates a Database object with a given DB Connection (that must
		comply to DB-API 2.0 (PEP 249)."""
		self.conn = db_conn
		self.conn.cursor().execute("""CREATE TABLE IF NOT EXISTS headers
			(uri TEXT,
			name TEXT,
			value TEXT,
			isValid INT)""")
		self.conn.cursor().execute("CREATE INDEX IF NOT EXISTS uri ON headers (uri)")
		self.conn.cursor().execute("CREATE INDEX IF NOT EXISTS name ON headers (name)")
		self.conn.commit()
	
	def build(self, source_files):
		"""Build the database from the given list of source files."""
		for source_file in source_files:
			if source_file.endswith(".gz"):
				source_file = GzipFile(source_file, "rb")
			tree = ElementTree.parse(source_file)
			headers = tree.findall("header")
			for header in headers:
				uri = header.get("uri")
				name = header.get("name").lower()
				value = header.get("value")
				isValid = self.isValid(name, value)
				self.conn.cursor().execute("INSERT INTO headers VALUES (?, ?, ?, ?)", \
					(uri, name, value, isValid))
			self.conn.commit()
	
	def isValid(self, name, value):
		"""Checks if a header is valid"""		
		if not fieldNameCompiled.search(name) or not fieldValueCompiled.search(value):
			return self.invalid
		elif name in headers:
			if headers[name](value):
				return self.valid
			else:
				return self.invalid
		else:
			return self.unknown