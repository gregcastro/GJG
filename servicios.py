# encoding=utf-8
# -*- coding: utf-8 -*-
import configuracion
from flask import Flask, request, json, make_response, render_template, json, flash, redirect, url_for, session
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime, date, time, timedelta
from random import choice
import jwt, calendar, hashlib, time, re, pdfkit
from flaskext.mysql import MySQL
import requests, random

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
    },
    'ErrorToken': {
        'error': "Se requiere un token de autenticación",
        'status': 400,
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
    ,
    'SolicitudDistribucionExitosa':{
    	'message': "Solicitud de distribución realizada exitosamente",
    	'status' : 200,
    }
}

app = configuracion.app_conf()
api = Api(app, errors=errors)
mysql = MySQL()
mysql.init_app(app)


url = 'http://localhost:5000'
headers = {'content-type': 'application/json'}

#===== Index y Login =====#
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

@app.route('/login_admin', methods=['POST'])
def login_admin():

	hashinput_password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest() 

	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("SELECT * FROM administrador WHERE correo=%s AND clave=%s", (request.form['correo'], hashinput_password))
	admin = cursor.fetchone()

	if (admin == None):
		return render_template("index.html", error=errors['ErrorLogin']['error'])
	else:
		session['logged_in'] = 'admin'
		return render_template("index.html", admin=request.form['correo'])
	



#===== Logout (Cerrar Sesión) =====#
@app.route('/cerrar_sesion', methods=['GET'])
def cerrar_sesion():
	if(session.get('logged_in')): 
		session.pop('logged_in', None)
		return redirect(url_for('index'))

#===== Signup (Registro) =====#
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


#===== Cliente o Adminstrador =====#
@app.route('/consulta-tarifa')
def consultar_tarifa():
	if(session.get('logged_in')):

		print(session.get('logged_in'))

		if session.get('logged_in') == 'admin':
			return render_template("tarifa.html", admin=session.get('logged_in'))
		else:
			return render_template("tarifa.html", current_user=session.get('logged_in'))

	return render_template("index.html")




#===== Fin Cliente o Adminstrador =====#


#===== Cliente Común =====#
@app.route('/gestion-solicitud-cliente')
def gestionar_solicitud_cliente():
	return render_template("index.html")

#===== Fin Cliente Común =====#

#===== Adminstrador =====#
@app.route('/gestion-solicitud-admin')
def gestionar_solicitud_admin():
	if(session.get('logged_in')):
		return render_template("gestion_solicitud.html", admin=session.get('logged_in'))
	return render_template("index.html")

@app.route('/solicitudes-admin')
def get_solicitudes_admin():
	if(session.get('logged_in')):

		desde = str(request.args['desde'])
		hasta = str(request.args['hasta'])
		estatus = str(request.args['tipo'])

		print( estatus )

		# fecha = new Date( request.args['desde'] )
		# print ('fecha = ', fecha)

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("SELECT * FROM view_solicitudes WHERE estatus=%s AND fechaCompra BETWEEN %s AND %s ", (estatus, desde, hasta) )
		solicitudes = cursor.fetchall()
		data = json.dumps(solicitudes)

		return '{}'.format(data)
	return render_template("index.html")


@app.route('/editar-solicitud', methods=['POST'])
def editar_solicitud():
	if(session.get('logged_in')):

		idEstado = request.form['estado']
		tracking = int(request.form['tracking'])

		print (idEstado)
		print( tracking )


		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("UPDATE encargo SET idEstatus = %s WHERE tracking = %s ", (idEstado, tracking) )
		con.commit()

		return render_template("gestion_solicitud.html", actualizado='Actualización de solicitud exitosa')
	return render_template("index.html")




@app.route('/reportes')
def generar_reporte():
	return render_template("index.html")

#===== Fin Adminstrador =====#





#No se si uso esto...
#Funcion seleccionar que muestra la ventana luego del logueo
@app.route('/seleccion')
def seleccionar():
	return selec_funct(session)

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





class Register(Resource):
	#FALTA
	# 1. Expresion regular de que el rif solo sea un numero de 8 u 9 digitos, en caso de ser 8 se coloca un 0 a la izquierda.
	# 2. Expresion regular de que el codPostal sea un numero de 4 digitos.
	# 3. Evaluar si hay tiempo de crear mensajes personalizados para cada error de peticion.
	# 4. Validar que el RIF sea unico
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
		if ('correo' not in data) or ('cedula' not in data) or ('nombre' not in data) or ('telefono' not in data) or ('direccion' not in data) or \
		('codPostal' not in data) or ('peso' not in data):
			return errors['ErrorPeticion'], 400

		codPostal = int(data['codPostal'])
		if (codPostal >= 1000 and codPostal < 9000):

			con = mysql.connect()
			cursor = con.cursor()

			#Obtengo el token de acceso, con el token busco al cliente y de ahi obtengo el idCliente para asociarlo al encargo
			usuario = request.headers.get('access_token')
			if(usuario == None): return errors['ErrorToken'], 400
			else:
				try:
					decod = jwt.decode(usuario, 'secret')
				except jwt.InvalidTokenError:
					return errors['ErrorAlDecodificar'], 412
				cursor.execute("SELECT idCliente, codPostal FROM cliente WHERE correo=%s", (decod['sub']))
				cliente = cursor.fetchone()

				idCliente = cliente[0]
				codPostalCliente = int(cliente[1])

			#Obtengo la fecha y hora actual
			fechaActual = date.today()
			print("fechaActual = ", fechaActual)


			#El precio depende de la distancia entre codPostal y codPostalCliente, el peso, 

			#La fecha depende de la distancia entre codPostal y codPostalCliente

			#Dependiendo del peso del encargo le asigno una categoria (esto se hace antes de calcular el costo OBVIAMENTE)
			cursor.execute("SELECT * FROM categoriaPeso")
			categoriaPeso = cursor.fetchall()
			print("categoriaPeso = ", categoriaPeso)

			peso = data['peso']
			for x in categoriaPeso:
				if (peso >= x[2] and peso <= x[3]):
					idCategoriaPeso = x[0]
					break

			costoBase = 1000.00

			# Multiplico el costo base por el tamano que tenga el producto
			costo = costoBase * int(idCategoriaPeso)


			#Para el random hacer una funcion en donde se le mande el rango de dias q puede salir
			diferencia_cod_postal = abs( codPostal - codPostalCliente )
			
			if diferencia_cod_postal>=0 and diferencia_cod_postal<=1000:
				fechaEstimada = fechaActual + timedelta(days=1)
			elif diferencia_cod_postal>1000 and diferencia_cod_postal<=3000:
				costo += 1000
				#si aun no son las 12pm entonces fechaEstimada es el siguiente dia
				#tomar en cuenta que no se trabaja fines de semana???
				N = random.randint(1, 2)
				fechaEstimada = fechaActual + timedelta(days=N)
			
			elif diferencia_cod_postal>3000 and diferencia_cod_postal<=5000:
				costo += 2000
				#random que sea de 2 a 3 dias o de 3 a 4 dias si ya no son las 12pm
				N = random.randint(2, 4)
				fechaEstimada = fechaActual + timedelta(days=N)
			elif diferencia_cod_postal>5000 and diferencia_cod_postal<=7000:
				costo += 3000
				#random que sea de 4 a 5 dias o de 5 a 6 dias si ya no son las 12pm
				N = random.randint(4, 6)
				fechaEstimada = fechaActual + timedelta(days=N)
			elif diferencia_cod_postal > 7000:
				#random que sea de 6 a 7 dias o de 7 a 8 si ya no son las 12pm
				costo += 4000
				N = random.randint(6, 8)
				fechaEstimada = fechaActual + timedelta(days=N)

			
			#Generacion del tracking number
			longitud = 8
			# valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
			valores = "0123456789"

			tracking = ""
			while True:
		  		tracking = tracking.join([choice(valores) for i in range(longitud)])
		  		cursor.execute("SELECT * FROM encargo WHERE tracking=%s", tracking)
		  		if (cursor.fetchone() == None):
		  			break
			
			print("random = ", tracking)
		
			# fechaEstimada = fechaActual + timedelta(days=3)
			print("fechaEstimada = ", fechaEstimada)

			

			cursor.execute("INSERT INTO direccion (codPostal, dirEnvio) VALUES(%s,%s)", (codPostal, data['direccion']) )
			con.commit()

			cursor.execute("SELECT idDireccion FROM direccion WHERE codPostal=%s AND dirEnvio=%s", (codPostal, data['direccion']))
			idDireccion = cursor.fetchone()[0]
			print("idDireccion = ", idDireccion)

			#El producto me lo tiene que mandar el cliente, pero esa logica no la coloco... simplemente invento que lo tengo o no lo tengo y el administrador coloca en la pagina que ya llego

			#Supongo que aqui siempre comenzara por 1, luego hay que simular los otros estatus 
			idEstatus = 1

			cursor.execute("INSERT INTO encargo (cedula, nombre, telefono, correo, peso, fechaCompra, fechaEstimada, costo, tracking, idDireccion, idEstatus, idCliente, " +
						   "idCategoriaPeso) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ( data['cedula'], data['nombre'], data['telefono'], data['correo'], data['peso'], fechaActual, fechaEstimada, costo, tracking, idDireccion, idEstatus, idCliente, idCategoriaPeso  ) )
			con.commit()

				
			#Esto deberia retornar el tracking
			success['SolicitudDistribucionExitosa']['costo'] = costo
			success['SolicitudDistribucionExitosa']['tracking_number'] = tracking
			success['SolicitudDistribucionExitosa']['fechaEstimada'] = str(fechaEstimada)
			return success['SolicitudDistribucionExitosa'], 200

		errors['ErrorPeticion']['message'] = "Código postal incorrecto"
		return errors['ErrorPeticion'], 400


	


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

###
class getPDF(Resource):
	def get(self):

		rendered = render_template('pdf_template.html', name="Greg", location="Venezuela")
		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		responde.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

		return response
###

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