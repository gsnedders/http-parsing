#!/usr/bin/env python
import BaseHeaderProcessor
import csv

class HeaderCount(BaseHeaderProcessor.BaseHeaderProcessor):
	""" Counts the number of occurrences of each header in the source data """
	
	def process(self):
		headers = {}
		for (k, value) in self.headers.items():
			for header in value:
				try:
					headers[header["name"]] += 1
				except KeyError:
					headers[header["name"]] = 1
		writer = csv.writer(open("HeaderCount.csv", "wb"))
		for (uri, count) in headers.items():
			writer.writerow([uri.encode("utf-8"), count])

if __name__ == '__main__':
	BaseHeaderProcessor.main(HeaderCount)