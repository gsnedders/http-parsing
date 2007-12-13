#!/usr/bin/env python
import BaseHeaderProcessor
import csv
import re

class Etag(BaseHeaderProcessor.BaseHeaderProcessor):
	""" Counts the number of occurrences of weak/strong/invalid Etags in the
	source data """
	
	def process(self):
		values = {"Valid (weak)": 0, "Valid (strong)": 0}
		etag = re.compile(r'^(W/)?"([^"]|\")*"$')
		for header in self.headers["etag"]:
			match = etag.match(header["value"])
			if match == None:
				try:
					values[header["value"]] += 1
				except KeyError:
					values[header["value"]] = 1
			elif match.groups()[0] == None:
				values["Valid (strong)"] += 1
			else:
				values["Valid (weak)"] += 1
		writer = csv.writer(open("Etag.csv", "wb"))
		for (value, count) in values.items():
			writer.writerow([value.encode("utf-8"), count])

if __name__ == '__main__':
	BaseHeaderProcessor.main(Etag)