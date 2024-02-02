from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
import psycopg2

PASSWORD = ""

blp = Blueprint("contacts", __name__, description = "Operations for the contact book")



@blp.route("/contacts")
class ContactMani(MethodView):
    def get(self):
        conn = psycopg2.connect(host = 'localhost', dbname = 'contact_book', user = "postgres",
                            password = PASSWORD, port = 5432)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts;")
        data = cursor.fetchall()

        data_json = {}
        for i in data:
            first_name = i[1]
            last_name = i[2]
            phone_number = i[3]
            email = i[4]
            if first_name and last_name:
                data_json[first_name+" "+last_name] = {"phone_number" : phone_number,
                                                    "email": email}
            elif first_name:
                data_json[first_name] = {"phone_number" : phone_number,
                                                    "email": email}
            elif last_name:
                data_json[last_name] = {"phone_number" : phone_number,
                                                    "email": email}

        sorted_data = sorted(data_json)
        sorted_data = {i:data_json[i] for i in sorted_data}
        conn.close()
        return sorted_data, 200
    
    def post(self):
        # {"firstname": "string",
        #     "lastname": "string",
        #     "phonenumber": "int",
        #     "email": "string"}
        conn = psycopg2.connect(host = 'localhost', dbname = 'contact_book', user = "postgres",
                            password = PASSWORD, port = 5432)
        request_data = request.get_json()
        if not request_data:
            abort(400, message = "Need to fill parameters/ can't use empty JSON")
        if "firstname" not in request_data and "lastname" not in request_data:
            abort(400, message= "First or last name needed")
        columns = request_data.keys()
        place_holders = ["%s"] * len(request_data)
        values = request_data.values()
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO contacts({", ".join(columns)})
                    VALUES({", ".join(place_holders)});""", tuple(values))
        
        conn.commit()
        cursor.close()
        conn.close()
        return request_data, 201
    
    def put(self):
        conn = psycopg2.connect(host = 'localhost', dbname = 'contact_book', user = "postgres",
                            password = PASSWORD, port = 5432)
        data = request.get_json()
        if "firstname" not in data and "lastname" not in data:
            abort(400, message = "missing name")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        verify = []
        for i in contacts:
            if i[1] and i[2]:
                verify.append(i[1] + " " + i[2])
            elif i[1] and not i[2]:
                verify.append(i[1])
            else:
                verify.append(i[2])
        if "firstname" in data and "lastname" in data:
            name = data["firstname"] + " " + data["lastname"]
        elif "firstname" in data and "lastname" not in data:
            name = data["firstname"]
        else:
            name = data["lastname"]
        if name in verify:
            if "firstname" in data and "lastname" in data:
                    cursor.execute(f"""UPDATE contacts
                                SET phonenumber = {data["phonenumber"]}, email = '{data["email"]}'
                                    WHERE firstname = '{data["firstname"]}' and lastname = '{data["lastname"]}'""")
                    conn.commit()
                    cursor.execute(f"""SELECT * FROM contacts WHERE firstname = '{data["firstname"]}' and lastname = '{data["lastname"]}'""")
                    result = cursor.fetchall()
                    result = {i[1] + " " + i[2]:{"phonenumber": i[3], "email": i[4]} for i in result}
                    cursor.close()
                    conn.close()
                    return result, 200
            elif "firstname" in data and "lastname" not in data:
                    cursor.execute(f"""UPDATE contacts
                                SET phonenumber = {data["phonenumber"]}, email = '{data["email"]}'
                                    WHERE firstname = '{data["firstname"]}'""")
                    conn.commit()
                    cursor.execute(f"""SELECT * FROM contacts WHERE firstname = '{data["firstname"]}'""")
                    result = cursor.fetchall()
                    result = {i[1]:{"phonenumber": i[3], "email": i[4]} for i in result}
                    cursor.close()
                    conn.close()
                    return result, 200
            else:
                    cursor.execute(f"""UPDATE contacts
                                SET phonenumber = {data["phonenumber"]}, email = '{data["email"]}'
                                    WHERE lastname = '{data["lastname"]}'""")
                    conn.commit()
                    cursor.execute(f"""SELECT * FROM contacts WHERE lastname = '{data["lastname"]}'""")
                    result = cursor.fetchall()
                    result = {i[2]:{"phonenumber": i[3], "email": i[4]} for i in result}
                    cursor.close()
                    conn.close()
                    return result, 200
        else:
            abort(400, message = "name does not exist")
    
    def delete(self):
        conn = psycopg2.connect(host = 'localhost', dbname = 'contact_book', user = "postgres",
                            password = PASSWORD, port = 5432)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE contacts;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(
        id SERIAL PRIMARY KEY,
        FirstName VARCHAR(20),
        LastName VARCHAR(20),
        PhoneNumber INT,
        Email VARCHAR(255));""")

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Contacts have been reset"}, 410
    

@blp.route("/contacts/delete-one", methods = ["DELETE"])
def delete_one():
    data = request.get_json()
    conn = psycopg2.connect(host = 'localhost', dbname = 'contact_book', user = "postgres",
                         password = PASSWORD, port = 5432)
    cursor = conn.cursor()
    if "firstname" in data and "lastname" in data:
        try:
            cursor.execute(f"""DELETE from contacts WHERE firstname = '{data["firstname"]}' and lastname = '{data["lastname"]}'; """)
        except KeyError:
            cursor.close()
            conn.close()
            abort(400, message = "Name not found")
    elif "firstname" in data and "lastname" not in data:
        try:
            cursor.execute(f"""DELETE from contacts WHERE firstname = '{data["firstname"]}'; """)
        except KeyError:
            cursor.close()
            conn.close()
            abort(400, message = "Name not found")
    elif "lastname" in data and "firstname" not in data:
        try:
            cursor.execute(f"""DELETE from contacts WHERE lastname = '{data["lastname"]}'; """)
        except KeyError:
            cursor.close()
            conn.close()
            abort(400, message = "Name not found")
    else:
        cursor.close()
        conn.close()
        abort(400, message = "Need name")
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Successfully deleted"}, 410

blp.add_url_rule('/contacts', view_func=ContactMani.as_view('contact_mani'))