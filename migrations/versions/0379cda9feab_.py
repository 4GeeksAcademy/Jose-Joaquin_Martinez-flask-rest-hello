"""empty message

Revision ID: 0379cda9feab
Revises: a5cffa318ac2
Create Date: 2024-04-15 19:16:29.354647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0379cda9feab'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('people_id', sa.Integer(), nullable=False),
    sa.Column('character_name', sa.String(length=50), nullable=False),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=15), nullable=True),
    sa.Column('skin_color', sa.String(length=15), nullable=True),
    sa.Column('eye_color', sa.String(length=15), nullable=True),
    sa.Column('birth_year', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('homeworld', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('people_id'),
    sa.UniqueConstraint('character_name')
    )
    op.create_table('planets',
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('planet_name', sa.String(length=50), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=10), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=50), nullable=True),
    sa.Column('terrain', sa.String(length=50), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('planet_id'),
    sa.UniqueConstraint('planet_name')
    )
    op.create_table('vehicles',
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('vehicle_name', sa.String(length=80), nullable=False),
    sa.Column('cargo_capacity', sa.Integer(), nullable=True),
    sa.Column('cost_in_credits', sa.Integer(), nullable=True),
    sa.Column('created', sa.String(length=80), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('manufacturer', sa.String(length=80), nullable=True),
    sa.Column('model', sa.String(length=80), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('vehicle_class', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('vehicle_id'),
    sa.UniqueConstraint('vehicle_name')
    )
    op.create_table('favorites',
    sa.Column('favorite_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.Column('favorite_type', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['people.people_id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.planet_id'], ),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.vehicle_id'], ),
    sa.PrimaryKeyConstraint('favorite_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
        batch_op.drop_column('id')

    op.drop_table('favorites')
    op.drop_table('vehicles')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###
