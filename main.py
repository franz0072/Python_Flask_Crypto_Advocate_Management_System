from flask import Flask
from public import public
from admin import admin
from advocate import advocate
from api import api
from clerk import clerk

app=Flask(__name__)

app.secret_key="secret_key"

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(advocate,url_prefix="/advocate")
app.register_blueprint(api,url_prefix="/api")
app.register_blueprint(clerk,url_prefix="/clerk")

app.run(debug=True,port=5115,host='0.0.0.0')