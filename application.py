from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
# from flask import request

# import CRUD oparations from lesson 1 #
from database_setup import Base, Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    hoges = session.query(Item).order_by(Item.created_date).limit(3)
    return render_template('home.html', hoges = hoges)

@app.route('/<string:category_slug>/items')
def showCategoryItems(category_slug):
    theCategory = session.query(Category).filter(Category.slug == category_slug).one()
    items  = session.query(Item).filter_by(category_id = theCategory.id)
    return render_template('categoryitems.html', category_name=theCategory.name, items=items)


@app.route('/<string:category_slug>/<string:item_slug>')
def showItem(category_slug, item_slug):
    theCategory = session.query(Category).filter(Category.slug == category_slug).one()
    item = session.query(Item).filter(Item.slug == item_slug).one()
    return render_template('item.html', category_name=theCategory.name, item=item)


@app.route('/<string:category_slug>/<string:item_slug>/edit', methods = ['GET','POST'])
def editItem(category_slug, item_slug):
    item = session.query(Item).filter(Item.slug == item_slug).one()
    
    if request.method == "POST":

        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        flash(item.name + 'has been updated succesfully!')

        theCategory = session.query(Category).filter(Category.id == item.category_id).one()

        return redirect (url_for('showItem', category_slug=theCategory.slug, item_slug= item.slug))      

    else:
        # to get category name
        theCategory = session.query(Category).filter(Category.slug == category_slug).one()
        # to get categories for edit category the item is belonged.
        categories = session.query(Category).all()
        return render_template('edititem.html', item=item, theCategory=theCategory, categories=categories)


@app.route('/<string:item_slug>/delete')
def deleteItem():
    return render_template('deleteitem.html')

@app.route('/<string:item_slug>/add')
def addItem():
    return render_template('additem.html')


if __name__ == '__main__':
    app.secret_key  = 'super_secret_key' # which flask will use to create sessions for our users.
    app.debug = True
    app.run(host='0.0.0.0', port=8080)