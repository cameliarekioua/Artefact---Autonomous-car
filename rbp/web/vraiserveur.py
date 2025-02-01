import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
from movement import *
from auto1 import *
from auto2 import *

def get_int_coos(coos):
	x = coos[1]
	column = int(x) - 1
	y = coos[0]
	row = 0 if y=="G" else (1 if y=="F" else (2 if y=="E" else (3 if y=="D" else (4 if y=="C" else (5 if y=="B" else (6 if y=="A" else -1))))))
	return column, row

#Simple class to handle HTTP requests
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	def _set_headers(self, code):
		self.send_response(code)
		self.end_headers()

	#disable default logs
	def log_message(self, format, *args):
		pass

	def do_GET(self):
		print("requête GET\n")
		if self.path == '/':
        	    self.path = '/interface.html'  # Page principale
	            return http.server.SimpleHTTPRequestHandler.do_GET(self)

		else:
		    return http.server.SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		print("Request : " + self.path+"\n")

		if self.path.startswith('/api/mode'):
			self.send_response(200)
			self.end_headers()



		elif self.path.startswith('/api/move'):
			try:
				parsed_url=urlparse(self.path)
				query_params = parse_qs(parsed_url.query)
				direction = query_params.get('direction', [None])[0]
				self.send_response(200)
				self.end_headers()
				print("Request processed\n")
				c=controller.Controller()
				if direction=='forward':
					forward(c,25,10)
				elif direction=='backward':
					backward(c,25,10)
				elif direction=='left':
					turn_left(c,90,20)
				else :
					turn_right(c,90,10)

			except:
				print('Failed to parse POST ' + str(self.path) )
				self.send_response(400)
				self.end_headers()

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
				self.send_response(200)
				self.end_headers()

			except:
				print('Failed to parse POST ' + str(self.path) )
				self._set_headers(400)

		elif self.path.startswith('/api/launch'):
			try:
				print("ok")
				parsed_url = urlparse(self.path)
				query_parameters = parse_qs(parsed_url.query)
				target_case = query_parameters.get('target', [None])[0]
				start_case = query_parameters.get('start', [None])[0]

				print("ok pour l'instant")

				scr = get_int_coos(start_case)
				print("1 appel ok")
				to = get_int_coos(target_case)
				print(1)
				move_1(scr,to)

				self.send_response(200)
				self.end_headers()

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
