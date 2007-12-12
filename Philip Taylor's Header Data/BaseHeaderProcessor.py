#!/usr/bin/env python
from gzip import GzipFile
import sys
from xml.dom import minidom

class BaseHeaderProcessor():
	""" This loads a file (given by the first parameter to the object) into a
	dictionary giving access to the data, then calls process()
	"""
	
	headers = {}
	
	def __init__(self, file):
		if file.endswith(".gz"):
			file = GzipFile(file, "rb")
		xmldoc = minidom.parse(file)
		headers = xmldoc.getElementsByTagName('header')
		for header in headers:
			name = header.attributes["name"].value
			uri = header.attributes["uri"].value
			value = header.attributes["value"].value
			try:
				self.headers[name].append({"name": name, "uri": uri, "value": value})
			except KeyError:
				self.headers[name] = [{"name": name, "uri": uri, "value": value}]
	
	def __getitem__(self, key):
		return self.headers[key]

def usage():
	print "Usage: ./BaseHeaderProcessor source_file"

def main(Processor):
	try:
		process = Processor(sys.argv[1])
		process.process()
	except IndexError:
		usage()
		sys.exit(2)