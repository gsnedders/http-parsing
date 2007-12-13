#!/usr/bin/env python
import BaseHeaderProcessor
import csv

class Server(BaseHeaderProcessor.BaseHeaderProcessor):
	""" Counts the number of occurrences of each Server value in the source data """
	
	def process(self):
		values = {}
		for header in self.headers["server"]:
			sp = header["value"].lstrip().find('\x20')
			if (sp > -1):
				value = header["value"].lstrip()[:sp]
			else:
				value = header["value"]
			try:
				values[value] += 1
			except KeyError:
				values[value] = 1
		writer = csv.writer(open("Server.csv", "wb"))
		for (value, count) in values.items():
			writer.writerow([value.encode("utf-8"), count])

if __name__ == '__main__':
	BaseHeaderProcessor.main(Server)