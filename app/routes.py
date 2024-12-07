from flask import Blueprint, render_template, redirect, url_for, flash, request, Response
from flask_login import login_user, logout_user, login_required
from .forms import MemberForm, LoginForm, MembershipTypeForm, MembershipForm, MemberFilterForm
from .models import db, Member,User, Membership, MembershipType
from .decorators import role_required
from datetime import datetime, timedelta
import csv, io

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/members', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def members():
    form = MemberFilterForm()

    # Populate membership type choices (add "All" as default)
    form.membership_type.choices = [(0, 'All Membership Types')] + [(m.id, m.name) for m in MembershipType.query.all()]

    search_query = request.args.get('search', '')  # Get search query from URL
    page = request.args.get('page', 1, type=int)  # Get page number from URL
    sort_by = request.args.get('sort_by', 'id')  # Field to sort by (default is 'id‚')
    sort_order = request.args.get('sort_order', 'asc')  # Sort order (default is ascending)

    # Base query for members
    members = Member.query

    # If a membership type is selected for filtering
    if form.validate_on_submit() and form.membership_type.data != 0:
        selected_type_id = form.membership_type.data
        # Join with memberships and filter by the selected type
        members= members.join(Membership).filter(Membership.fk_membership_type == selected_type_id)


    if search_query:
        # Filter members by name or email if there's a search query
        members = Member.query.filter(
            (Member.name.ilike(f'%{search_query}%')) |
            (Member.email.ilike(f'%{search_query}%'))
        )

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

    return render_template('members.html', members=pagination.items, search_query=search_query, pagination=pagination, 
                           sort_by=sort_by, sort_order=sort_order, form=form)


@main.route('/add_member', methods=['GET', 'POST'])
@login_required
@role_required('admin')
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
@login_required
@role_required('admin')
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
@login_required
@role_required('admin')
def delete_member(id):
    member = Member.query.get_or_404(id)  # Get the member or return 404 if not found

    # Delete the member from the database
    db.session.delete(member)
    db.session.commit()

    # Flash a success message
    flash(f"Member {member.name} has been deleted.", "success")

    return redirect(url_for('main.members'))

@main.route('/export_members')
@login_required
@role_required('admin')
def export_members():
    # Fetch all members from the database
    members = Member.query.all()

    # Create the CSV response
    def generate():
        # Create the CSV writer
        data = io.StringIO()
        csv_writer = csv.writer(data)

        # Write the header row
        csv_writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Address', 'Join Date'])

        # Write member data rows
        for member in members:
            csv_writer.writerow([member.id, member.name, member.email, member.phone, member.address, member.join_date.strftime('%Y-%m-%d')])
        
        data.seek(0)
        return data.getvalue()

    response = Response(generate(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='members.csv')
    return response

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Log in the user
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@main.route('/member/<int:id>', methods=['GET'])
@login_required
@role_required('admin')
def member_profile(id):
    member = Member.query.get_or_404(id)
    memberships = Membership.query.filter_by(fk_member=member.id).all()
    return render_template('member_profile.html', member=member, memberships=memberships)

@main.route('/assign_membership/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')  # Only admins can assign memberships
def assign_membership(id):
    member = Member.query.get_or_404(id)
    form = MembershipForm()

    # Populate the membership type dropdown
    form.membership_type.choices = [(m.id, m.name) for m in MembershipType.query.all()]

    if form.validate_on_submit():
        # Create a new membership
        new_membership = Membership(
            fk_member=member.id,
            fk_membership_type=form.membership_type.data,
            membership_start=form.membership_start.data,
            membership_end=form.membership_end.data
        )
        db.session.add(new_membership)
        db.session.commit()

        flash(f"Membership for {member.name} assigned successfully!", 'success')
        return redirect(url_for('main.member_profile', id=member.id))

    return render_template('assign_membership.html', form=form, member=member)

@main.route('/membership_types', methods=['GET'])
@login_required
@role_required('admin')
def membership_types():
    membership_types = MembershipType.query.all()
    return render_template('membership_types.html', membership_types=membership_types)


@main.route('/create_membership_type', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_membership_type():
    form = MembershipTypeForm()
    if form.validate_on_submit():
        new_type = MembershipType(
            name=form.name.data,
            term_value=form.term_value.data,
            term_interval=form.term_interval.data,
            extension_value=form.extension_value.data,
            extension_interval=form.extension_interval.data,
            price=form.price.data,
            price_interval=form.price_interval.data
        )
        db.session.add(new_type)
        db.session.commit()

        flash('New membership type created successfully!', 'success')
        return redirect(url_for('main.membership_types'))

    return render_template('create_membership_type.html', form=form)

@main.route('/edit_membership_type/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_membership_type(id):
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

@main.route('/delete_membership_type/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_membership_type(id):
    membership_type = MembershipType.query.get_or_404(id)
    db.session.delete(membership_type)
    db.session.commit()

    flash('Membership type deleted successfully!', 'success')
    return redirect(url_for('main.membership_types'))