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

# authorization and authentication
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


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

#@app.route('/catalog')
#def showCatalog():
#    categories = session.query(Category).order_by(Category.name)
#    return render_template('main_page.html', categories=categories)

@app.route('/')
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


@app.route('/categories/<int:category_id>/edit',  methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('edited_category.html', category=editedCategory)


@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deletedCategory)
        flash('%s Successfully Deleted' % deletedCategory.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('delete_category.html', category=deletedCategory)


@app.route('/categories/<int:category_id>')
@app.route('/categories/<int:category_id>/items')
def showCategoryItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('public_items.html', items=items, category=category, creator=creator)
    else:
        return render_template('items.html', items=items, category=category, creator=creator)


# @app.route('/categories/<int:category_id>/<int:item_id>')
# def showItem(category_id, item_id):
#    return 'this will show {item_id} from {category_id}'

@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem=Item(name=request.form['name'], description=request.form['description'],category=request.form['category'], category_id=category_id, user_id=category.user_id)
        session.add(newItem)
        session.commit()
        flash('New %s Item Successfully Created'% (newItem.name))
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('new_item.html', category_id=category_id)


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