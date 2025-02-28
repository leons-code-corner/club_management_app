from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    membership = db.relationship('Membership', backref='member',cascade = 'all, delete-orphan',lazy=True)
    

    def __repr__(self):
        return f'<Member {self.name}>'
    
class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    membership_start = db.Column(db.DateTime, nullable=False)
    membership_end = db.Column(db.DateTime, nullable=True)

    # Relationships
    fk_member = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    fk_membership_type = db.Column(db.Integer, db.ForeignKey('membership_type.id',ondelete = 'CASCADE'), nullable=False)

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

    # Relationships
    memberships = db.relationship('Membership', backref='membership_type', lazy=True)

    @staticmethod
    def edit(id):
        membership_type = MembershipType.query.get_or_404(id)
        form = MembershipTypeForm(obj=membership_type)

        if form.validate_on_submit():
            membership_type.name = form.name.data
            membership_type.term_value = form.term_value.data
            membership_type.term_interval = form.term_interval.data
            membership_type.extension_value = form.extension_value.data
            membership_type.extension_interval = form.extension_interval.data
            membership_type.price = form.price.data
            membership_type.price_interval = form.price_interval.data

            db.session.commit()
            flash('Membership type updated successfully!', 'success')
            return redirect(url_for('main.membership_types'))

        return render_template('edit_membership_type.html', form=form, membership_type=membership_type)

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
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), name='fk_user_member', nullable=True)

    member = db.relationship("Member", backref="user", uselist=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
