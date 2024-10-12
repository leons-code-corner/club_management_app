"""Initial migration with membership tables

Revision ID: 1edcdacc8c48
Revises: 
Create Date: 2024-10-12 20:09:19.332317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1edcdacc8c48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('join_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('membership_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('term_value', sa.Integer(), nullable=False),
    sa.Column('term_interval', sa.String(length=10), nullable=False),
    sa.Column('extension_value', sa.Integer(), nullable=False),
    sa.Column('extension_interval', sa.String(length=10), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('price_interval', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('membership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('membership_start', sa.DateTime(), nullable=False),
    sa.Column('membership_end', sa.DateTime(), nullable=False),
    sa.Column('fk_member', sa.Integer(), nullable=False),
    sa.Column('fk_membership_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fk_member'], ['member.id'], ),
    sa.ForeignKeyConstraint(['fk_membership_type'], ['membership_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    op.drop_table('membership')
    op.drop_table('file')
    op.drop_table('membership_type')
    op.drop_table('member')
    # ### end Alembic commands ###
