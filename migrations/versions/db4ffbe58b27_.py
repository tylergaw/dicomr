"""empty message

Revision ID: db4ffbe58b27
Revises: 
Create Date: 2017-03-19 20:53:12.264383

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'db4ffbe58b27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.String(), nullable=True),
    sa.Column('image_thumb_name', sa.String(), nullable=True),
    sa.Column('dicom_name', sa.String(), nullable=True),
    sa.Column('dicom_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('records')
    # ### end Alembic commands ###
