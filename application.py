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

def index():
    # Execute the SQL query and fetch the results
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP (1000) * FROM [SalesLT].[vGetAllCategories]")
    rows = cursor.fetchall()
    # Render the results in an HTML table format
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run()
