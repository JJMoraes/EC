import os
from app import create_app, db
from app.models import User, Role, AdSense, Article, Log
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)