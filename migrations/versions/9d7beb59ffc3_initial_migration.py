"""initial_migration

Revision ID: 9d7beb59ffc3
Revises: 
Create Date: 2025-08-25 20:11:18.097341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d7beb59ffc3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("transaction_id", sa.String(), primary_key=True),
        sa.Column("property_code", sa.String(), nullable=False),
        sa.Column("sale_value", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "parties",
        sa.Column("party_id", sa.String(), primary_key=True),
        sa.Column("transaction_id_fk", sa.String(), sa.ForeignKey("transactions.transaction_id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("cpf_cnpj", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
    )

    op.create_table(
        "commissions",
        sa.Column("commission_id", sa.String(), primary_key=True),
        sa.Column("transaction_id_fk", sa.String(), sa.ForeignKey("transactions.transaction_id", ondelete="CASCADE"), nullable=False),
        sa.Column("percentage", sa.Numeric(5, 4), nullable=False),
        sa.Column("calculated_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("paid", sa.Boolean(), default=False, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("commissions")
    op.drop_table("parties")
    op.drop_table("transactions")
    op.execute("DROP TYPE IF EXISTS transactionstatus CASCADE")
    op.execute("DROP TYPE IF EXISTS partytype CASCADE")