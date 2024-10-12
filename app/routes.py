from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import MemberForm
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


@main.route('/add_member', methods=['GET', 'POST'])
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        # Create a new member instance
        new_member = Member(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            join_date=form.join_date.data
        )
        # Add the new member to the database
        db.session.add(new_member)
        db.session.commit()

        # Flash a success message
        flash(f"Member {new_member.name} added successfully!", "success")
        return redirect(url_for('main.add_member'))
    
    return render_template('add_member.html', form=form)