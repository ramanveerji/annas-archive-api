from os import cpu_count, environ

from api import server

if __name__ == '__main__':
    server.app.go_fast(host='0.0.0.0',
                       port=int(environ.get('PORT', 8080)),
                       workers=cpu_count() or 1)
