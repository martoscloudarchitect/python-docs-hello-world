from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)
app.config["DEBUG"] = True
# Set up the database connection
server = os.environ.get("DB_SERVER")
database = os.environ.get("DB_NAME")
username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")
driver= "{ODBC Driver 17 for SQL Server}"
cnxn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")

# Define the route for the web page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Update the edited row in the database
        cursor = cnxn.cursor()
        cursor.execute("UPDATE [SalesLT].[Category] SET Name=?, ParentCategoryID=? WHERE CategoryID=?", request.form["Name"], request.form["ParentCategoryID"], request.form["CategoryID"])
        cnxn.commit()
        return redirect("/")
    else:
        # Execute the SQL query and fetch the results
        cursor = cnxn.cursor()
        cursor.execute("SELECT TOP (1000) * FROM [SalesLT].[vGetAllCategories]")
        rows = cursor.fetchall()

        # Render the results in an HTML table format
        return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run()
