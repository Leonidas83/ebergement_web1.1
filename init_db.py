```python
from app import app, db, User, ServiceCategory, ServicePlan, Subscription, SupportTicket
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print('Database tables created.')

    # Ajout d'un admin initial si la base est vide pour faciliter le test
    if User.query.filter_by(username='admin').first() is None:
        admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('adminpassword', method='pbkdf2:sha256'), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created.')

    # Ajout de données de démonstration pour ServiceCategory et ServicePlan si la base est vide
    if ServiceCategory.query.count() == 0:
        web_cat = ServiceCategory(name='Hébergement de Sites Web', description='Idéal pour les entreprises et les portfolios.')
        gaming_cat = ServiceCategory(name='Hébergement de Jeux', description='Créez votre propre serveur pour jouer avec vos amis.')
        cloud_cat = ServiceCategory(name='Stockage Cloud', description='Stockez vos fichiers en toute sécurité et accédez-y de partout.')
        db.session.add_all([web_cat, gaming_cat, cloud_cat])
        db.session.commit()

        plan1 = ServicePlan(name='Basique Web', description='10 Go SSD, 1 Domaine, Support Standard', price=9.99, category=web_cat)
        plan2 = ServicePlan(name='Pro Gaming', description='8 Go RAM, 4 CPU Cores, Protection DDoS Avancée', price=29.99, category=gaming_cat, elite_maintenance=True)
        plan3 = ServicePlan(name='Cloud Pro', description='2 To, Sauvegarde Automatique, 10 Utilisateurs', price=30.00, category=cloud_cat, elite_maintenance=True)
        db.session.add_all([plan1, plan2, plan3])
        db.session.commit()
        print('Demo categories and plans created.')

    # Création d'un utilisateur de test si la base est vide (non-admin)
    if User.query.filter_by(username='testuser').first() is None:
        test_user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='pbkdf2:sha256'), is_admin=False)
        db.session.add(test_user)
        db.session.commit()
        print('Test user created.')
        # Ajoutez un abonnement pour l'utilisateur de test si des plans existent
        if ServicePlan.query.first():
            sub1 = Subscription(user_rel=test_user, plan_rel=ServicePlan.query.filter_by(name='Basique Web').first(), is_active=True)
            db.session.add(sub1)
            db.session.commit()
            print('Subscription for test user created.')

        # Ajoutez un ticket de support pour l'utilisateur de test
        ticket1 = SupportTicket(user_ticket_rel=test_user, subject='Problème de connexion au site', message='Je ne peux pas accéder à mon site web depuis ce matin.', status='Ouvert')
        db.session.add(ticket1)
        db.session.commit()
        print('Support ticket for test user created.')

    print('Database initialization and demo data insertion complete.')
```
