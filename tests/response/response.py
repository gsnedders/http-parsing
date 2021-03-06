#!/usr/bin/env python
"""Tolerant HTTP Parsing response parsing test suite HTTP Server.

This builds on SimpleHTTPServer by returning entire files (as they
include HTTP headers within them).

"""

__version__ = "0.1"

__all__ = ["HTTPParsingReponseTestServer"]

import os
import BaseHTTPServer
import SimpleHTTPServer

class HTTPParsingReponseTestServer(SimpleHTTPServer.SimpleHTTPRequestHandler):

	"""Simple HTTP request handler with GET and HEAD commands.

	This serves files from the current directory and any of its
	subdirectories.

	The GET and HEAD requests are identical except that the HEAD
	request omits the actual contents of the file.

	"""

	server_version = "HTTPParsingReponseTestServer/" + __version__

	def do_HEAD(self):
		"""Serve a HEAD request."""
		f = self.send_head()
		if f:
			if self.path.startswith("/tests"):
				data = f.read()
				LFLF = data.find("\n\n")
				LFCRLF = data.find("\n\r\n")
				if (-1 < LFLF < LFCRLF):
					self.wfile.write(data[:LFLF + 2])
				elif (LFCRLF > -1):
					self.wfile.write(data[:LFCRLF + 3])
				else:
					self.send_error(500, "Internal Server Error")
			f.close()

	def send_head(self):
		"""Common code for GET and HEAD commands.

		Return value is either a file object (which has to be copied
		to the outputfile by the caller unless the command was HEAD,
		and must be closed by the caller under all circumstances), or
		None, in which case the caller has nothing further to do.

		"""
		if self.request_version == 'HTTP/0.9':
			self.send_error(505, "HTTP Version Not Supported")
			return None
		path = self.translate_path(self.path)
		f = None
		if os.path.isdir(path):
			if not self.path.endswith('/'):
				# redirect browser - doing basically what apache does
				self.send_response(301)
				self.send_header("Location", self.path + "/")
				self.end_headers()
				return None
			elif os.path.exists(os.path.join(path, "index.html")):
				path = index
			else:
				f = self.list_directory(path)
				self.copyfile(f, self.wfile)
				return None
		try:
			f = open(path, "r")
		except IOError:
			self.send_error(404, "File not found")
			return None
		if not self.path.startswith("/tests"):
			self.send_response(200)
			if self.path == "/runtests.html":
				self.send_header("Content-type", "text/html;charset=utf-8")
			elif self.path == "/runtests.js":
				self.send_header("Content-type", "text/javascript;charset=utf-8")
			elif self.path == "/runtests.css":
				self.send_header("Content-type", "text/css;charset=utf-8")
			elif self.path.startswith("/expected"):
				self.send_header("Content-type", "application/json")
			else:
				self.send_header("Content-type", "application/octet-stream")
			fs = os.fstat(f.fileno())
			self.send_header("Content-Length", str(fs[6]))
			self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
			self.end_headers()
		return f


def test(HandlerClass = HTTPParsingReponseTestServer,
		 ServerClass = BaseHTTPServer.HTTPServer):
	BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
	test()
