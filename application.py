from flask import Flask, render_template
import pyodbc, os, time

app = Flask(__name__)
app.config["DEBUG"] = True

# Set up the database connection
server = os.environ.get("DB_SERVER")
database = os.environ.get("DB_NAME")
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")
driver= "{ODBC Driver 18 for SQL Server}"
cnxn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")

# Define the route for the web page
@app.route("/")
def PythonRetryLogicConnectToTheDB():
    try:
        nTimes=0
        while nTimes <5:
                nTimes=nTimes+1
                print("Connecting to the DB - Attempt Number: %i " % nTimes)
                start_time = time.time()    
                conn = ConnectToTheDB()
                if( conn != None ):
                    print("Connected to the Database %s seconds ---" % ((time.time() - start_time)) )
                    return conn    
                else:
                  print("------ Next Attempt ----- Waiting for 5 seconds ---")       
                  time.sleep(5)     
        return 
    except Exception as e:
        print("An error occurred connecting to the DB - " + format(e))
        return
        
def ConnectToTheDB():
    try:
        return pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};timeout=30");  
    except Exception as e:
        print("An error occurred connecting to the DB - " + format(e))
        return 

def index():
    # Execute the SQL query and fetch the results
    cnxn = PythonRetryLogicConnectToTheDB()
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP (1000) * FROM [SalesLT].[vGetAllCategories]")
    rows = cursor.fetchall()
    # Render the results in an HTML table format
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run()
