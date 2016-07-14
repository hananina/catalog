from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
# from flask import request

# import CRUD oparations from lesson 1 #
from database_setup import Base, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# new impotys for this step (OAUTH2) 
from flask import session as login_session
import random, string

# flow_from_clientsecrets, creates a flow object from the clientsecrets JSON file.
# this JSON formatted style stores your client ID, clientsecret and other OAuth2 parameters.
from oauth2client.client import flow_from_clientsecrets

# if we run into an error trying to exchange an authorization code for an access token.
# we can use this FlowExchangeError method to catch it.
from oauth2client.client import FlowExchangeError

# a comprehensive HTTP client library in python.
import httplib2

import json

# this method converts the return value from a function
# into a real response object that we can send off to our client.
from flask import make_response

# HTTP librariy written in python
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json','r').read())['web']['client_id']
APPLICATION_NAME = 'Item CATALOG'


# Create session and connect to DB
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# to generate unique session token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)


# to generate unique session token
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Confirming that the token that the client sent to the server
    # matches the token the server sent to the client.
    if request.args.get('state') != login_session['state']:
       response = make_response(json.dumps('Invalid state parameters'), 401)
       response.headers['Content-Type'] = 'application/json'
       return response

    code = request.data

    try:
        # [MAKING CREDENTIAL OBJECT WITH OAUTH_FLOW METHOD] 
        # Upgrade the authorization code into a credential object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)


    except FlowExchangeError:
        response = make_response(json.dumps('faild to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # if there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers['Content-Type'] = 'application/json'

    #varify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID.", 401))
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's",401))

        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credential = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credential is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # store the access token in the session for later use,
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info: requesting the user info allowed by my token scope
    # I will store credential token
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;" '
    flash('you are now logged in as %s' %login_session['username'] )
    print 'done!'
    return output


# Disconnect - revoke a current user's token and reset thir login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected user.
    access_token = login_session.get('access_token')

    if access_token is None:
        print 'no access token'
        response = make_response(json.dumps('Current User not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Excute HTTP GET request to revoke current token.
    # To revoke, pass the access token to Google's url and store the response in "result" object.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print 'access_token in disconnect is = '
    print access_token
    print result

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('successfully disconnected!'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        # For watever reason, the given token was invalid.
        response = make_response(json.dumps("Faild to revoke token for intended user"), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
def home():
    hoges = session.query(Item).order_by(Item.created_date).limit(3)
    return render_template('home.html', hoges = hoges)

@app.route('/<string:category_slug>/items')
def showCategoryItems(category_slug):
    theCategory = session.query(Category).filter(Category.slug == category_slug).one()
    items  = session.query(Item).filter_by(category_id = theCategory.id)
    return render_template('categoryitems.html', category_slug=category_slug, category_name=theCategory.name, items=items)


@app.route('/<string:category_slug>/<string:item_slug>')
def showItem(category_slug, item_slug):
    theCategory = session.query(Category).filter(Category.slug == category_slug).one()
    item = session.query(Item).filter(Item.slug == item_slug).one()
    return render_template('item.html', category_slug=category_slug, category_name=theCategory.name, item=item)


@app.route('/<string:category_slug>/<string:item_slug>/edit', methods = ['GET','POST'])
def editItem(category_slug, item_slug):
    item = session.query(Item).filter(Item.slug == item_slug).one()

    if request.method == "POST":
        item.name = request.form['name']
        item.slug = request.form['name'].lower().replace(' ','_')
        item.description = request.form['description']
        item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        flash(item.name + 'has been updated succesfully!')

        # to get category slug from updated item, in order to use redirect argument
        theCategory = session.query(Category).filter(Category.id == item.category_id).one()
        return redirect (url_for('showItem', category_slug=theCategory.slug, item_slug= item.slug))      

    else:
        # to get category info
        theCategory = session.query(Category).filter(Category.slug == category_slug).one()
        # to get categories for edit category the item is belonged.
        categories = session.query(Category).all()
        return render_template('edititem.html', item=item, category_slug=category_slug, category_name=theCategory.name, categories=categories)


@app.route('/<string:category_slug>/<string:item_slug>/delete', methods = ['GET','POST'])
def deleteItem(category_slug, item_slug):
    item = session.query(Item).filter(Item.slug == item_slug).one()
    theCategory = session.query(Category).filter(Category.slug == category_slug).one()
    
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash(item.name + "has been deleted succesfully!")
        return redirect(url_for('showCategoryItems', category_slug=category_slug))

    else:
        return render_template('deleteitem.html', item=item, category_slug=category_slug, category_name= theCategory.name)


@app.route('/add', methods =['GET','POST'])
def addItem():

    if request.method == "POST":

        newItem = Item(
                    name=request.form['name'], 
                    slug=request.form['name'].lower().replace(' ','_'), 
                    description=request.form['description'], 
                    category_id=request.form['category_id']
                )

        session.add(newItem)
        session.commit()

        theCategory = session.query(Category).filter(Category.id==request.form['category_id']).one()

        return redirect (url_for('showCategoryItems', category_slug=theCategory.slug))

    else:
        categories = session.query(Category).all()
        return render_template('additem.html',categories=categories)


if __name__ == '__main__':
    app.secret_key  = 'super_secret_key' # which flask will use to create sessions for our users.
    app.debug = True
    app.run(host='0.0.0.0', port=8080)