# Fichier: (à placer à la racine de votre projet)
# Fichier: app.py (à mettre à jour)
# Cette cellule modifie le fichier app.py existant pour ajouter de nouveaux modèles de base de données.
# Insérez ce code APRES la définition de la classe User et AVANT `if __name__ == '__main__':`

# Modèle pour les Catégories de Services (par exemple: Site Web, Gaming, Cloud)
# Fichier: app.py (à mettre à jour)
# Insérez ce code APRÈS les définitions de tous les modèles de base de données et AVANT `if __name__ == '__main__':`

from werkzeug.security import generate_password_hash, check_password_hash

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Vérifier si l'utilisateur existe déjà
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
    # Pour l'instant, nous retournerons un simple formulaire HTML pour le GET
    return '''
        <h1>Inscription</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Nom d'utilisateur" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <input type="submit" value="S'inscrire">
        </form>
        <p>Déjà un compte ? <a href="/login">Connectez-vous ici</a></p>
    '''

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Connexion réussie !', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard')) # Rediriger vers le tableau de bord admin
            else:
                return redirect(url_for('client_dashboard')) # Rediriger vers le tableau de bord client
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    # Pour l'instant, nous retournerons un simple formulaire HTML pour le GET
    return '''
        <h1>Connexion</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Nom d'utilisateur" required><br>
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <input type="submit" value="Se connecter">
        </form>
        <p>Pas encore de compte ? <a href="/register">Inscrivez-vous ici</a></p>
    '''

# Route de déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('home'))

# Route de tableau de bord admin (placeholder)
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('login'))
    return '<h1>Tableau de bord Administrateur</h1><p>Bienvenue, Admin !</p><p><a href="/logout">Déconnexion</a></p>'

# Route de tableau de bord client (placeholder)
@app.route('/client_dashboard')
def client_dashboard():
    if not session.get('user_id'):
        flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if user.is_admin:
        flash('Accès non autorisé.', 'danger') # Admin ne devrait pas être ici, ou devrait être redirigé
        return redirect(url_for('admin_dashboard'))
    return f'<h1>Tableau de bord Client</h1><p>Bienvenue, {user.username} !</p><p><a href="/logout">Déconnexion</a></p>'
