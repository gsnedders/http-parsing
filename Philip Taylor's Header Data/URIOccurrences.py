#!/usr/bin/env python
import BaseHeaderProcessor
import csv

class URIOccurrences(BaseHeaderProcessor.BaseHeaderProcessor):
	""" Counts the number of occurrences of each URIs in the source data """
	
	def process(self):
		URIs = {}
		for (k, value) in self.headers.items():
			for header in value:
				try:
					URIs[header["uri"]] += 1
				except KeyError:
					URIs[header["uri"]] = 1
		writer = csv.writer(open("URIOccurrences.csv", "wb"))
		for (uri, count) in URIs.items():
			writer.writerow([uri.encode("utf-8"), count])

if __name__ == '__main__':
	BaseHeaderProcessor.main(URIOccurrences)