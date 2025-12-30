# Fichier: (à placer à la racine de votre projet)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_here' # Remplacez par une clé secrète forte
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Base de données SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définition d'un modèle simple pour l'utilisateur (pour la base de données)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', 'Admin: {self.is_admin}')"

# Route pour la page d'accueil
@app.route('/')
def home():
    return "<h1>Bienvenue sur notre service d'hébergement !</h1><p>Cette page sera la page d'accueil principale.</p>"

# Exécute l'application si ce fichier est le fichier principal exécuté
if __name__ == '__main__':
    # Crée toutes les tables de la base de données si elles n'existent pas
    with app.app_context():
        db.create_all()
    app.run(debug=True)
