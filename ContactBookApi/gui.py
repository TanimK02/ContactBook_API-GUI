from typing import Any, Optional, Tuple, Union
from customtkinter import *
from PIL import Image
import subprocess
import signal
import requests
from functools import partial
import json

URL = 'http://127.0.0.1:5000/contacts'

class connection_level(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x200")
        self.maxsize(200,200)
        self.title("Connect to DB")
        self.img_logo = Image.open("IMG_0123.jpeg")
        self.image = CTkImage(dark_image=self.img_logo, size=(200,200))
        self.logo = CTkLabel(self, image=self.image, text=None)
        self.logo.grid(column = 0, row = 0)
        self.connect = CTkButton(self, command=self.begin_connection, text = "Connect", fg_color="Green", corner_radius=20, bg_color= "#d2dce4")
        self.connect.grid(row = 0, column = 0)
        
    def begin_connection(self):
        self.process = subprocess.Popen(["flask", "run"])
        self.withdraw()


class method_frame(CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_contacts = CTkButton(self, text = "Contacts")
        self.get_contacts.grid(column = 0, row =0, padx = 20, pady = 20)
        self.make_contact = CTkButton(self, text = "Create Contact", command=self.post)
        self.make_contact.grid(column = 0, row =1, padx = 20, pady = 20)
        self.update_contact = CTkButton(self, text = "Update Contact", command=self.put)
        self.update_contact.grid(column = 0, row =2, padx = 20, pady = 20)
        self.delete_contact = CTkButton(self, text = "Delete Contact", command=self.delete)
        self.delete_contact.grid(column = 0, row =3, padx = 20, pady = 20)
        self.delete_contact = CTkButton(self, text = "Reset Contacts", command=self.reset)
        self.delete_contact.grid(column = 0, row =4, padx = 20, pady = 20)

    def post(self):
        def confirmed():
            if firstname.get() != "" or lastname.get() != "":
                if firstname.get() != "":
                    f_name = firstname.get()
                else:
                    f_name = None
                if lastname.get() != "":
                    l_name = lastname.get()
                else:
                    l_name = None
                if phonenumber.get() != "":
                    phone = phonenumber.get()
                else:
                    phone = None
                if email.get() != "":
                    mail = email.get()
                else:
                    mail = None
                parameters = {
                    "firstname": f_name,
                    "lastname": l_name,
                    "phonenumber": phone,
                    "email": mail
                }
                requests.post(url=URL, json=parameters)
        query = CTkToplevel(self)
        query.title = "Enter Info"
        firstname = CTkEntry(master = query, placeholder_text="First name", width=300)
        firstname.grid(column = 0, row = 0, pady = 5)
        lastname = CTkEntry(master=query, placeholder_text="Last name", width=300)
        lastname.grid(column = 0, row = 1, pady = 5)
        phonenumber = CTkEntry(master=query, placeholder_text="Phone number", width=300)
        phonenumber.grid(column = 0, row = 2, pady = 5)
        email = CTkEntry(master=query, placeholder_text="Email", width= 300)
        email.grid(column = 0, row = 3, pady = 5)
        confirmation = CTkButton(master=query, text="Confirm", width= 300, command = confirmed)
        confirmation.grid(column= 0, row = 4, pady = 5)
    
    def delete(self):
        def send_delete():
            if firstname.get() != "" or lastname.get() != "":
                if firstname.get() != "":
                    f_name = firstname.get()
                else:
                    f_name = None
                if lastname.get() != "":
                    l_name = lastname.get()
                else:
                    l_name = None
            if f_name and l_name:
                parameters = {
                    "firstname": f_name,
                    "lastname": l_name
                }
            elif f_name and not l_name:
                parameters = {
                    "firstname": f_name
                }
            else:
                parameters = {
                    "lastname": l_name
                }
            requests.delete(url=URL + "/delete-one", json=parameters)
        query2 = CTkToplevel(self)
        query2.title = "Enter Info"
        firstname = CTkEntry(master = query2, placeholder_text="First name", width=300)
        firstname.grid(column = 0, row = 0, pady = 5)
        lastname = CTkEntry(master=query2, placeholder_text="Last name", width=300)
        lastname.grid(column = 0, row = 1, pady = 5)
        confirmation = CTkButton(master=query2, text="Confirm", width= 300, command = send_delete)
        confirmation.grid(column= 0, row = 4, pady = 5)
        
    @staticmethod
    def reset():
        requests.delete(url = URL)

    def put(self):
        def confirmed():
            if firstname.get() != "" or lastname.get() != "":
                if firstname.get() != "":
                    f_name = firstname.get()
                else:
                    f_name = None
                if lastname.get() != "":
                    l_name = lastname.get()
                else:
                    l_name = None
                if phonenumber.get() != "":
                    phone = phonenumber.get()
                else:
                    phone = None
                if email.get() != "":
                    mail = email.get()
                else:
                    mail = None
                parameters = {
                    "firstname": f_name,
                    "lastname": l_name,
                    "phonenumber": phone,
                    "email": mail
                }
                requests.put(url=URL, json=parameters)
        query = CTkToplevel(self)
        query.title = "Enter Info"
        firstname = CTkEntry(master = query, placeholder_text="First name", width=300)
        firstname.grid(column = 0, row = 0, pady = 5)
        lastname = CTkEntry(master=query, placeholder_text="Last name", width=300)
        lastname.grid(column = 0, row = 1, pady = 5)
        phonenumber = CTkEntry(master=query, placeholder_text="Phone number", width=300)
        phonenumber.grid(column = 0, row = 2, pady = 5)
        email = CTkEntry(master=query, placeholder_text="Email", width= 300)
        email.grid(column = 0, row = 3, pady = 5)
        confirmation = CTkButton(master=query, text="Confirm", width= 300, command = confirmed)
        confirmation.grid(column= 0, row = 4, pady = 5)



class contact_scroll(CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contacts = {}
    def get_contacts(self):
        self.contacts = {}
        data = requests.get(url=URL)
        data = data.json()
        for widget in self.winfo_children():
            widget.destroy()
        i = 0
        for key, value in data.items():
            contact = CTkButton(self, text=key)
            contact.configure(command = partial(self.get_info, contact))
            self.contacts[contact] = value
            contact.grid(column = 0, row = i, padx = 30, pady = 5)
            i += 1
    def get_info(self,contact):
        for widget in self.winfo_children():
            widget.destroy()
        i = 0
        for key, value in self.contacts[contact].items():
            info = CTkTextbox(self, width= 300, height=10)
            info.insert("0.0", f"{key}:{value}")
            info.grid(column = 0, row = i, padx = 0, pady = 5, sticky = "W")
            i += 1

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection_level(self)
        self.title("Contact Book")
        self.maxsize(width=650, height = 250)
        self.disconnect = CTkButton(self, text = "Disconnect", fg_color="Dark Red", command = self.disconnect_api)
        self.disconnect.grid(column = 0, row = 0, sticky = "E", padx =20, pady = 20)
        self.method_frame = method_frame(self)
        self.method_frame.grid(column = 2, row = 0, sticky = "E", pady = 20, padx = 20)
        self.contact_scroll = contact_scroll(self)
        self.contact_scroll.grid(column = 1, row = 0, pady = 20)
        self.get_contacts = self.contact_scroll.get_contacts
        self.method_frame.get_contacts.configure(command = self.get_contacts)

    def disconnect_api(self):
        self.connection.process.send_signal(signal.SIGINT)
        self.disconnect.configure(text = "Disconnected", fg_color = "Green")
app = App()
app.mainloop()