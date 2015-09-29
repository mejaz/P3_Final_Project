Item Catalog Version 1.0 09/25/2015

Introduction:
-------------
This website can be used to view the latest items added by the users, list of items in a selected catagory and item description.

An authorized user can add, delete and edit an item.

A user can login using Google+ account.


Configuration:
----------------------------
The webserver (Final_Project.py) works with -
1. Flask framework - 0.9, 0.10
2. SQLAlchemy Version - 0.8.4
3. oauth2client Version - 1.4.11



Database:
---------
1. The name of the database(s) : catalog.db


Steps to run the test file:
-------------------------------
1. Navigate to the P3_Final_Project directory path.
2. Following files should be present in this directory : 
	i. Final_Project.py
	ii. database_setup.py
	iii. client_secrets.json
	iv. catalog.db
	v. templates (directory containing different templates)
	vi. templates (directory containing stylesheets)
3. After navigating to P3_Final_Project directory, type python Final_Project.py, to start the server.
4. Goto the Chrome browser and type the URL - http://localhost:8000/
5. Then hit Enter.


API Endpoints:
--------------
1. JSON Endpoint : http://localhost:8000/catalog/<string:catagory_name>/items/JSON
2. XML Endpoint : http://localhost:8000/catalog/<string:catagory_name>/items/XML

List of Categories - catagory_name:

Soccer , Baseketball ,	Baseball , Frisbee , Snowboarding , Rock Climbing , Foosball , Skating , Hockey 

e.g. To get the items under category 'Soccer', 

For a JSON response, use : http://localhost:8000/catalog/Soccer/items/JSON

Similarly, for an XML response, use : /catalog/Soccer/items/XML


Contact Us:
Email : mohdejazsiddiqui@gmail.com