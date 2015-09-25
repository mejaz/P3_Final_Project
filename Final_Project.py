from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Usernames, Catagory, Items

# imports for oAuth 2.0

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Getting the Client ID from the .json file downloaded from Google.

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Creating a Database Engine

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# State token and login page

@app.route('/login')

def showLogin():
    """ Retruns a state  token with random uppercase letter and digits to login template """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
		 for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)

# Routing to Google+ login button.

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


    # Adding username to our Database.
    # Password is default to 12345 for every user.

    # First check if the user already exists.

    my_user = session.query(Usernames).filter_by(user_id=login_session['email']).all()

    if len(my_user) > 0:
    	print "user already exists"
    else:
	    user = Usernames(user_id=login_session['email'], user_pic=login_session['picture'], user_password="12345")
	    session.add(user)
	    session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Logout a User.

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        
        return redirect(url_for('displayCatalog'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



# Display home page.
@app.route('/')
@app.route('/catalog/')

def displayCatalog():
	all_catagories = session.query(Catagory).all()

	# Displaying only the latest 9 items added to the Database.
	all_items = session.query(Items).order_by(Items.item_id.desc()).limit(9)

	if 'username' not in login_session:
		return render_template('catalog.html', all_catagories=all_catagories, all_items=all_items)
	else:
		return render_template('catalogonLogin.html', all_catagories=all_catagories, all_items=all_items)
	

# User logged in
@app.route('/catalogonLogin/')

def displayCatalogonLogin():
	if 'username' not in login_session:
		return redirect('/login')
	all_catagories = session.query(Catagory).all()

	# Displaying only the latest 9 items.
	all_items = session.query(Items).order_by(Items.item_id.desc()).limit(9)

	# return render_template('catalogonLogin.html', all_catagories=all_catagories, all_items=all_items)
	return render_template('catalogonLogin.html', all_catagories=all_catagories, all_items=all_items)

# Display all items for a selected category
@app.route('/catalog/<string:catagory_name>/items')

def displayCatagoryItems(catagory_name):
    all_catagories = session.query(Catagory).all()

    # Selected catagory.
	
    sel_cat = session.query(Catagory).filter_by(catagory_name=catagory_name).one()
	
    if 'username' not in login_session:
		catagory_items = session.query(Items).filter_by(catagory_id_fk=sel_cat.catagory_id).all()
		return render_template('catagoryItems.html', all_catagories=all_catagories, all_items=catagory_items, sel_cat=sel_cat)
    else:
		catagory_items = session.query(Items).filter_by(catagory_id_fk=sel_cat.catagory_id, user_id_fk=login_session['email']).all()
		return render_template('catagoryItems.html', all_catagories=all_catagories, all_items=catagory_items, sel_cat=sel_cat)

# Display selected item's description - Add for authorized users
@app.route('/catalog/<string:catagory_name>/<string:item_name>/<string:userid>')
def displayItemDesc(catagory_name, userid, item_name):
    
    # Selected catagory.

    catagory = session.query(Catagory).filter_by(catagory_name=catagory_name).one()
   
    if 'username' not in login_session:
        
        # Filtering the description for the selected catagory.

        sel_cat = session.query(Items).filter_by(catagory_id_fk=catagory.catagory_id, item_name=item_name, user_id_fk=userid).one()
        return render_template('itemDesc.html', catagory_name=catagory_name, item=sel_cat)
    else:

        # Filtering the description for the selected catagory.

        sel_cat = session.query(Items).filter_by(catagory_id_fk=catagory.catagory_id, item_name=item_name, user_id_fk=login_session['email']).one()
        return render_template('itemDesconLogin.html', catagory_name=catagory_name, item=sel_cat)
	

# Delete a selected item
@app.route('/catalog/<string:catagory_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(catagory_name, item_name):

    if 'username' not in login_session:
        return redirect('/login')

    # Selected Catagory.

	catagory = session.query(Catagory).filter_by(catagory_name=catagory_name).one()
	
    #  Filtering the item to be deleted.

    sel_cat = session.query(Items).filter_by(catagory_id_fk=catagory.catagory_id, item_name=item_name).one()

    if request.method == 'POST':
		print request.form['response']
		if request.form['response'] == "Yes":
			session.delete(sel_cat)
			session.commit()
			flash(item_name + " successfully deleted.")
			return redirect(url_for('displayCatagoryItems', catagory_name=catagory_name))
		else:
			return redirect(url_for('displayCatagoryItems', catagory_name=catagory_name))
    else:
		return render_template('deleteItem.html', catagory_name=catagory_name, item_name=item_name)

# Edit a selected item - authorized user
@app.route('/catalog/<string:catagory_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(catagory_name, item_name):

    if 'username' not in login_session:
		return redirect('/login')


    # Seleected Catagory.

    catagory = session.query(Catagory).filter_by(catagory_name=catagory_name).one()
	
    # Filtering the item to be edited.

    sel_cat = session.query(Items).filter_by(catagory_id_fk=catagory.catagory_id, item_name=item_name).one()


    if request.method == 'POST':

		if request.form['items_name']:
			
			sel_cat.item_name = request.form['items_name']
			sel_cat.item_desc = request.form['items_desc']
			session.add(sel_cat)
			session.commit()
			flash("Item edited successfully!")
		return redirect(url_for('displayCatagoryItems', catagory_name=catagory_name))
    else:
		return render_template('editItem.html', catagory_name=catagory_name, item=sel_cat)

# Add a new item - authorized users only
@app.route('/catalog/addItem', methods=['GET', 'POST'])
def addItem():

	if 'username' not in login_session:
		return redirect('/login')

    # Selecting all catagory names.

	all_catagories = session.query(Catagory).all()

    # Selecting all Items

	all_items = session.query(Items).all()
	if request.method == 'POST':
		if request.form['addedItem']:

			catToAdd = session.query(Catagory).filter_by(catagory_name=request.form['catg_name']).one()
			
			username1 = session.query(Usernames).filter_by(user_id=login_session['email'], user_pic=login_session['picture'], user_password='12345').one()
			item1 = Items(item_name=request.form['addedItem'], item_desc=request.form['addedItemDesc'], catagory=catToAdd, usernames=username1)
			session.add(item1)
			session.commit()
			flash("Item successfully added.")
		return redirect(url_for('displayCatalog'))
	else:
		catagory = session.query(Catagory).all()
		return render_template('addItem.html', catagory=catagory)

# API endpoint
@app.route('/catalog/<string:catagory_name>/items/JSON')
def allItemsJSON(catagory_name):
    """ returns a JSON"""
    selected_catagory = session.query(Catagory).filter_by(catagory_name=catagory_name).one()
    catagory_items = session.query(Items).filter_by(catagory_id_fk=selected_catagory.catagory_id).all()

    return jsonify(AllItems=[i.serialize for i in catagory_items])


if __name__ == '__main__':
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host='0.0.0.0', port=8000)