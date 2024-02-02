I made this API using flask, tkinter, psycopg2, postgresql, and just now played with flasksmorest and changed it from what it was before to a blueprint.

How to use it:

If you don't have postgresql install it and pgadmin probably comes with it. Open pgadmin set a password, and save the password, youll need it to connect the program to the database.

In pgadmin make a database call contact_book.

Open up the contactbookapi folder and go to app and change password to whatever password you used for pgadmin and make sure its in the quotation marks go to the gui and change the password to the same thing over there.

Also make a virtual environment in terminal and type "python -m venv venv", then in terminal type "source venv/bin/activate".

Next in the terminal type pip install -r requirements.txt.

Afterwards just run the gui, press connect to database and you should be in. Make sure to disconnect before you close it.

To update the contacts in the scroll frame just press the contacts button.
