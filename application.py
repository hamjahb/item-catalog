from databasesetup import Base, User, Category, Item
from flask import Flask, jsonify, request, url_for, abort, g, redirect, flash, render_template
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth() 

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# JSON APi
@app.route('/categories/json')
def categoriesJSON():
    return 'this will show the json for categories'

@app.route('/categories/<int:category_id>/json')
def showCategoryItemsJSON(category_id):
    return 'this will show the items json in {category_id}'

@app.route('/categories/<int:category_id>/<int:item_id>/json')
def showItemJSON(category_id, item_id):
    return 'this will show JSON of {item_id} from {category_id}'


#main application
@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(Category.name)
    return render_template('main_page.html', categories=categories)

@app.route('/categories')
def showCategories():
    categories = session.query(Category).order_by(Category.name)
    return render_template('main_page.html', categories=categories)

@app.route('/categories/new', methods = ['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Succesfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('new_category.html')

@app.route('/categories/<int:category_id>/edit')
def editCategory(category_id):
    return 'this page will be to edit {category_id}'

@app.route('/categories/<int:category_id>/delete')
def deleteCategory(category_id):
    return 'this page will be to delete {category_id}'

@app.route('/categories/<int:category_id>/items')
def showCategoryItems(category_id):
    return 'will show all items in {category_id}'

@app.route('/categories/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
    return 'this will show {item_id} from {category_id}'

@app.route('/categories/<int:category_id>/new')
def newCategoryItem(category_id):
    return 'this page will adda new item in {category_id}'

@app.route('/categories/<int:category_id>/<int:item_id>/edit')
def editCategoryItem(category_id, item_id):
    return 'this page will be to edit {item_id} in {category_id}'

@app.route('/categories/<int:category_id>/<int:item_id>/delete')
def deleteCategoryItem(category_id, item_id):
    return 'this page will be to delete {item_id} in {category_id}'



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)