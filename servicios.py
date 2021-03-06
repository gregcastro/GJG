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
        'error': "Error en la petición",
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
        'message': "Usuario registrado con éxito",
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



#=========== POR HACER =============#

# WB consultarTarifa()

# API REST

# HOSTING

# Comunicacion grupos

#=========== POR HACER =============#



#===== Index y Login =====#
@app.route('/', methods=['GET','POST'])
def index():
	# Si tengo token en el local storage estoy logeado, sino no
	# Realizar pruebas en el token para ver si funciona lo del tiempo de vencimiento.
	if(request.method == 'GET'): 
		if(session.get('logged_in')):
			if session.get('logged_in') == 'admin':
				return render_template("index.html", admin=session.get('logged_in'))
			return render_template("index.html", current_user=session.get('logged_in'))
		return render_template("index.html")
	else:
		data = {"correo" : request.form['correo'], "clave" : request.form['password'] }
		# print(data)
		r = requests.post(url+'/login', json.dumps(data), headers=headers)
		response = r.json()
		
		if response['status'] == 200:

			session['logged_in'] = response['access_token']
			con = mysql.connect()
			cursor = con.cursor()
			cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), request.form['correo'], 'Nuevo inicio de sesión') )
			con.commit()
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
		cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), request.form['correo'], 'Nuevo inicio de sesión') )
		con.commit()
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

				con = mysql.connect()
				cursor = con.cursor()
				cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), request.form['correo'], 'Nuevo Registro de Usuario') )
				con.commit()
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
	if(session.get('logged_in') and session.get('logged_in')!='admin' ):

		return render_template("gestion_solicitud.html", current_user=session.get('logged_in'), tipo_user='normal')

	return render_template("index.html")


@app.route('/solicitudes')
def get_solicitudes():
	if(session.get('logged_in') and session.get('logged_in') != 'admin'):

		desde = str(request.args['desde'])
		hasta = str(request.args['hasta'])
		estatus = str(request.args['tipo'])

		print( estatus )
		print(desde)
		print(hasta)

		con = mysql.connect()
		cursor = con.cursor()

		# Busco el idCliente del usuario de esta sesion
		try:
			decod = jwt.decode(session.get('logged_in'), 'secret')
		except jwt.InvalidTokenError:
			return errors['ErrorAlDecodificar'], 412

		print(decod['sub'])

		cursor.execute("SELECT idCliente FROM cliente WHERE correo=%s", (decod['sub']))
		idCliente = cursor.fetchone()
		idCliente = idCliente[0]


		if estatus == "":
			cursor.execute("SELECT * FROM view_solicitudes WHERE fechaCompra BETWEEN %s AND %s AND idCliente=%s", (desde, hasta, idCliente) )
		else:
			cursor.execute("SELECT * FROM view_solicitudes WHERE estatus=%s AND fechaCompra BETWEEN %s AND %s AND idCliente=%s", (estatus, desde, hasta, idCliente) )

		solicitudes = cursor.fetchall()
		print(solicitudes)
		data = json.dumps(solicitudes)

		descripcion = 'Realizó una búsqueda de solicitudes entre ' + desde + ' y ' + hasta
		cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), decod['sub'], descripcion) )
		con.commit()

		return '{}'.format(data)
	return render_template("index.html")
#===== Fin Cliente Común =====#




#===== Administrador =====#
@app.route('/rastrear_tracking')
def rastrear_tracking():
	tracking = request.args['tracking']
	con = mysql.connect()
	cursor = con.cursor()

	if(session.get('logged_in') == 'admin'):
		tracking = request.args['tracking']

		cursor.execute("SELECT * FROM encargo WHERE tracking=%s ", tracking )
		encargo = cursor.fetchall()

		data = json.dumps(encargo)

		descripcion = 'Rastreó el número de orden ' + tracking
		cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), 'Administrador', descripcion) )
		con.commit()

		return '{}'.format(data)

	elif (session.get('logged_in')):
		cursor.execute("SELECT idEncargo FROM encargo WHERE tracking=%s ", tracking )
		idEncargo = cursor.fetchone()
		data = []
		if idEncargo != None:
			idEncargo = idEncargo[0]

			try:
				decod = jwt.decode(session.get('logged_in'), 'secret')
			except jwt.InvalidTokenError:
				return errors['ErrorAlDecodificar'], 412

			print(decod['sub'])

			cursor.execute("SELECT idCliente FROM cliente WHERE correo=%s", (decod['sub']))
			idCliente = cursor.fetchone()
			idCliente = idCliente[0]

			cursor.execute("SELECT * FROM view_historial_paquete WHERE idCliente=%s AND idEncargo=%s", (idCliente, idEncargo) )
			historial = cursor.fetchall()

			print(historial)

			data = json.dumps(historial)

			descripcion = 'Rastreó el número de orden ' + tracking
			cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), decod['sub'], descripcion) )
			con.commit()

		return '{}'.format(data)


	return render_template("index.html")


@app.route('/gestion-solicitud-admin')
def gestionar_solicitud_admin():
	if(session.get('logged_in') and session.get('logged_in')=='admin'):
		if 'actualizado' in request.args:
			actualizado = request.args['actualizado']
			return render_template("gestion_solicitud.html", admin=session.get('logged_in'), actualizado=actualizado,tipo_user='admin')

		return render_template("gestion_solicitud.html", admin=session.get('logged_in'), tipo_user='admin')
	return render_template("index.html")


@app.route('/solicitudes-admin')
def get_solicitudes_admin():
	if(session.get('logged_in') and session.get('logged_in')=='admin'):

		desde = str(request.args['desde'])
		hasta = str(request.args['hasta'])
		estatus = str(request.args['tipo'])

		print( estatus )
		print(desde)
		print(hasta)

		# fecha = new Date( request.args['desde'] )
		# print ('fecha = ', fecha)

		con = mysql.connect()
		cursor = con.cursor()
		if estatus == "":
			cursor.execute("SELECT * FROM view_solicitudes WHERE fechaCompra BETWEEN %s AND %s ", (desde, hasta) )
		else:
			cursor.execute("SELECT * FROM view_solicitudes WHERE estatus=%s AND fechaCompra BETWEEN %s AND %s ", (estatus, desde, hasta) )
		
		solicitudes = cursor.fetchall()
		print(solicitudes)
		data = json.dumps(solicitudes)

		descripcion = 'Realizó una búsqueda de solicitudes entre ' + desde + ' y ' + hasta
		cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), 'Administrador', descripcion) )
		con.commit()

		return '{}'.format(data)
	return render_template("index.html")


@app.route('/get-logs')
def get_logs_admin():
	if(session.get('logged_in') and session.get('logged_in')=='admin'):

		desde = str(request.args['desde'])
		hasta = str(request.args['hasta'])

		print(desde)
		print(hasta)

		# fecha = new Date( request.args['desde'] )
		# print ('fecha = ', fecha)

		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute("SELECT * FROM auditoria WHERE fecha BETWEEN %s AND %s ", (desde, hasta) )		
		
		logs = cursor.fetchall()
		print(logs)
		data = json.dumps(logs)

		return '{}'.format(data)
	return render_template("index.html")


@app.route('/estatusEncargo')
def get_estatus_encargo():
	if(session.get('logged_in') and session.get('logged_in')=='admin'):

		tracking = request.args['tracking']

		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute("SELECT idEstatus FROM encargo WHERE tracking=%s ", tracking )
		
		data = cursor.fetchone()

		data = data[0]
		data = json.dumps(data)


		return '{}'.format(data)
	return render_template("index.html")


@app.route('/editar-solicitud', methods=['POST'])
def editar_solicitud():

	if(session.get('logged_in') and session.get('logged_in')=='admin'):
		# Obtengo parametros del form
		idEstado = request.form['estado']
		tracking = int(request.form['tracking'])
		fecha = request.form['fecha']

		con = mysql.connect()
		cursor = con.cursor()

		# Busco el idEncargo perteneciente al encargo que se esta editando
		cursor.execute("SELECT idEncargo FROM encargo WHERE tracking=%s ", tracking )
		idEncargo = cursor.fetchone()
		idEncargo = idEncargo[0]

		# Si el estatus no es ENTREGADO entonces realizo una insercion en el historial de donde se encuentra el paquete
		if idEstado != '4':
			locacion = request.form['locacion']
			# Inserto en historial la locacion y fecha correspondiente
			cursor.execute("INSERT INTO historial (fecha, locacion, idEncargo) VALUES(%s,%s,%s)", (fecha, locacion, idEncargo) )
			descripcion = 'Actualizó la solicitud con el número de orden ' + tracking + ' con el estatus ' + idEstado + ' en la locación ' + locacion
		
		if idEstado == '4':
			cursor.execute("INSERT INTO historial (fecha, locacion, idEncargo) VALUES(%s,%s,%s)", (fecha, "Producto Entregado", idEncargo) )
			descripcion = 'Se entregó la solicitud con el número de orden ' + tracking
		
		# Se actualiza el estado del encargo
		cursor.execute("UPDATE encargo SET idEstatus = %s WHERE tracking = %s ", (idEstado, tracking) )
		
		cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), 'Administrador', descripcion) )

		con.commit()



		return redirect(url_for('gestionar_solicitud_admin', actualizado=1) )
		# return render_template("gestion_solicitud.html", actualizado=1, admin=session.get('logged_in') )
	return render_template("index.html")


@app.route('/reportes')
def generar_reporte():
	if(session.get('logged_in') and session.get('logged_in')=='admin'):
		return render_template("reportes.html", admin=session.get('logged_in'))
	return render_template("index.html")


@app.route('/pdf_generate', methods=['POST'])
def pdf_generate():
	solicitud = request.form['solicitud']
	real_solicitud = request.form['solicitud']
	fecha1 = request.form['desde']
	fecha2 = request.form['hasta']

	print(fecha1)
	print(fecha2)
	
	con = mysql.connect()
	cursor = con.cursor()

	if solicitud == "Solicitudes Despachadas":

		tipo_fecha = request.form['tipo_fecha']

		if tipo_fecha == 'Día':
			cursor.execute("SELECT * FROM view_solicitudes WHERE estatus!=%s AND fechaCompra=%s ", ("POR PROCESAR", fecha1) )
		else:
			cursor.execute("SELECT * FROM view_solicitudes WHERE estatus!=%s AND fechaCompra BETWEEN %s AND %s ", ("POR PROCESAR", fecha1, fecha2) )
		
		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Solicitudes Despachadas</title>
					<meta name="pdfkit-page-size" content="Legal"/>
					<meta name="pdfkit-orientation" content="Landscape"/>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Solicitudes Despachadas</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th># Orden</th>
				    <th>Enviado a</th>
				    <th>Comercio</th>
				    <th>Costo</th>
				    <th>Fecha de Compra</th>
				    <th>Fecha Estimada</th>
				    <th>Estado</th>
				    <th>Dirección</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + solicitud[0] + """ </td> """
			body += """<td>""" + solicitud[1] + """ </td> """
			body += """<td>""" + solicitud[2] + """ </td> """
			body += """<td>""" + str(solicitud[3]) + """ </td> """
			body += """<td>""" + str(solicitud[4]) + """ </td> """
			body += """<td>""" + str(solicitud[5]) + """ </td> """
			body += """<td>""" + str(solicitud[6]) + """ </td> """
			body += """<td>""" + solicitud[7] + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)

	elif solicitud == "Solicitudes Pendientes":
		tipo_fecha = request.form['tipo_fecha']
		if tipo_fecha == 'Día':
			cursor.execute("SELECT * FROM view_solicitudes WHERE estatus=%s AND fechaCompra=%s ", ("POR PROCESAR", fecha1) )
		else:
			cursor.execute("SELECT * FROM view_solicitudes WHERE estatus=%s AND fechaCompra BETWEEN %s AND %s ", ("POR PROCESAR", fecha1, fecha2) )
		

		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Solicitudes Pendientes</title>
					<meta name="pdfkit-page-size" content="Legal"/>
					<meta name="pdfkit-orientation" content="Landscape"/>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Solicitudes Pendientes</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th># Orden</th>
				    <th>Enviado a</th>
				    <th>Comercio</th>
				    <th>Costo</th>
				    <th>Fecha de Compra</th>
				    <th>Fecha Estimada</th>
				    <th>Estado</th>
				    <th>Dirección</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + solicitud[0] + """ </td> """
			body += """<td>""" + solicitud[1] + """ </td> """
			body += """<td>""" + solicitud[2] + """ </td> """
			body += """<td>""" + str(solicitud[3]) + """ </td> """
			body += """<td>""" + str(solicitud[4]) + """ </td> """
			body += """<td>""" + str(solicitud[5]) + """ </td> """
			body += """<td>""" + str(solicitud[6]) + """ </td> """
			body += """<td>""" + solicitud[7] + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)

	elif solicitud == "Clientes":
		cursor.execute("SELECT * FROM view_clientes")
		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Clientes</title>
					<meta name="pdfkit-page-size" content="Legal"/>
					<meta name="pdfkit-orientation" content="Landscape"/>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Clientes</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th>Nombre</th>
				    <th>Email</th>
				    <th>RIF</th>
				    <th>Código Postal</th>
				    <th>Cantidad de Solicitudes</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + solicitud[0] + """ </td> """
			body += """<td>""" + solicitud[1] + """ </td> """
			body += """<td>J-""" + str(solicitud[2]) + """ </td> """
			body += """<td>""" + str(solicitud[3]) + """ </td> """
			body += """<td>""" + str(solicitud[4]) + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)

	elif solicitud == "Destinos":
		cursor.execute("SELECT * FROM view_destinos ")
		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Destinos</title>
					<meta name="pdfkit-page-size" content="Legal"/>
					<meta name="pdfkit-orientation" content="Landscape"/>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Destinos</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th>Código Postal</th>
				    <th>Dirección de Envío</th>
				    <th>Cantidad de Solicitudes</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + str(solicitud[0]) + """ </td> """
			body += """<td>""" + solicitud[1] + """ </td> """
			body += """<td>""" + str(solicitud[2]) + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)

	elif solicitud == "Facturas Canceladas":
		cursor.execute("SELECT * FROM view_facturas_cancelacion ")
		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Facturas Canceladas</title>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Facturas Canceladas</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th>Fecha de Cancelación</th>
				    <th>Fecha de Vencimiento</th>
				    <th>Monto</th>
				    <th>Comercio</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + str(solicitud[0]) + """ </td> """
			body += """<td>""" + str(solicitud[1]) + """ </td> """
			body += """<td>""" + str(solicitud[2]) + """ </td> """
			body += """<td>""" + solicitud[3] + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)

	elif solicitud == "Facturas Vigentes":
		cursor.execute("SELECT * FROM view_facturas_vigentes ")
		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Facturas Vigentes</title>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Facturas Vigentes</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th>Fecha de Vencimiento</th>
				    <th>Monto</th>
				    <th>Comercio</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + str(solicitud[0]) + """ </td> """
			body += """<td>""" + str(solicitud[1]) + """ </td> """
			body += """<td>""" + solicitud[2] + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)

	elif solicitud == "Facturas Vencidas":
		cursor.execute("SELECT * FROM view_facturas_vencidas ")
		solicitudes = cursor.fetchall()

		body = """
				<!DOCTYPE html>
				<html>
				<style>

					table {
					    border-collapse: collapse;
					    width: 100%;					    
					}

					td, th {
					    border: 1px solid #dddddd;
					    padding: 15px;
					}

					th {
						text-align: center;
					}

					tr:nth-child(even) {
					    background-color: #dddddd;
					}

				</style>
				<head>
					<img src="https://preview.ibb.co/fKfW3F/gjg.png">
					<title>Facturas Vencidas</title>
					<meta charset="utf-8">
				</head>
				<body>
				<center> <h2>Facturas Vencidas</h2> </center>
		    	<table width="100%">
				  <tr>
				    <th>Fecha de Vencimiento</th>
				    <th>Monto</th>
				    <th>Comercio</th>
				  </tr>
		"""
		for solicitud in solicitudes:
			body += """ <tr style="text-align:center;"> <td>""" + str(solicitud[0]) + """ </td> """
			body += """<td>""" + str(solicitud[1]) + """ </td> """
			body += """<td>""" + solicitud[2] + """ </td> """


		body += """</tr> </table> </body> </html>"""

		pdf = pdfkit.from_string(body, False)


	descripcion = 'Se generó un PDF para las solicitudes de ' + real_solicitud
	cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), 'Administrador', descripcion) )
	con.commit()


	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; filename=reporte.pdf'

	return response


@app.route('/logs')
def gestion_logs():
	if(session.get('logged_in') and session.get('logged_in')=='admin'):
		return render_template("logs.html", admin=session.get('logged_in'))
	return render_template("index.html")

#===== Fin Adminstrador =====#




#===== API =====#
codPostalOrigen = 1060;

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
				
			fechaVencimientoFactura = fechaActual + timedelta(days=15)
			cursor.execute("INSERT INTO factura (fechaVencimiento, monto, idCliente, idEstadoFactura, idEncargo)" + 
						   "VALUES (%s,%s,%s,%s,%s)", (fechaVencimientoFactura, costo, idCliente, 1, con.insert_id()) )


			descripcion = 'Se solicitó un servicio de distribución con los siguientes datos: cédula: ' + data['cedula'] + ' nombre: ' + data['nombre'] + ' teléfono: ' + data['telefono'] + ' correo: ' + data['correo'] + ' peso: ' + str(data['peso']) + ' costo: ' + str(costo) +' número de orden: ' + tracking
			cursor.execute("INSERT INTO auditoria (fecha, usuario, descripcion) VALUES(%s,%s,%s)", (date.today(), decod['sub'], descripcion) )

			con.commit()

				
			#Esto deberia retornar el tracking
			success['SolicitudDistribucionExitosa']['costo'] = costo
			success['SolicitudDistribucionExitosa']['tracking_number'] = tracking
			success['SolicitudDistribucionExitosa']['fechaEstimada'] = str(fechaEstimada)
			return success['SolicitudDistribucionExitosa'], 200

		errors['ErrorPeticion']['message'] = "Código postal incorrecto"
		return errors['ErrorPeticion'], 400


	



api.add_resource(Register, '/registro')
api.add_resource(Login, '/login')
api.add_resource(consultarTarifa, '/consultarTarifa/<string:codPostal>/<float:peso>')
api.add_resource(solicitarDistribucion, '/solicitarDistribucion')


# @app.route('/pdf')
# def pdf_template():

	# path_wkthmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
	# path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
	# path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\pin\wkhtmltopdf.exe'
	# config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	# pdfkit.from_string('Hello!', False)
	# rendered = render_template('pdf_template.html', name="Greg", location="Venezuela")
	# pdf = pdfkit.from_string(rendered, False)

	# response = make_response(pdf)
	# responde.headers['Content-Type'] = 'application/pdf'
	# response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
	# return "hola"
	# return response

if __name__ == '__main__':
	app.run(threaded=True,debug=True)
	# app.run(threaded=True,debug=True, host='192.168.1.109', port=3000)



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