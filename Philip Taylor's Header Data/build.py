#!/usr/bin/env python
"""Header database creator

Creates a database of HTTP headers from specified files

Usage: python build.py [files...]

Options:
  -h, --help                Give this help

Examples:
  build.py                  Builds the database from the default source files
  build.py foo.xml          Builds the database from foo.xml
  build.py foo.xml bar.xml  Builds the database from foo.xml and bar.xml
"""
import getopt
import sqlite3
import sys

import database

def Builder(files):
	conn = sqlite3.connect("headers.db")
	db = database.Database(conn)
	db.build(files)
	conn.close()

def usage():
	print __doc__

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "h", ("help",))
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	
	if "h" in opts or "help" in opts:
		usage()
		sys.exit()
	
	if not args:
		args = ("headers.xml.gz", "headers2.xml.gz")
	
	Builder(args)

if __name__ == "__main__":
	main(sys.argv[1:])