#!/usr/bin/env python
import BaseHeaderProcessor
import csv

class ContentType(BaseHeaderProcessor.BaseHeaderProcessor):
	""" Counts the number of occurrences of each Content-Type value in the
	source data """
	
	def process(self):
		values = {}
		for header in self.headers["content-type"]:
			try:
				values[header["value"]] += 1
			except KeyError:
				values[header["value"]] = 1
		writer = csv.writer(open("ContentType.csv", "wb"))
		for (value, count) in values.items():
			writer.writerow([value.encode("utf-8"), count])

if __name__ == '__main__':
	BaseHeaderProcessor.main(ContentType)