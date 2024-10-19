from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import MemberForm
from .models import db, Member, Membership, MembershipType
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/members', methods=['GET', 'POST'])
def members():
    search_query = request.args.get('search', '')  # Get search query from URL
    page = request.args.get('page', 1, type=int)  # Get page number from URL
    sort_by = request.args.get('sort_by', 'id')  # Field to sort by (default is 'id‚')
    sort_order = request.args.get('sort_order', 'asc')  # Sort order (default is ascending)

    if search_query:
        # Filter members by name or email if there's a search query
        members = Member.query.filter(
            (Member.name.ilike(f'%{search_query}%')) |
            (Member.email.ilike(f'%{search_query}%'))
        )
    else:
        # If no search query, return all members
        members = Member.query

    # Handle sorting logic
    if sort_by == 'id':
        members = members.order_by(Member.id.asc() if sort_order == 'asc' else Member.id.desc())
    elif sort_by == 'name':
        members = members.order_by(Member.name.asc() if sort_order == 'asc' else Member.name.desc())
    elif sort_by == 'email':
        members = members.order_by(Member.email.asc() if sort_order == 'asc' else Member.email.desc())
    elif sort_by == 'join_date':
        members = members.order_by(Member.join_date.asc() if sort_order == 'asc' else Member.join_date.desc())

    
    pagination = members.paginate(page=page, per_page=10)

    return render_template('members.html', members=pagination.items, search_query=search_query, pagination=pagination, sort_by=sort_by, sort_order=sort_order)


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
