from flask import Flask
import pyodbc, os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello():
     
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    # server = 'tcp:mytest.centralus.cloudapp.azure.com' 
    # database = 'test' 
    # username = 'ndb' 
    # password = 'test1789###' 

     server = os.environ.get("DB_SERVER")
     database = os.environ.get("DB_NAME")
     username = os.environ.get("DB_USER")
     password = os.environ.get("DB_PASS")

     cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
     cursor = cnxn.cursor()
     cursor.execute('SELECT * FROM [SalesLT].[vGetAllCategories]')
     s = ' '
     for row in cursor:
         s += ''.join(str(row))
         s += '<hr>'
         print(row)
     #s = '!! Azure'
     return s
