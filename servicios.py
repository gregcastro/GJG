# encoding=utf-8
# -*- coding: utf-8 -*-
import configuracion
from flask import Flask, request, json, make_response, render_template, json, flash, redirect, url_for, session
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime, date, time, timedelta
import jwt, calendar, hashlib, time, re, pdfkit
from flaskext.mysql import MySQL
import requests

errors = {
    'UsuarioExistente': {
        'error': "El usuario indicado ya existe",
        'status': 409,
    },
    'RecursoNoExistente': {
        'error': "El recurso con ese ID no existe",
        'status': 410,
    },
   	'ErrorLogin': {
        'error': "Las credenciales ingresadas no son válidas",
        'status': 410,
    },
    'ProductoNotFound': {
        'error': "El producto seleccionado no existe",
        'status': 404,
    },
    'ProductoYaCreado': {
        'error': "El producto que desea ingresar ya esta creado",
        'status': 410,
    },
   	'ErrorPeticion': {
        'error': "Error en la peticion",
        'status': 400,
    },
    'ErrorAlDecodificar': {
        'error': "Error al decodificar el token",
        'status': 412,
    }
}


success = {
    'RegistroCompletado': {
        'message': "Usuario registrado con exito!",
        'status': 201,
    },
    'LoginCompletado':{
    	'message': "Login realizado exitosamente",
    	'status' : 200,
    }
}

app = configuracion.app_conf()
api = Api(app, errors=errors)
mysql = MySQL()
mysql.init_app(app)

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'gjg'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.secret_key = "Estodeberiaserandom"

url = 'http://localhost:5000'
headers = {'content-type': 'application/json'}


@app.route('/', methods=['GET','POST'])
def index():
	# Si tengo token en el local storage estoy logeado, sino no
	# Realizar pruebas en el token para ver si funciona lo del tiempo de vencimiento.
	if(request.method == 'GET'): 
		if(session.get('logged_in')):
			return render_template("index.html", current_user=session.get('logged_in'))
		return render_template("index.html")
	else:
		data = {"correo" : request.form['correo'], "clave" : request.form['password'] }
		# print(data)
		r = requests.post(url+'/login', json.dumps(data), headers=headers)
		response = r.json()
		
		if response['status'] == 200:

			session['logged_in'] = response['access_token']
			return render_template("index.html", current_user=response['access_token'])

		return render_template("index.html", error=response['error'])

@app.route('/cerrar_sesion', methods=['GET'])
def cerrar_sesion():
	if(session.get('logged_in')): 
		session.pop('logged_in', None)
		return redirect(url_for('index'))


#Funcion seleccionar que muestra la ventana luego del logueo
@app.route('/seleccion')
def seleccionar():
	return selec_funct(session)

@app.route('/signup', methods=['GET','POST'])
def registro():
	if(session.get('logged_in')):
		return redirect(url_for('index'))
	else:
		if(request.method == 'GET'): return render_template("registro.html")
		else:
			if request.form['password'] == request.form['repassword']:
				data = {  
						"correo" : request.form['correo'],
						"clave" : request.form['password'],
						"descripcion" : request.form['nombre'],
						"rif" : request.form['rif'],
						"codPostal" : request.form['codPostal']
					   }
				# print ( json.dumps(data) )
				
				r = requests.post(url+'/registro', json.dumps(data), headers=headers )
				response = r.json()
				# print(response['message'])

				if 'message' not in response:
					return render_template("registro.html", error=response['error'])

				return render_template("registro.html", registrado=response['message'])
			else:
				return render_template("registro.html", error='Las contraseñas no coinciden')
	
		


# @app.route('/inicio_sesion', methods=['POST'])
# def inicio_sesion():
# 	data = {"correo" : request.form['correo'], "clave" : request.form['password'] }
# 	r = requests.post(url+'/login', json.dumps(data), headers=headers)
# 	response = r.json()
	
# 	if response['status'] == 200:

# 		flash(response['access_token'])
# 		return redirect(url_for('index'))

# 	return render_template("index.html", error=response['error'])



# r = requests.get('http://127.0.0.1:5000/consultarTarifa/1060/8.5')
# x = r.json()
# print(x['monto_cotizado'])

#Recibe argumento variado, en caso de ser POST recibe usuario y clave, sino solo retorna los valores del template
def index_funct(*args):
	bad_user = None
	if len(args) > 0:
		# hashinput_user = hashlib.sha256(str(args[0]).encode('utf-8')).hexdigest() #Le hice encriptacion sha256
		correo = args[0]
		hashinput_password = hashlib.sha256(str(args[1]).encode('utf-8')).hexdigest() #Le hice encriptacion sha256
		
		cursor = mysql.connect().cursor()
		
		cursor.execute("SELECT * FROM cliente WHERE correo = %s AND clave = %s ", correo, hashinput_password)
		data = cursor.fetchall()

		if ( data == None ) :
			bad_user = "Usuario o contraseña erróneos. Por favor, intente de nuevo.";
		else:
			args[2]['logged_in'] = args[0] 
			return redirect(url_for('seleccionar'))
	return render_template("index.html", err=bad_user)



#Funcion que retorna la pantalla principal despues de logeo (tambien elimina la sesion)
def selec_funct(session):
	if session.get('logged_in'):
		return render_template("registrar.html")
	else:
		return redirect(url_for('index'))


codPostalOrigen = 1060;
# Cuando registran un cliente colocan el codigo postal donde se encuentra...
# hacer dos consultar tarifa, si estas registrado mandas el idCliente (rif) , en el caso de no estar registrado mandas codPostal origen y destino
# El consultarTarifa no se manda token, pero se manda idCliente
# solicitarDistribucion ajuro tiene q estar registrado y se envia el token de sesion
# Tomar en cuenta que el paquete se envia desde el comercio..
# No habra prioridad.




class Register(Resource):
	#FALTA
	# 1. Expresion regular de que el rif solo sea un numero de 8 u 9 digitos, en caso de ser 8 se coloca un 0 a la izquierda.
	# 2. Expresion regular de que el codPostal sea un numero de 4 digitos.
	# 3. Evaluar si hay tiempo de crear mensajes personalizados para cada error de peticion.
	def post(self):
		data = request.get_json()
		print('data = ',data)
		if ('correo' not in data) or ('clave' not in data) or ('rif' not in data) or ('codPostal' not in data) or \
		(re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data['correo']) == None) or \
		(len(str(data['clave'])) < 8):
			return errors['ErrorPeticion'], 400

		con = mysql.connect()
		cursor = con.cursor()

		if ('descripcion') not in data:
			data['descripcion'] = None

		cursor.execute("SELECT correo from cliente WHERE correo=%s", data['correo'])
		email_actual = cursor.fetchone()
		if(email_actual != None): return errors['UsuarioExistente'], 409
		hashinput_password = hashlib.sha256(str(data['clave']).encode('utf-8')).hexdigest() #Le hice cifrado sha256

		cursor.execute("INSERT INTO cliente (correo, clave, descripcion, rif, codPostal) VALUES (%s,%s,%s,%s,%s)", (data['correo'], hashinput_password, data['descripcion'], data['rif'], data['codPostal']))
		con.commit()
		return success['RegistroCompletado'], 201

class Login(Resource):
	def post(self):

		data = request.get_json()

		if ('correo' not in data) or ('clave' not in data):
			return errors['ErrorPeticion'], 400

		hashinput_password = hashlib.sha256(str(data['clave']).encode('utf-8')).hexdigest() #Le hice cifrado sha256

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("SELECT correo FROM cliente WHERE correo=%s AND clave=%s", (data['correo'], hashinput_password))
		check_log = cursor.fetchone()


		if(check_log != None): 
			#Obtengo la fecha y hora actual
			ahora = time.time()
			#Sumo 30 minutos a la fecha actual
			mas_30_min = 30*60
			hoy_mas_30_minutos = ahora + mas_30_min

			payload = {
			    'sub' : data['correo'],
			    'iat' : ahora,
			    'exp' : hoy_mas_30_minutos
			}

			cod = jwt.encode( payload , 'secret', algorithm='HS256')
			cod = str(cod).split("'")

			success['LoginCompletado']['access_token'] = cod[1]
			return success['LoginCompletado'], 200

		return errors['ErrorLogin'], 410

class consultarTarifa(Resource):
	def get(self, codPostal, peso):
		con = mysql.connect()
		cursor = con.cursor()

		print(codPostal)
		print(peso)

		codPostal = int(codPostal)
		if (codPostal >= 1000 and codPostal < 9000):
			# Aqui adentro va la logica para calcular el costo, basandose en la distancia y el peso total del encargo
			costo = 5000.30
			return dict(monto_cotizado=costo)


		return errors['ErrorPeticion'], 400

class solicitarDistribucion(Resource):
	def post(self):

		data = request.get_json()

		#Validar campos obligatorios
		if ('correo' not in data) or ('cedula' not in data) or ('nombre' not in data) or ('telefono' not in data) or ('direccion' not in data) or ('codPostal' not in data) or ('peso' not in data):
			return errors['ErrorPeticion'], 400

		codPostal = int(data['codPostal'])
		if (codPostal >= 1000 and codPostal < 9000):

			#calcular fecha de llegada del producto
			#Obtengo la fecha y hora actual
			fechaActual = date.today()
			print("fechaActual = ", fechaActual)

			#dependiendo de lo lejos le coloco una cantidad de dias
			fechaEstimada = fechaActual + timedelta(days=3)
			print("fechaEstimada = ", fechaEstimada)

			#En el caso de conservar el registro ´fechaEnvio´ colocar que se envia el siguiente dia si ya pasaron mas de las 10am
			fechaEnvio = fechaActual + timedelta(days=1)

			con = mysql.connect()
			cursor = con.cursor()

			cursor.execute("INSERT INTO direccion (codPostal, dirEnvio) VALUES(%s,%s)", (codPostal, data['direccion']) )
			con.commit()

			cursor.execute("SELECT idDireccion FROM direccion WHERE codPostal=%s AND dirEnvio=%s", (codPostal, data['direccion']))
			idDireccion = cursor.fetchone()[0]
			print("idDireccion = ", idDireccion)

			#Por ahora voy a asumir que ya tengo el producto y no tengo que simular que me tiene que llegar por parte del comercio


			#Dependiendo del peso del encargo le asigno una categoria (esto se hace antes de calcular el costo OBVIAMENTE)
			cursor.execute("SELECT * FROM categoriaPeso")
			categoriaPeso = cursor.fetchall()
			print("categoriaPeso = ", categoriaPeso)

			peso = data['peso']
			for x in categoriaPeso:
				if (peso >= x[2] and peso <= x[3]):
					idCategoriaPeso = x[0]
					break

			#Supongo que aqui siempre comenzara por 1, luego hay que simular los otros estatus 
			idEstatus = 1

			#En este momento que no se como obtendre el idCliente lo voy a cablear en 1.
			idCliente = 1

			#Por ahora no se si habra una prioridad de envio
			idPrioridadEnvio = 1

			# Aqui adentro va la logica para calcular el costo, basandose en la distancia y el peso total del encargo
			costo = 5000.30

			cursor.execute("INSERT INTO encargo (cedula, nombre, telefono, correo, peso, fechaEnvio, fechaEstimada, dirFuente, costo, idDireccion, idEstatus, idCliente, " +
						   "idPrioridadEnvio, idCategoriaPeso) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ( data['cedula'], data['nombre'], data['telefono'], data['correo'], data['peso'], fechaEnvio, fechaEstimada, None, costo, idDireccion, idEstatus, idCliente, idPrioridadEnvio , idCategoriaPeso  ) )
			con.commit()

		return "fin"

class actualizarEstadoSolicitud(Resource):
	def put(self):

		data = request.get_json()

		if ('estatus' not in data) or ('idEncargo' not in data):
			return errors['ErrorPeticion'], 400

		#Comprobar que el idEncargo existe y el estatus es valido, es decir.. que exista y que sea mayor al anterior
		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("SELECT * FROM encargo WHERE idEncargo = %s", (data['idEncargo']))
		encargo = cursor.fetchall()
		if (encargo == None):
			return "No existe este encargo"

		cursor.execute("SELECT * FROM estatusencargo WHERE idEstatus = %s", (data['estatus']))
		estatus = cursor.fetchall()
		if (estatus == None):
			return "No existe este estatus"
	

		cursor.execute("UPDATE encargo SET idEstatus = %s WHERE idEncargo = %s", (data['estatus'], data['idEncargo']) )
		con.commit()

		return "Estatus cambiado exitosamente (cambiar esto)"

class solicitudesPorDespachar(Resource):
	def get(self):

		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute("SELECT * FROM view_solicitudes_por_despachar ")

		encargos = cursor.fetchall()
		print(encargos)

		#Tengo que convertirlo a json, darle a todos las filas una clave (clave-valor)
		return json.dumps(encargos)




class getPDF(Resource):
	def get(self):

		rendered = render_template('pdf_template.html', name="Greg", location="Venezuela")
		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		responde.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

		return response


class Productos(Resource):
	def get(self, idP):

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("SELECT * FROM producto WHERE idProducto=%s", (idP))
		producto = cursor.fetchone()

		if(producto != None): return dict(id=producto[0], nombre=producto[1], descripcion=producto[2], foto=producto[3], precio=producto[4], cantVendida=producto[5], idCategoria=producto[6])

		return errors['ProductoNotFound'], 404

class ProductosList(Resource):
	def get(self):
		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("SELECT * FROM producto")
		data = cursor.fetchall()

		return ([dict(id=producto[0], nombre=producto[1], descripcion=producto[2], foto=producto[3], precio=producto[4], cantVendida=producto[5], idCategoria=producto[6]) for producto in data])

	def post(self):
		producto = request.get_json()

		con = mysql.connect()
		cursor = con.cursor()

		if ('nombre' not in producto) or ('precio' not in producto):
			return errors['ErrorPeticion'], 400

		cursor.execute("SELECT COUNT(*) FROM producto")
		data = cursor.fetchone()
		producto['idProducto'] = int(data[0]) + 1;

		if ('foto') not in producto:
			producto['foto'] = None
		if ('cantVendida') not in producto:
			producto['cantVendida'] = 0
		if ('idCategoria') not in producto:
			producto['idCategoria'] = None
		if ('descripcion') not in producto:
			producto['descripcion'] = None


		cursor.execute("INSERT INTO producto VALUES (%s,%s,%s,%s,%s,%s,%s)", (producto['idProducto'], producto['nombre'], producto['descripcion'], producto['foto'], producto['precio'], producto['cantVendida'], producto['idCategoria']))
		con.commit()

		return success['ProductoAgregado'], 200

	def put(self):
		producto = request.get_json()

		con = mysql.connect()
		cursor = con.cursor()

		if ('idProducto' not in producto):
			return errors['ErrorPeticion'], 400

		cursor.execute("SELECT * from producto WHERE idProducto=%s", (producto['idProducto']))
		hay_producto = cursor.fetchone()

		if(hay_producto == None): return errors['ProductoNotFound'], 404

		if('nombre' not in producto or producto['nombre'] == None): producto['nombre'] = hay_producto[1]
		if('descripcion' not in producto or producto['descripcion'] == None): producto['descripcion'] = hay_producto[2]
		if('foto' not in producto or producto['foto'] == None): producto['foto'] = hay_producto[3]
		if('precio' not in producto or producto['precio'] == None): producto['precio'] = hay_producto[4]	
		if('cantVendida' not in producto or producto['cantVendida'] == None): producto['cantVendida'] = hay_producto[5]	
		if('idCategoria' not in producto or producto['idCategoria'] == None): producto['idCategoria'] = hay_producto[6]	


		cursor.execute("UPDATE producto SET idProducto=%s, nombre=%s, descripcion=%s, foto=%s, precio=%s, cantVendida=%s, idCategoria=%s WHERE idProducto=%s", (producto['idProducto'], producto['nombre'], producto['descripcion'], producto['foto'], producto['precio'], producto['cantVendida'], producto['idCategoria'], producto['idProducto']))
		con.commit()

		return success['ProductoEditado'], 200

class InfoUser(Resource):
	def get(self):

		usuario = request.headers.get('access_token')
		con = mysql.connect()
		cursor = con.cursor()

		if(usuario != None): 
			try:
				decod = jwt.decode(usuario, 'secret')
			except jwt.InvalidTokenError:
				return errors['ErrorAlDecodificar'], 412
			cursor.execute("SELECT * FROM cliente WHERE email=%s", (decod['sub']))
			data = cursor.fetchone()
			return dict(nombre=data[1], apellido=data[2], fotoPerfil=data[5], fechaNacimiento=data[6], genero=data[7], telefono=data[8], ciudad=data[9])
		return errors['RecursoNoExistente'], 404



api.add_resource(Register, '/registro')
api.add_resource(Login, '/login')
api.add_resource(consultarTarifa, '/consultarTarifa/<string:codPostal>/<float:peso>')
api.add_resource(solicitarDistribucion, '/solicitarDistribucion')
api.add_resource(actualizarEstadoSolicitud, '/estado-solicitud')
api.add_resource(solicitudesPorDespachar, '/solicitudes-por-despachar')
#solicitudes despachas es igual a "por despachar"

# api.add_resource(getPDF, '/pdf')



#DUDAS
# 1) Solicitudes recibidas del comercio?


api.add_resource(Productos, '/productos/<string:idP>', endpoint='prod_ep')
api.add_resource(ProductosList, '/productos')
api.add_resource(InfoUser, '/usuario')


@app.route('/pdf')
def pdf_template():

	# path_wkthmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
	# path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
	# path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\pin\wkhtmltopdf.exe'
	# config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	pdfkit.from_string('Hello!', False)
	# rendered = render_template('pdf_template.html', name="Greg", location="Venezuela")
	# pdf = pdfkit.from_string(rendered, False)

	# response = make_response(pdf)
	# responde.headers['Content-Type'] = 'application/pdf'
	# response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
	# return "hola"
	return response

if __name__ == '__main__':
	app.run(threaded=True,debug=True)



# {
#   "cedula": "24635907",
#   "nombre": "Jose Gregorio Castro",
#   "telefono": "04140179052",
#   "correo": "josegregorio994@gmail.com",
#   "direccion": "Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27",
#   "codPostal": "1060",
#   "peso": 3.5
# }


#Tomar en cuenta el numero de guia, para seguir el estado del paquete...


#Solicitudes por despachar
# {
#   "estatus": 1,
#   "idEncargo": 2
# }