#!/usr/bin/env python
import BaseHeaderProcessor
import csv
import re

class Date(BaseHeaderProcessor.BaseHeaderProcessor):
	""" Counts the number of occurrences of each Date value type in the
	source data """
	
	rfc822 = re.compile('^(?:(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?,)?(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?([0-9]{1,2})(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)([0-9]{2}|[0-9]{4})(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)([0-9]{2})(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?:(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?([0-9]{2})(?:(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?:(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)?([0-9]{2}))?(?:[\x09\x20]+|[\x09\x20]*(?:\x0D\x0A[\x09\x20]+)+)(?:([+\-])([0-9]{2})([0-9]{2})|(UT|GMT|EST|EDT|CST|CDT|MST|MDT|PST|PDT|[A-I]|[K-Z]))$')
	rfc850 = re.compile('^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),[\x09\x20]+([0-9]{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-([0-9]{2})[\x09\x20]+([0-9]{2}):([0-9]{2}):([0-9]{2})[\x09\x20]+([A-Z]{1,5})$')
	asctime = re.compile('^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[\x09\x20]+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\x09\x20]+([0-9]{1,2})[\x09\x20]+([0-9]{2}):([0-9]{2}):([0-9]{2})[\x09\x20]+([0-9]{4})\x0A?\x00?$')
	
	def process(self):
		values = {}
		for header in self.headers["date"]:
			try:
				values[self.date_type(header["value"])] += 1
			except KeyError:
				values[self.date_type(header["value"])] = 1
		writer = csv.writer(open("Date.csv", "wb"))
		for (value, count) in values.items():
			writer.writerow([value.encode("utf-8"), count])
	
	def date_type(self, date):
		if self.rfc822.match(date):
			return "RFC822"
		elif self.rfc850.match(date):
			return "RFC850"
		elif self.asctime.match(date):
			return "asctime()"
		else:
			return date

if __name__ == '__main__':
	BaseHeaderProcessor.main(Date)