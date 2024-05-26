from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user
from models.model import Recipe, Ingrediants, Comment
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

	# Define allowed file extensions



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
		# else:
		# 	return "done"

		recipe = Recipe(title=title, description=description, instructions=instructions, category=category, image=image.filename, user_id=current_user.id)
		db.session.add(recipe)
		db.session.commit()
		flash("recipe added successfully ", 'success')
		return redirect(url_for('main.add_ingrediants'))
	return render_template('add_recipe.html')


@main.route('/add-ingrediants', methods=['POST', 'GET'])
def add_ingrediants():
	if not current_user.is_authenticated:
		flash('Log in first to visit page', 'warning')
		return redirect(url_for('auth.login'))

	if request.method == "POST":
		item = request.form['title']
		amount = request.form['description']
		recipe_id = request.form['recipe_id']
		ingrediants = Ingrediants(item=item, amount=amount,recipe_id=recipe_id)
		db.session.add(ingrediants)
		db.session.commit()
		flash("ingrediants added successfully ", 'success')
		return "add success ingrediants "
	return "add ingrediants"


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

@main.route('/base')
def base():
	return render_template('base.html')