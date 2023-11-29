"""empty message

Revision ID: 5d649930b830
Revises: b26adad45c71
Create Date: 2023-11-28 10:29:20.915108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d649930b830'
down_revision: Union[str, None] = 'b26adad45c71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('productdealer', 'product_key')
    op.drop_column('productdealer', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('productdealer', sa.Column('date', sa.DATE(), autoincrement=False, nullable=False))
    op.add_column('productdealer', sa.Column('product_key', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('productdealer_product_key_date_dealer_id_fkey', 'productdealer', 'dealerprice', ['product_key', 'date', 'dealer_id'], ['product_key', 'date', 'dealer_id'])
    # ### end Alembic commands ###
