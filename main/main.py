from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from flask_login import current_user
from models.model import Recipe, Ingrediants, Comment, User
from werkzeug.utils import secure_filename
from ext.ext import db
import os

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_upload():
	if not os.path.exists(main.upload_folder):
		os.makedirs(main.upload_folder)

@main.route('/add-recipe', methods=['POST', 'GET'])
def add_recipe():
	if not current_user.is_authenticated:
		flash('Logg in first to visit page', 'warning')
		return redirect(url_for('auth.login'))
	if request.method == "POST":
		title = request.form['title']
		description = request.form['description']
		instructions = request.form['instructions']
		category = request.form['category']
		if 'image' not in request.files:
			flash('No file part', 'danger')
			return redirect(request.url)
		image = request.files['image']
        # If user does not select a file, the browser submits an empty file without a filename
		if image.filename == '':
			flash('No selected file', 'danger')
			return redirect(request.url)
			file_upload()
		if not image and not allowed_file(image.filename):
			flash('File type not allowed', 'error')
			return redirect(request.url)
		filename = secure_filename(image.filename)
		image.save(os.path.join(main.upload_folder, filename))
		flash('image successfully uploaded', 'success')
		recipe = Recipe(title=title, description=description, instructions=instructions, category=category, image=image.filename, user_id=current_user.id)
		db.session.add(recipe)
		db.session.commit()
		session['recipe_id'] = recipe.id
		session['data'] = {}
		flash("recipe added successfully ", 'success')
		return redirect(url_for('main.add_ingrediants'))
	return render_template('add_recipe.html')


@main.route('/add-recipe/add-ingrediants', methods=['POST', 'GET'])
def add_ingrediants():
	if not current_user.is_authenticated:
		flash('Log in first to visit page', 'warning')
		return redirect(url_for('auth.login'))
	try:
		recipe_id = session['recipe_id']
	except KeyError:
		flash('add recipe first before adding ingrediants', 'danger')
		return	redirect(url_for('main.add_recipe'))
	if request.method == "POST":
		btn = request.form['button']
		if btn == 'add':
			item = request.form['item']
			amount = request.form['amount']
			if item in ("", None) or amount in ("", None) :
				flash("Item name And Item amount Cannot be blank", 'warning')
				return redirect(request.url)	
			session['data'][item] = amount 
			session.modified = True
			print(session)
			return render_template('add_ingrediants.html', data=session['data'])
		if btn == 'Save & Continue':
			data = session['data']
			for item, amount in data.items():
				ingrediants = Ingrediants(item=item, ammount=amount,recipe_id=recipe_id)
				db.session.add(ingrediants)
				db.session.commit()
			flash("ingrediants added successfully ", 'success')
			session.clear()
			return redirect(url_for('main.base'))
	return render_template("add_ingrediants.html", data=session['data'])

@main.route('/add-recipe/add-ingrediants/remove/<string:item>/<string:amount>')
def  remove_ingrediants(item,amount):
		removed = False
		if item in session['data']:
		    session['data'].pop(item)
		    removed = True
		    # Mark the session as modified to ensure changes are saved
		if removed:
		    session.modified = True
		    flash(f'Items {item} removed successfully!', 'info')
		    return render_template('add_ingrediants.html', data=session['data'])
		return redirect(url_for('main.add_ingrediants'))

@main.route('/add-comment/<int:recipe_id>', methods=['POST', 'GET'])
def add_comment(recipe_id):
	if not current_user.is_authenticated:
		flash('Log in first to visit page', 'warning')
		return redirect(url_for('auth.login'))
	if request.method == "POST":
		content = request.form['content']
		rating = request.form['rating']
		recipe_id = recipe_id
		if len(content) > 100 :
			flash("content mst be less than 100 characters", 'danger')
			return redirect(url_for('add_comment'))
		comment = Comment(content=content, rating=rating,recipe_id=int(recipe_id), user_id=current_user.id)
		db.session.add(comment)
		db.session.commit()
		flash("comments added successfully ", 'success')
		return "add success comments here"
	return "add comments"


@main.route('/find-recipe/<string:filters>')
def find_recipe(filters):
	if filters == 'all':
		recipes = Recipe.query.all()
		return render_template("find_recipe.html", recipes=recipes, path=main.upload_folder)
	elif filters not in ['Breakfast','Brunch', 'Lunch','Dinner','Supper', 'Disert', 'Snack']:
		flash('Invalid filter value ', 'danger')
		recipes = Recipe.query.all()
		return render_template("find_recipe.html", recipes=recipes, path=main.upload_folder)
	else:
		recipes = Recipe.query.filter_by(category=filters).all()
		return render_template("find_recipe.html", recipes=recipes, path=main.upload_folder, category=filters)

@main.route('/find-recipe/view-recipe/<int:id>')
def view_recipe(id):
	if not current_user.is_authenticated:
		flash('Please log in to visit this page', 'warning')
		return redirect(request.url)
	recipe = Recipe.query.filter_by(id=id).first()
	if recipe:
		print(recipe.ingredients)
		return render_template('view_recipe.html', recipe=recipe)
	else:
		flash('recipe not found ', 'danger')
		return redirect(request.url)


@main.route('/profile', methods = ['POST', "GET"])
def profile():
	if not current_user.is_authenticated:
		flash('Please log in to visit this page', 'warning')
		return redirect(request.url)
	if request.method == 'POST':
		username = request.form['username'] 
		password = request.form['password']

		if len(password) >= 8:
			try:
				str(username)
				user = User.query.filter_by(id=current_user.id).first()
				user.username = username
				user.password = password
				db.session.commit()
				flash('INformation updated successfuly', 'success')
				
			except Exception as e:
				raise e
	recipes = Recipe.query.filter_by(user_id=current_user.id).all()
	
	return render_template('profile.html', recipes=recipes)

@main.route('/base')
def base():
	return render_template('base.html')