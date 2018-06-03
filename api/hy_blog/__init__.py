from flask import Flask

def creat_app(config_filename):
	app = Flask(__name__)
	app.config.from_pyfile(config_filename)

	from view import views
	for a_view in views:
		app.register_blueprint(a_view)
	
	return app 
