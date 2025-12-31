```python
# Fichier: app.py (à placer à la racine de votre projet)

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_key_here') # Remplacez par une clé secrète forte en production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Base de données SQLite pour le développement
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définition d'un modèle simple pour l'utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Relations avec les abonnements et tickets
    subscriptions = db.relationship('Subscription', backref='user_rel', lazy=True)
    tickets_created = db.relationship('SupportTicket', foreign_keys='SupportTicket.user_id', backref='user_ticket_rel', lazy=True)
    tickets_assigned = db.relationship('SupportTicket', foreign_keys='SupportTicket.admin_id', backref='admin_ticket_rel', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', 'Admin: {self.is_admin}')"

# Modèle pour les Catégories de Services
class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    plans = db.relationship('ServicePlan', backref='category', lazy=True)

    def __repr__(self):
        return f"ServiceCategory('{self.name}')"

# Modèle pour les Plans de Services
class ServicePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    elite_maintenance = db.Column(db.Boolean, default=False)
    subscriptions = db.relationship('Subscription', backref='plan_rel', lazy=True)

    def __repr__(self):
        return f"ServicePlan('{self.name}', '{self.price}', Category: '{self.category.name}')"

# Modèle pour les Abonnements Clients
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('service_plan.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Subscription(User: '{self.user_rel.username}', Plan: '{self.plan_rel.name}', Active: {self.is_active})"

# Modèle pour les Tickets de Support Client
class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Ouvert')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        user_name = self.user_ticket_rel.username if self.user_ticket_rel else 'N/A'
        admin_name = self.admin_ticket_rel.username if self.admin_ticket_rel else 'N/A'
        return f"SupportTicket(ID: {self.id}, Subject: '{self.subject}', Status: '{self.status}', User: '{user_name}', Admin: '{admin_name}')"


# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Ce nom d\'utilisateur existe déjà.', 'danger')
            return redirect(url_for('register'))
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Cet e-mail est déjà utilisé.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('client_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Connexion réussie !', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('client_dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html')

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('home'))

# Route de tableau de bord admin
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Accès non autorisé. Vous devez être administrateur.', 'danger')
        return redirect(url_for('login'))

    users = User.query.all()
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    categories = ServiceCategory.query.all() 
    plans = ServicePlan.query.all() 
    subscriptions = Subscription.query.all() 

    return render_template('admin_dashboard.html', users=users, tickets=tickets, categories=categories, plans=plans, subscriptions=subscriptions)

# Route de tableau de bord client
@app.route('/client_dashboard')
def client_dashboard():
    if not session.get('user_id'):
        flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user.is_admin:
        flash('Vous êtes connecté en tant qu\'administrateur. Accès au tableau de bord admin.', 'info')
        return redirect(url_for('admin_dashboard'))

    active_subscriptions = Subscription.query.filter_by(user_id=user.id, is_active=True).all()
    user_tickets = SupportTicket.query.filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()

    return render_template('client_dashboard.html', user=user, active_subscriptions=active_subscriptions, user_tickets=user_tickets)

# Route d'accueil
@app.route('/')
def home():
    # Données de démonstration pour les catégories et les plans
    # En production, vous chargeriez ces données depuis la base de données
    categories_data = [
        {
            'name': 'Hébergement de Sites Web',
            'description': 'Idéal pour les entreprises et les portfolios.',
            'plans': [
                {'name': 'Basique', 'price': 9.99, 'features': ['10 Go SSD', '1 Domaine', 'Support Standard']},
                {'name': 'Professionnel', 'price': 19.99, 'features': ['50 Go SSD', '3 Domaines', 'Support Prioritaire']},
                {'name': 'Entreprise', 'price': 49.99, 'features': ['100 Go SSD', 'Domaines Illimités', 'Support Elite', 'Maintenance Prioritaire']}
            ]
        },
        {
            'name': 'Hébergement de Jeux',
            'description': 'Créez votre propre serveur pour jouer avec vos amis.',
            'plans': [
                {'name': 'Petit Serveur', 'price': 14.99, 'features': ['4 Go RAM', '2 CPU Cores', 'Protection DDoS']},
                {'name': 'Moyen Serveur', 'price': 29.99, 'features': ['8 Go RAM', '4 CPU Cores', 'Protection DDoS Avancée']},
                {'name': 'Grand Serveur', 'price': 59.99, 'features': ['16 Go RAM', '6 CPU Cores', 'Support 24/7', 'Maintenance Prioritaire']}
            ]
        },
        {
            'name': 'Stockage Cloud',
            'description': 'Stockez vos fichiers en toute sécurité et accédez-y de partout.',
            'plans': [
                {'name': 'Personnel', 'price': 5.00, 'features': ['100 Go', 'Partage de Fichiers']},
                {'name': 'Famille', 'price': 15.00, 'features': ['500 Go', 'Synchronisation Automatique', '5 Utilisateurs']},
                {'name': 'Professionnel', 'price': 30.00, 'features': ['2 To', 'Sauvegarde Automatique', '10 Utilisateurs', 'Maintenance Prioritaire']}
            ]
        }
    ]

    return render_template('home.html', categories=categories_data)

# Route pour créer un ticket client (Exemple)
@app.route('/client/tickets/create', methods=['GET', 'POST'])
def create_ticket():
    if not session.get('user_id'): # Vérifier si l'utilisateur est connecté
        flash('Veuillez vous connecter pour créer un ticket.', 'danger')
        return redirect(url_for('login'))

    if session.get('is_admin'): # Empêcher les admins de créer des tickets client via cette route
        flash('Les administrateurs ne peuvent pas créer de tickets client directement via cette interface.', 'danger')
        return redirect(url_for('admin_dashboard'))

    user_id = session['user_id']

    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not subject or not message:
            flash('Le sujet et le message ne peuvent pas être vides.', 'danger')
        else:
            new_ticket = SupportTicket(user_id=user_id, subject=subject, message=message)
            db.session.add(new_ticket)
            db.session.commit()
            flash('Votre ticket de support a été créé avec succès !', 'success')
            return redirect(url_for('client_dashboard'))

    return render_template('create_ticket.html')


# Exécute l'application si ce fichier est le fichier principal exécuté
```
