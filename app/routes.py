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

@main.route('/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Member.query.get_or_404(id)  # Get the member or return 404 if not found
    form = MemberForm(obj=member)  # Pre-fill the form with the member's data

    if form.validate_on_submit():
        # Update member details with form data
        member.name = form.name.data
        member.email = form.email.data
        member.phone = form.phone.data
        member.address = form.address.data
        member.join_date = form.join_date.data
        
        # Commit the changes to the database
        db.session.commit()

        # Flash a success message
        flash(f"Member {member.name} updated successfully!", "success")
        return redirect(url_for('main.edit_member', id=member.id))
    
    return render_template('edit_member.html', form=form, member=member)

@main.route('/delete_member/<int:id>', methods=['POST'])
def delete_member(id):
    member = Member.query.get_or_404(id)  # Get the member or return 404 if not found

    # Delete the member from the database
    db.session.delete(member)
    db.session.commit()

    # Flash a success message
    flash(f"Member {member.name} has been deleted.", "success")

    return redirect(url_for('main.members'))
