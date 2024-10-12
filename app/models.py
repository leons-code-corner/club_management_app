from . import db
from flask_login import UserMixin
from datetime import datetime

# Define the Member model
class Member(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    join_date = db.Column(db.Date, default=datetime.utcnow)

    # Relationships
    notes = db.relationship('Note', backref='member', lazy=True)
    files = db.relationship('File', backref='member', lazy=True)
    membership = db.relationship('Membership', backref='member', lazy=True)
    

    def __repr__(self):
        return f'<Member {self.name}>'
    
class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    membership_start = db.Column(db.DateTime, nullable=False)
    membership_end = db.Column(db.DateTime, nullable=False)

    # Relationships
    fk_member = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    fk_membership_type = db.Column(db.Integer, db.ForeignKey('membership_type.id'), nullable=False)

    def __repr__(self):
        return f'<Membership {self.id}>'


class MembershipType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    term_value = db.Column(db.Integer, nullable=False)
    term_interval = db.Column(db.String(10), nullable=False)
    extension_value = db.Column(db.Integer, nullable=False)
    extension_interval = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_interval = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<MembershipType {self.name}>'
    

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    def __repr__(self):
        return f'<Note {self.id} for Member {self.member_id}>'
    
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    def __repr__(self):
        return f'<File {self.file_name} for Member {self.member_id}>'
    
