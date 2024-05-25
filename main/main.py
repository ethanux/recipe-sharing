from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user
from models.model import Recipe, Ingrediants, Comment
main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route('/add-recipe', methods=['POST', 'GET'])
def add_recipe():
	if not current_user.is_authenticated:
		flash('Logg in first to visit page', 'warning')
		return redirect(url_for('auth.login'))

	if requst.method == "POST":
		title = request.form['title']
		description = request.form['description']
		instructions = request.form['instructions']
		category = request.form['category']
		image = request.form['images']
		recipe = Recipe(title=title, description=description, instructions=instructions, category=category, image=image, user_id=current_user.id)
		db.session.add(recipe)
		db.session.commit()
		flash("recipe added successfully ", 'success')
		return "add success recipe "
	return "add recipe"


@main.route('/add-ingrediants', methods=['POST', 'GET'])
def add_ingrediants():
	if not current_user.is_authenticated:
		flash('Logg in first to visit page', 'warning')
		return redirect(url_for('auth.login'))

	if requst.method == "POST":
		item = request.form['title']
		amount = request.form['description']
		recipe_id = request.form['recipe_id']
		ingrediants = Ingrediants(item=item, amount=amount,recipe_id=recipe_id)
		db.session.add(ingrediants)
		db.session.commit()
		flash("ingrediants added successfully ", 'success')
		return "add success ingrediants "
	return "add ingrediants"