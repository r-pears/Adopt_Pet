"""Models for Adoption Agency Pet app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE = 'https://www.readersdigest.ca/wp-content/uploads/2013/03/6-facts-to-know-before-owning-a-puppy.jpg?w=1000'


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)


class Pet (db.Model):
    """Model for the pet up for adoption."""
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def image_url(self):
        """Return the image of the pet."""

        return self.photo_url or DEFAULT_IMAGE
