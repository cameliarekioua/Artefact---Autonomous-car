# Serveur HTTP sur le Raspberry Pi
import http.server
import socketserver

PORT = 8080  # Utilise un port au-dessus de 1024

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/interface.html'  # Page principale
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path.startswith('/api/move'):
            command = self.path.split('=')[-1] # Extraire la commande de mouvement
            print(f'Commande de mouvement reçue : {command}')
            # la logique pour contrôler la voiture ( à faire , frame work ):


            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Commande reçue")
        else:
            self.send_response(404)
            self.end_headers()

            # Lancer le serveur
            with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
            print(f"Serveur en cours d'exécution sur le port {PORT}")
            httpd.serve_forever()