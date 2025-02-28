from app import create_app, db
from app.models import User, Member, MembershipType
from werkzeug.security import generate_password_hash

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Admin und regulärer User erstellen
        admin = User(
            username='admin', 
            email='admin@example.com', 
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        user = User(
            username='user', 
            email='user@example.com', 
            password_hash=generate_password_hash('user123'),
            is_admin=False
        )
        
        # Vertragsarten erstellen
        memberships = [
            MembershipType(name='Aktive Mitgliedschaft'),
            MembershipType(name='Passive Mitgliedschaft'),
            MembershipType(name='Ermäßigte Mitgliedschaft')
        ]
        
        # Beispiel-Mitglieder erstellen
        members = [
            Member(name='Max Mustermann', email='max@example.com', membership_type=memberships[0]),
            Member(name='Erika Musterfrau', email='erika@example.com', membership_type=memberships[1]),
            Member(name='Hans Beispiel', email='hans@example.com', membership_type=memberships[2])
        ]
        
        db.session.add(admin)
        db.session.add(user)
        db.session.add_all(memberships)
        db.session.add_all(members)
        db.session.commit()
        
        print("Datenbank erfolgreich befüllt!")

if __name__ == '__main__':
    seed_database()
