from flask import Flask, url_for, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_password"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt_pet"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()
toolbar = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    """List all the pets."""
    pets = Pet.query.all()

    return render_template('homepage.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Add a pet to the agency database."""
    form = AddPetForm()

    if form.validate_on_submit():
        data = {stats: stat for stats, stat in form.data.items() if stats != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{ new_pet.name } is up for adoption.")
        return redirect(url_for('homepage'))
    else:
        return render_template('add_pet_form.html', form=form)   


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """Edit an existing pet."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{ pet.name } updated.")
        return redirect(url_for('homepage'))
    else:
        return render_template('edit_pet_form.html', form=form, pet=pet)
