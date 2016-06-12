from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
# from flask import request

# import CRUD oparations from lesson 1 #
from database_setup import Base, Shop, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def test():
    hoge = session.query(Shop).first()

    print hoge
    return render_template('home.html',hoge = hoge)

@app.route('/category/items')
def showCategories():
    return render_template('categoryitems.html')

@app.route('/category/item')
def showItem():
    return render_template('item.html')

@app.route('/item/edit')
def editItem():
    return render_template('edititem.html')

@app.route('/item/delete')
def deleteItem():
    return render_template('deleteitem.html')

@app.route('/item/add')
def addItem():
    return render_template('additem.html')


if __name__ == '__main__':
    app.secret_key  = 'super_secret_key' # which flask will use to create sessions for our users.
    app.debug = True
    app.run(host='0.0.0.0', port=8080)