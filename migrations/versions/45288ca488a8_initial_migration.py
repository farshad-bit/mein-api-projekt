"""Initial migration

Revision ID: 45288ca488a8
Revises: 
Create Date: 2024-09-27 16:24:57.274184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45288ca488a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('title', sa.String(length=10), nullable=True),
    sa.Column('physician', sa.String(length=100), nullable=True),
    sa.Column('ancestry', sa.String(length=100), nullable=True),
    sa.Column('inconsistency', sa.String(length=255), nullable=True),
    sa.Column('eyeid', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_patients_eyeid'), ['eyeid'], unique=True)
        batch_op.create_index(batch_op.f('ix_patients_last_name'), ['last_name'], unique=False)

    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(length=255), nullable=False),
    sa.Column('date_taken', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.String(length=255), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.create_index('idx_tags', ['tags'], unique=False)
        batch_op.create_index(batch_op.f('ix_images_patient_id'), ['patient_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_images_patient_id'))
        batch_op.drop_index('idx_tags')

    op.drop_table('images')
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_patients_last_name'))
        batch_op.drop_index(batch_op.f('ix_patients_eyeid'))

    op.drop_table('patients')
    # ### end Alembic commands ###
