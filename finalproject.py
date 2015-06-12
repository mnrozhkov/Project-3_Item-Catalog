#!/usr/bin/python
"""The Multy-Level Catalog Project

The app is a catalog of open source projects stored in few categorues.
Logged in user can use CRUD functionality on categories and projects he/she added
to catalog.
"""

from flask import Flask, render_template, request, redirect,jsonify, url_for, flash, \
    make_response
from flask import session as login_session
import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#import from project modules
from database_setup import Base, Category, Project, User
# from user import createUser, getUserInfo, getUserID

#IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

#create application function
def create_app():
    '''Create and run the app

    Returns:
      application object
    '''

    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'development'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects_catalog_users.db'
    return app


#run application
app = create_app()


# configure database connection
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db = DBSession()


#Create anti-forgery state token
@app.route('/login')
def showLogin():
    '''Creates anti-forgery state token

    Returns:
      Render login.html template with anti-forgery state token
    '''

    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    print("The current session state is %s" % login_session['state'])
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE = state)


#Authorization via Google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''Authorizes an user via Google+ account

    Returns:
      Returns a response with results of authorization via Google+
    '''

    CLIENT_ID = json.loads(
    open('client_secrets_gl.json', 'r').read())['web']['client_id']
    APPLICATION_NAME= "Open Source Projects Catalog"

    #Validate state token
    print("gconnect() step 1: check for 'state'...")
    print 'received state of %s' %request.args.get('state')
    print 'login_sesion["state"] = %s' %login_session['state']
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Obtain authorization code
    print("gconnect() step 2: Obtain authorization code...")
    # gplus_id = request.args.get('gplus_id')
    # print "request.args.get('gplus_id') = %s" %request.args.get('gplus_id')
    code = request.data

    print("gconnect() step 3:  Upgrade the authorization code into a credentials object...")
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets_gl.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        # credentials = credentials.to_json
        print(credentials)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    print("gconnect() step 4:  Check that the access token is valid...")
    access_token = credentials.access_token
    # access_token = login_session.get('credentials')
    # print("Access token: " + access_token)

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # print("result: " + str(result))

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    print("gconnect() step 5: ...")
    gplus_id = credentials.id_token['sub']
    # print("gplus_id is: " + gplus_id)
    # print("user_id is: " + str(result)) #something is wrong here
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    print("gconnect() step 6: ...")
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    #Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    print("gconnect() step 7: ...")
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # response = make_response(json.dumps('Successfully connected user.', 200))

    print("#Get user info")
    # print("gconnect() step 8: ...")
    userinfo_url =  "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    # data = answer.json()
    data = json.loads(answer.text)
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        # print("New user was created!")
    login_session['user_id'] = user_id

    print("gconnect() step 9: ...")
    output = ''
    output +='<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output +=' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s"%login_session['username'])
    # print "done!"
    return output


#DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    '''Revoke a current user's token and reset their login session

    Returns:
      Returns a response with deleted session info
    '''

    print("gdisconnect(): started")
    #Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # access_token = credentials.access_token
    access_token = login_session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # result = json.loads(h.request(url, 'GET')[1])

    if result['status'] == '200':
        #Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print("gdisconnect(): finished")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print("gdisconnect(): finished")
        return response


# Authorize user via Facebook account
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    '''Authorizes an user via Facebook account

    Returns:
      Returns a response with results of authorization via FB and user data
    '''

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    # print "Step 1: access token received %s " % access_token
    # print "Step 1: login_session['state'] %s " % login_session['state']

    app_id = json.loads(open('client_secrets_fb.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('client_secrets_fb.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    # print(url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # result = json.loads(h.request(url, 'GET')[1])
    # print "Step: result: %s" % result

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]
    # print "Step: token: %s" % token

    url = 'https://graph.facebook.com/v2.2/me?%s' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # result = json.loads(h.request(url, 'GET')[1])
    # print "url sent for API access:%s"% url
    # print "Step 2: API JSON result: %s" % result
    data = json.loads(result)
    # print("Print data: " + data)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    # print "Step 3: Login_session data collected "

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    '''Revoke a current user's token and reset their login session

    Returns:
      Returns a response with deleted session info
    '''

    facebook_id = login_session['facebook_id']
    # print("facebook_id: %s", facebook_id)

    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    # print("access_token: %s", access_token)

    url = 'https://graph.facebook.com/%s/permissions' % (facebook_id)
    # print("url: %s", url)

    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    '''Dicsonnect session based on provider

    Returns:
      Call gdisconnect() or fbdisconnect() function
    '''

    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


#User Helper Functions
def createUser(login_session):
    '''Create new user and store data into database

    Returns:
      user.id
    '''

    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    db.add(newUser)
    db.commit()
    user = db.query(User).filter_by(email = login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''Retrieve user info from database

    Returns:
      Object User
    '''

    user = db.query(User).filter_by(id = user_id).one()
    return user


def getUserID(email):
    '''Get an user ID based on user's email

    Returns:
      user.id or None
    '''

    try:
        user = db.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None


###Create restful API
#JSON APIs to view Open Source Projects Catalog information
@app.route('/category/<category_id>/projects/JSON')
def categoryJSON(category_id):
    '''JSON APIs to view Category information

    Returns:
      List of projects names, abstacts and image
    '''

    # category = db.query(Category).filter_by(id = category_id).one()
    projects = db.query(Project).filter_by(category_id = category_id).all()
    return jsonify(categoryProjects = [item.serialize for item in projects])


@app.route('/category/<category_id>/projects/<project_id>/JSON')
def projectJSON(category_id, project_id):
    '''JSON APIs to view Project information

    Returns:
      Project's name, abstact, image, website
    '''

    project = db.query(Project).filter_by(id = project_id).one()
    return jsonify(project = project.serialize)


@app.route('/catalog/JSON')
def catalogJSON():
    '''JSON APIs to view Project information

    Returns:
        List of categories IDs, names and images
    '''

    catalog = db.query(Category).all()
    return jsonify(categories = [item.serialize for item in catalog])


#Show all categories and last added (new) projects
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    '''Shows main page with all categories and last added (new) projects

    Returns:
        Main page catalog.html
    '''

    #show all categories
    #return("This page will show all categories and last items")
    lastprojects = []
    categories = db.query(Category).all()
    for each_category in categories:
        #item = db.query(Project).one()
        # print("each_category.name value: ", each_category.name)
        # print(lastprojects)
        # category_projects = showCategory(each_category.name)
        item = db.query(Project).filter_by(category_id = each_category.id).order_by('-id').first()
        lastprojects.append(item)

    if 'username' not in login_session:
        return render_template('catalog_public.html', categories = categories, projects = lastprojects)
    else:
        user_id = login_session['user_id']
        user = db.query(User).filter_by(id = user_id).one()
        return render_template('catalog.html', categories = categories, projects = lastprojects,
                               user_picture = user.picture, user_name = user.name)


###Create a new category of projects
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    '''Adds new category

    Returns:
        Render template category_new.html
    '''

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newCategory = Category(name = request.form['name'],
                               user_id=login_session['user_id'],
                               image = request.form['image'])
        db.add(newCategory)
        db.commit()
        flash("New category %s added!" % newCategory.name)
        return redirect(url_for('showCategory', category_id = newCategory.id))
    else:
        return render_template('category_new.html')


#Edit category
@app.route('/category/<category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    '''Edit a category info

    Returns:
        Render template category_edit.html
    '''

    #a user has the ability to update item info
    # return("This page will allow user to update %s project info")
    # # % project_id)
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = db.query(Category).filter_by(id = category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this Categroy. " \
           "Please create your own Category in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name'] or request.form['image']:
            editedCategory.name = request.form['name']
            editedCategory.image = request.form['image']
            db.add(editedCategory)
            db.commit()
        flash("Category %s has been edited!" % editedCategory.name)
        return redirect(url_for('showCategory', category_id = editedCategory.id))
    else:
        return render_template('category_edit.html', category_id = editedCategory.id, category = editedCategory)


#Delete category
@app.route('/category/<category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    '''Delete a category

    Returns:
        Render template category_delete.html
    '''

    itemToDelete = db.query(Category).filter_by(id = category_id).one()
    if 'username' not in login_session:
        return redirect('/login')

    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this Categroy. " \
           "Please create your own Category in order to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        db.delete(itemToDelete)
        db.commit()
        flash("Category %s deleted!" % itemToDelete.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('category_delete.html', category = itemToDelete)


#Show projects in the category
@app.route('/category/<category_id>/')
@app.route('/category/<category_id>/projects/')
def showCategory(category_id):
    '''Shows you all projects in the category

    Returns:
        Render template category.html
    '''

    category = db.query(Category).filter_by(id = category_id).one()
    creator = getUserInfo(category.user_id)
    projects = db.query(Project).filter_by(category_id = category_id).all()
    # for item in projects:
    #     print(item.name)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('category_public.html', category = category, projects = projects, creator= creator)
    else:
         return render_template('category.html', category = category, projects = projects, creator= creator)


@app.route('/category/<category_id>/projects/<project_id>/')
def showProject(category_id, project_id):
    '''Shows all info about the project

    Returns:
        Render template project.html
    '''

    projectToShow = db.query(Project).filter_by(id = project_id).one()
    category = db.query(Category).filter_by(id = projectToShow.category_id).one()
    creator = getUserInfo(category.user_id)
    # print(category.name)
    # print(category.id)
    print("showProject: category.id: " + str(category.id))
    print("showProject: project.id: " + str(projectToShow.id))
    if 'username' not in login_session or creator.id != login_session['user_id']:
        print("showProject: user_id: " + str(creator.id))
        return render_template('project_public.html', project = projectToShow, category = category)
    else:
        return render_template('project.html', project = projectToShow, category = category)


#Create a new project
@app.route('/category/<category_id>/new/', methods=['GET', 'POST'])
@app.route('/category/<category_id>/projects/new/', methods=['GET', 'POST'])
def newProject(category_id):
    '''Create a new project

    Returns:
        Render template project_new.html
    '''

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newProject = Project(name = request.form['name'],
                             abstract = request.form['abstract'],
                             description = request.form['description'],
                             license = request.form['license'],
                             website = request.form['website'],
                             category_id = category_id,
                             user_id=login_session['user_id'],
                             image = request.form['image'])
        db.add(newProject)
        db.commit()
        flash("New project %s added!" % newProject.name)
        #get new project id
        item = db.query(Project).filter_by(category_id = category_id).order_by('-id').first()
        # print("newProject: showProject id: " + str(item.id))

        # return redirect(url_for('showProject', category_id = category_id, project_id = item.id))
        return showProject(project_id = item.id, category_id = item.category_id)
        # return render_template('project.html', project_id = item.id, category_id = category_id)
    else:
        # print(category_id)
        return render_template('project_new.html', category_id = category_id)


#Edit a project
@app.route('/category/<category_id>/projects/<project_id>/edit/', methods=['GET', 'POST'])
def editProject(project_id, category_id):
    '''Edit project

    Returns:
        Render template project_edit.html
    '''

    itemToEdit = db.query(Project).filter_by(id = project_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToEdit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not" \
               "authorized to edit this project. Please create your " \
               "own project in order to edit.');</script><body" \
               "onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['abstract']:
            itemToEdit.abstract = request.form['abstract']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['license']:
            itemToEdit.license = request.form['license']
        if request.form['website']:
            itemToEdit.website = request.form['website']
        db.add(itemToEdit)
        db.commit()
        flash("Project %s has been edited!" % itemToEdit.name)
        return redirect(url_for('showProject', project_id = itemToEdit.id, category_id = itemToEdit.category_id))
    else:
        return render_template('project_edit.html', project = itemToEdit, category_id = itemToEdit.category_id)


#Delete a project
@app.route('/category/<category_id>/projects/<project_id>/delete/', methods=['GET', 'POST'])
def deleteProject(category_id, project_id):
    '''Delete project

    Returns:
        Render template project_delete.html
    '''

    itemToDelete = db.query(Project).filter_by(id = project_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not" \
               "authorized to delete this project. Please create your " \
               "own project in order to delete.');</script><body" \
               "onload='myFunction()''>"

    if request.method == 'POST':
        db.delete(itemToDelete)
        db.commit()
        flash("Project %s deleted!" % itemToDelete.name)
        return redirect(url_for('showCategory', category_id = itemToDelete.category_id))
    else:
        return render_template('project_delete.html', category_id = category_id, project = itemToDelete)




if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)
