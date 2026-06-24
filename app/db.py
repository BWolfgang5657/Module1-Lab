"""Database engine + schema creation — Module 04 reference solution.

Builds the SQLAlchemy ``engine`` from a connection string loaded out of the
environment (``.env``), and creates all tables from the models when run as a
script.

里 Debug / Fix — the driver error
    A teammate set ``DATABASE_URL=postgresql://...`` and hit::

        ModuleNotFoundError: No module named 'psycopg2'

    The bare ``postgresql://`` prefix quietly defaults to the *legacy* driver
    ``psycopg2``. This course installs the modern ``psycopg`` (v3) driver, so the
    URL must name it explicitly with ``postgresql+psycopg://``. The dialect in
    the URL and the installed package must match. See ``.env.example``.

Run (creates the tables):
    python -m app.db
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.models import Base

# Load variables from a local ``.env`` file into the environment, if present.
# Credentials live in ``.env`` (git-ignored) — NEVER hard-coded in source.
load_dotenv()

# For Postgres (the lab's target) set DATABASE_URL in .env to, e.g.:
#   postgresql+psycopg://taskflow:secret@localhost:5432/taskflow
# We fall back to a local SQLite file so this reference solution runs and tests
# without a database server. The SAME models and code work against both.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///taskflow.db")

# ``echo=True`` prints the generated SQL (the CREATE TABLE statements), so you
# can read exactly what your models produce — the "ground truth" the lab tells
# you to compare against any AI explanation.
engine = create_engine(DATABASE_URL, echo=True)


def create_all() -> None:
    """Create every TaskFlow table on the configured engine.

    Note: ``create_all`` only creates *missing* tables — it does NOT alter
    existing ones. To pick up a model change in this course DB, drop the table
    and recreate (real projects use migrations instead).
    """
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_all()