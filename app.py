# Fichier: app.py (à mettre à jour)
# Insérez ce code APRÈS les routes d'authentification (register, login, logout) et AVANT `if __name__ == '__main__':`

# Modifie la route d'accueil pour afficher les catégories de services et leurs plans
@app.route('/')
def home():
    # Données de démonstration pour les catégories et les plans
    # Dans une application réelle, ces données viendraient de la base de données
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

    # Récupérer les catégories et plans de la base de données si disponibles
    # Si la base de données est remplie avec des catégories et plans, vous pouvez les charger ici.
    # Exemple (décommenter si vous avez des données en DB):
    # categories_db = ServiceCategory.query.all()
    # if categories_db:
    #     categories_data = []
    #     for cat_db in categories_db:
    #         plans_for_cat = []
    #         for plan_db in cat_db.plans:
    #             plans_for_cat.append({
    #                 'name': plan_db.name,
    #                 'price': plan_db.price,
    #                 'features': plan_db.description.split(', ') if plan_db.description else [], # Supposons que les features sont séparées par des virgules
    #                 'elite_maintenance': plan_db.elite_maintenance
    #             })
    #         categories_data.append({
    #             'name': cat_db.name,
    #             'description': cat_db.description,
    #             'plans': plans_for_cat
    #         })

    return render_template('home.html', categories=categories_data)
