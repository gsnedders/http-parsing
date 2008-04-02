#!/usr/bin/env python
import re
import sqlite3
from gzip import GzipFile

try:
	import xml.etree.cElementTree as ElementTree
except ImportError:
	import xml.etree.ElementTree as ElementTree

class Database(object):
	""" Class for interfacing with header database"""
	
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
		# Basic rules
		lws =  r"(?:\r\n)?[\x09\x20]+"
		text = r"(?:[\x20-\xFF]|" + lws + ")"
		seperators = r"[()<>@,;:\\\"/[\]?={} \t]"
		token = r"[!#$%&'*+\-\.^_`|~0-9A-Za-z]+"
		qdtext = r"(?:[\x21\x23-\x5B\x5D-\x7E\x80-\xFF]|" + lws + ")"
		quotedPair = r"\\[\x00-\x7F]"
		quotedString = r'"(?:' + qdtext + '|' + quotedPair + ')*"'
		
		# Message header rules
		fieldName = token
		fieldValue = r"(?:(?:" + text + "*|(?:" + token + "|" + seperators + "|" + quotedString + ")*)|" + lws + ")*"
		
		if not re.match("^" + fieldName + "$", name) or not re.match("^" + fieldValue + "$", value):
			return False
		else:
			return False