"""Tolerant HTTP Parsing response parsing test suite HTTP Server.

This builds on SimpleHTTPServer by returning entire files (as they
include HTTP headers within them).

"""


__version__ = "0.1"

__all__ = ["HTTPParsingReponseTestServer"]

import os
import SimplePieHTTPServer

class HTTPParsingReponseTestServer(SimplePieHTTPServer.SimpleHTTPRequestHandler):

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
            data = f.read()
            f.close()
            LFLF = data.find("\n\n")
            LFCRLF = data.find("\n\r\n")
            if (LFLF < LFCRLF):
                self.wfile.write(data[:LFLF])
            else:
                self.wfile.write(data[:LFCRLF])

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
        if os.path.samefile(path, __file__):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
        return f


def test(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
