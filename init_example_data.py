from app import create_app, db
from app.models import User, Member, MembershipType, Membership
from werkzeug.security import generate_password_hash

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Admin und regulärer User erstellen
        admin = User(
            username='admin',  
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        user = User(
            username='user', 
            password_hash=generate_password_hash('user123'),
            role='user'
        )
        
        # Vertragsarten erstellen
        membership_types= [
            MembershipType(name='Aktive Mitgliedschaft'),
            MembershipType(name='Passive Mitgliedschaft'),
            MembershipType(name='Ermäßigte Mitgliedschaft')
        ]
        
        # Beispiel-Mitglieder erstellen
        members = [
            Member(id = 1, name='Max Mustermann', email='max@example.com',phone = 123456, join_date = '2021-01-01'),
            Member(id = 2, name='Erika Musterfrau', email='erika@example.com',phone = 234567, join_date = '2022-01-01'),
            Member(id = 3, name='Hans Beispiel', email='hans@example.com', phone = 345678, join_date = '2020-01-01')
        ]

        # Beispiel-Mitgliedschaften erstellen
        memberships = [
            Membership(id = 1, membership_start = '2021-01-01', fk_member = 1, fk_membership_type = 3),
            Membership(id = 2, membership_start = '2022-01-01', fk_member = 2, fk_membership_type = 1),
            Membership(id = 3, membership_start = '2020-01-01', fk_member = 3, membership_end = '2022-12-31', fk_membership_type = 1),
            Membership(id = 4, membership_start = '2023-01-01', fk_member = 1, fk_membership_type = 2)
        ]
        
        db.session.add(admin)
        db.session.add(user)
        db.session.add_all(membership_types)
        db.session.add_all(members)
        db.session.add_all(memberships)
        db.session.commit()
        
        print("Datenbank erfolgreich befüllt!")

if __name__ == '__main__':
    seed_database()
