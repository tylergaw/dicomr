"""empty message

Revision ID: eaf3177934e8
Revises: 27045c5738b8
Create Date: 2017-03-20 21:41:18.448182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaf3177934e8'
down_revision = '27045c5738b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('records', sa.Column('created_at', sa.Date(), nullable=True))
    op.add_column('records', sa.Column('study_uid', sa.String(), nullable=True))
    op.add_column('records', sa.Column('updated_at', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('records', 'updated_at')
    op.drop_column('records', 'study_uid')
    op.drop_column('records', 'created_at')
    # ### end Alembic commands ###
