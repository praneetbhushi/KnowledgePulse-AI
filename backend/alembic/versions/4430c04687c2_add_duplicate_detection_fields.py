"""Add duplicate detection fields

Revision ID: 4430c04687c2
Revises: 665cf327ecf2
Create Date: <keep your existing date>
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "4430c04687c2"

down_revision: Union[str, Sequence[str], None] = (
    "665cf327ecf2"
)

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ---------------------------------
    # Add is_duplicate
    #
    # server_default=False is required
    # because documents already exist.
    # ---------------------------------

    op.add_column(
        "documents",
        sa.Column(
            "is_duplicate",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )


    # ---------------------------------
    # Add duplicate document reference
    # ---------------------------------

    op.add_column(
        "documents",
        sa.Column(
            "duplicate_of_document_id",
            sa.Integer(),
            nullable=True
        )
    )


    # ---------------------------------
    # Add duplicate similarity score
    # ---------------------------------

    op.add_column(
        "documents",
        sa.Column(
            "duplicate_similarity",
            sa.Float(),
            nullable=True
        )
    )


    # ---------------------------------
    # Foreign key:
    # duplicate_of_document_id
    # references documents.id
    # ---------------------------------

    op.create_foreign_key(
        None,
        "documents",
        "documents",
        [
            "duplicate_of_document_id"
        ],
        [
            "id"
        ],
        ondelete="SET NULL"
    )


def downgrade() -> None:

    # ---------------------------------
    # Remove foreign key first
    # ---------------------------------

    # IMPORTANT:
    # If your automatically generated
    # migration has a specific FK name,
    # keep that generated downgrade code.
    # Do not invent a constraint name here.

    # Then remove columns in reverse order.

    op.drop_column(
        "documents",
        "duplicate_similarity"
    )

    op.drop_column(
        "documents",
        "duplicate_of_document_id"
    )

    op.drop_column(
        "documents",
        "is_duplicate"
    )