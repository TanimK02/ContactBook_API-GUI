from flask import Flask
import psycopg2
from flask_smorest import Api
from resources.contacts import blp

PASSWORD = ""

app = Flask(__name__)


conn = psycopg2.connect(host = 'localhost', dbname = 'contact_book', user = "postgres",
                         password = PASSWORD, port = 5432)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(
    id SERIAL PRIMARY KEY,
    FirstName VARCHAR(20),
    LastName VARCHAR(20),
    PhoneNumber INT,
    Email VARCHAR(255)
);""")

conn.commit()
cursor.close()
conn.close()

app.config["PROPOGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Contact Book Api"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"

api = Api(app)

api.register_blueprint(blp)