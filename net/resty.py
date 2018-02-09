# coding=utf-8
"""
根据 WSGI 规范（http://www.python.org/dev/peps/pep-3333）创建的一个简单的 REST 风格接口。
自带 HTTP basic auth
"""
import cgi
import time

USERNAME = 'admin'
PASSWORD = 'admin'

def notfound_404(environ, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Not Found']


class PathDispatcher:
    def __init__(self):
        self.pathmap = {}

    def __call__(self, environ, start_response):
        if self._authenticated(environ.get('HTTP_AUTHORIZATION')):
            path = environ['PATH_INFO']
            params = cgi.FieldStorage(environ['wsgi.input'],
                                      environ=environ)
            method = environ['REQUEST_METHOD'].lower()
            environ['params'] = {key: params.getvalue(key) for key in params}
            handler = self.pathmap.get((method, path), notfound_404)
            return handler(environ, start_response)
        return self._unauthorized(environ, start_response)

    def register(self, method, path, func):
        self.pathmap[method.lower(), path] = func
        return func

    def _unauthorized(self, environ, start_response):
        start_response('401 Authentication Required',
                       [('Content-Type', 'text/html'),
                        ('WWW-Authenticate', 'Basic')])
        return [b'Unauthorized ']

    def _authenticated(self, header):
        from base64 import b64decode
        if not header:
            return False
        _, encoded = header.split(None, 1)
        decoded = b64decode(encoded).decode('UTF-8')
        username, password = decoded.split(':', 1)
        return (username == USERNAME) and (password == PASSWORD)


_hello_resp = '''\
<html>
  <head>
     <title>Hello {name}</title>
   </head>
   <body>
     <h1>Hello {name}!</h1>
   </body>
</html>'''


def hello_world(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')


_localtime_resp = '''\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
  <hour>{t.tm_hour}</hour>
  <minute>{t.tm_min}</minute>
  <second>{t.tm_sec}</second>
</time>'''


def localtime(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/xml')])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', localtime)

    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()
