import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self, code):
        self.send_response(code)
        self.end_headers()

    # Disable default logs
    def log_message(self, format, *args):
        pass

    # Gestion des requêtes GET
    def do_GET(self):
        if self.path == '/':
            self.path = '/interface.html'  # Page principale
        elif self.path == '/manual.html':  # Serve la page `manual.html`
            self.path = '/manual.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Gestion des requêtes POST
    def do_POST(self):
        if self.path.startswith('/api/pos'):
            try:
                parsed_url = urlparse(self.path)
                user_x = int(parse_qs(parsed_url.query)['x'][0])
                user_y = int(parse_qs(parsed_url.query)['y'][0])
                print('x is ' + str(user_x) + ' y is ' + str(user_y))
                self._set_headers(200)

            except:
                print('Failed to parse POST ' + str(self.path))
                self._set_headers(400)
        elif self.path.startswith('/api/marker'):
            try:
                parsed_url = urlparse(self.path)
                user_mid = int(parse_qs(parsed_url.query)['id'][0])
                marker_col = int(parse_qs(parsed_url.query)['col'][0])
                marker_row = parse_qs(parsed_url.query)['row'][0]
                print('Marker ID ' + str(user_mid) + ' column ' + str(marker_col) + ' row ' + str(marker_row))
                self._set_headers(200)

            except:
                print('Failed to parse POST ' + str(self.path))
                self._set_headers(400)
        else:
            print('Unknown request ' + str(self.path))
            self._set_headers(400)

# Lancer le serveur
handler_object = MyHttpRequestHandler
PORT = 8080
httpd = http.server.HTTPServer(("", PORT), handler_object)
print(f"Serveur en cours d'exécution sur le port {PORT}")
httpd.serve_forever()
