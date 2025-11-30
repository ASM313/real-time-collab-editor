"""
Database initialization and migration helper.
Run this to create tables if they don't exist automatically.
"""

from app.db import engine, Base
from app.models import Room

def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

if __name__ == "__main__":
    create_tables()
