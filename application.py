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
def test():
    hoges = session.query(Item).order_by(Item.created_date).limit(3)
    return render_template('home.html', hoges = hoges)

@app.route('/<string:category_name>/items')
def showCategoryItems(category_name):
    thecategory = session.query(Category).filter(Category.name == category_name).one()
    items  = session.query(Item).filter_by(category_id = thecategory.id)
    return render_template('categoryitems.html', category_name = category_name, items = items)

@app.route('/<string:category>/<string:item>')
def showItem():
    return render_template('item.html')

@app.route('/<string:item>/edit')
def editItem():
    return render_template('edititem.html')

@app.route('/<string:item>/delete')
def deleteItem():
    return render_template('deleteitem.html')

@app.route('/<string:item>/add')
def addItem():
    return render_template('additem.html')


if __name__ == '__main__':
    app.secret_key  = 'super_secret_key' # which flask will use to create sessions for our users.
    app.debug = True
    app.run(host='0.0.0.0', port=8080)