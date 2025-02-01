import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
from movement import *
from auto1 import *
from auto2 import *

def coordinates(cell):

    letter_to_row = {
        'G': 0, 'F': 1, 'E': 2, 'D': 3, 'C': 4, 'B': 5, 'A': 6
    }
    
    letter = cell[0]
    column = int(cell[1]) - 1  
    row = letter_to_row.get(letter, None)
    if row is None:
        raise ValueError(f"Invalid letter: {letter}")
    
    return row, column

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
			self._set_headers(200)


		elif self.path.startswith('/api/move'):
			try:
				parsed_url=urlparse(self.path)
				query_params = parse_qs(parsed_url.query)
				direction = query_params.get('direction', [None])[0]
				c=controller.Controller()
				if direction=='forward':
					forward(c,50,10)
				elif direction=='backward':
					backward(c,50,10)
				elif direction=='left':
					turn_left(c,90,20)
				else :
					turn_right(c,90,10)
				self._set_headers(200)

			except:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)

		elif self.path.startswith('/api/automatic_mode'):
			try:
				parsed_url = urlparse(self.path)
				automatic_mode = parsed_url.query
				if(automatic_mode == "navigate"):
					print("Navigate Mode")
				elif(automatic_mode == "flaghunt"):
					print("Flag Hunt Mode")
					c=controller.Controller()
					capture_the_flag(c)
				self._set_headers(200)

			except:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)

		elif self.path.startswith('/api/launch'):
			try:
				parsed_url = urlparse(self.path)
				query_parameters = parse_qs(parsed_url.query)
				target_case = query_parameters.get('target', [None])[0]
				start_case = query_parameters.get('start', [None])[0]
				self._set_headers(200)

				scr=coordinates(start_case)
				to=coordinates(target_case)
				move_1(scr,to)

			except:
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
