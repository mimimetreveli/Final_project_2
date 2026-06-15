import os
from ext import app, db

with app.app_context():
    # Explicitly clear out database file paths to avoid file lock issues
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass

    db.create_all()
    print("Database structure initialized for School Hub successfully.")