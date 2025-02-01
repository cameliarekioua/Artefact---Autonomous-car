import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
from movement import *


#Simple class to handle HTTP requests
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	def _set_headers(self, code):
		self.send_response(code)
		self.end_headers()

	#disable default logs
	def log_message(self, format, *args):
		pass

	def do_GET(self):
		print("requête GET")
		if self.path == '/':
        	    self.path = '/interface.html'  # Page principale
	            return http.server.SimpleHTTPRequestHandler.do_GET(self)
		else:
		    return http.server.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		print("Request : " + self.path)
		if self.path.startswith('/api/mode'):
			try:
				parsed_url=urlparse(self.path)
				query_params = parse_qs(parsed_url.query)
				print(query_params)
				mode = query_params.get('mode', [None])[0]
				print(mode)
				c=controller.Controller()
				



				self._set_headers(200)

			except:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)


		elif self.path.startswith('/api/move'):
			try:
				print("direction")
				print(self.path)
				parsed_url=urlparse(self.path)
				query_params = parse_qs(parsed_url.query)
				print(query_params)
				direction = query_params.get('direction', [None])[0]
				print(direction)
				c=controller.Controller()
				if direction=='forward':
					forward(c,50,10)
				elif direction=='backward':
					backward(c,50,10)
				elif direction=='left':
					print("On tourne à droite")
					turn_left(c,90,20)
					print("En fait c'était à gauche")
				else :
					turn_right(c,90,10)
				self._set_headers(200)
			except Exception as e:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)

		elif self.path.startswith('/api/pos'):
			try:
				print("Hello world")
				parsed_url = urlparse(self.path)
				user_x = int(  parse_qs(parsed_url.query)['x'][0] )
				user_y = int(  parse_qs(parsed_url.query)['y'][0] )
				print('x is ' + str(user_x) + ' y is ' + str(user_y))
				self._set_headers(200)

			except:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)
		elif self.path.startswith('/api/marker'):
			try:
				parsed_url = urlparse(self.path)
				user_mid = int(  parse_qs(parsed_url.query)['id'][0] )
				marker_col = int(  parse_qs(parsed_url.query)['col'][0] )
				marker_row = parse_qs(parsed_url.query)['row'][0]
				print('Marker ID ' + str(user_mid) + ' column ' + str(marker_col) + ' row ' + str(marker_row))
				self._set_headers(200)

			except:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)
		else:
			print('Unknown request ' + str(self.path) )
			self._set_headers(400)

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8080
httpd = http.server.HTTPServer(("", PORT), handler_object)
httpd.serve_forever()
