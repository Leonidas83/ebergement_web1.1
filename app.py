# Fichier: (à placer à la racine de votre projet)
# Fichier: app.py (à mettre à jour)
# Cette cellule modifie le fichier app.py existant pour ajouter de nouveaux modèles de base de données.
# Insérez ce code APRES la définition de la classe User et AVANT `if __name__ == '__main__':`

# Modèle pour les Catégories de Services (par exemple: Site Web, Gaming, Cloud)
class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    plans = db.relationship('ServicePlan', backref='category', lazy=True)

    def __repr__(self):
        return f"ServiceCategory('{self.name}')"

# Modèle pour les Plans de Services (par exemple: Basique, Premium, Elite pour chaque catégorie)
class ServicePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    # Exemple de fonctionnalité spécifique au plan (ex: maintenance prioritaire)
    elite_maintenance = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"ServicePlan('{self.name}', '{self.price}', Category: '{self.category.name}')"

# Modèle pour les Abonnements Clients (liaison entre User et ServicePlan)
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('service_plan.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime, nullable=True) # Null for indefinite subscription
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='subscriptions', lazy=True)
    plan = db.relationship('ServicePlan', backref='subscriptions', lazy=True)

    def __repr__(self):
        return f"Subscription(User: '{self.user.username}', Plan: '{self.plan.name}', Active: {self.is_active})"

# Modèle pour les Tickets de Support Client
class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Ouvert') # Ex: Ouvert, En cours, Résolu, Fermé
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    # L'admin qui a pris en charge le ticket (peut être null si pas encore attribué)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    user = db.relationship('User', foreign_keys=[user_id], backref='tickets_created', lazy=True)
    assigned_admin = db.relationship('User', foreign_keys=[admin_id], backref='tickets_assigned', lazy=True)

    def __repr__(self):
        return f"SupportTicket(ID: {self.id}, Subject: '{self.subject}', Status: '{self.status}', User: '{self.user.username}')"
