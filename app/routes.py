from flask import Blueprint, render_template, redirect, url_for
from .models import db, Member, Membership, MembershipType
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/members')
def members():
    # Fetch all members from the database
    members = Member.query.all()
    return render_template('members.html', members=members)


@main.route('/add_member')
def add_member():
    # Create a test membership type
    basic_type = MembershipType(
        name="Basic Membership",
        term_value=1,
        term_interval="year",
        extension_value=1,
        extension_interval="year",
        price=99.99,
        price_interval="year"
    )
    db.session.add(basic_type)
    db.session.commit()

    # Add a new member
    new_member = Member(
        name="Jane Doe",
        email="jane@example.com",
        phone="987654321",
        address="456 Club Ave, City",
        join_date=datetime(2023, 1, 1)
    )
    db.session.add(new_member)
    db.session.commit()

    # Add a membership for this member
    membership = Membership(
        membership_start=datetime(2023, 1, 1),
        membership_end=datetime(2024, 1, 1),
        fk_member=new_member.id,
        fk_membership_type=basic_type.id
    )
    db.session.add(membership)
    db.session.commit()

    return redirect(url_for('main.index'))