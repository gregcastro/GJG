from flask import Flask

def app_conf():
	app = Flask(__name__)
	app.config['MYSQL_DATABASE_USER'] = 'root'
	# app.config['MYSQL_DATABASE_PASSWORD'] = '123'
	app.config['MYSQL_DATABASE_PASSWORD'] = ''
	app.config['MYSQL_DATABASE_DB'] = 'gjg'
	app.config['MYSQL_DATABASE_HOST'] = 'localhost'
	app.secret_key = "Estodeberiaserandom"
	return app