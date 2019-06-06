import os
from app import create_app, db
from app.models import User, TypeUser, AdSense, Articles, Log
from flask_migrate import Migrate

app = create_app()
<<<<<<< HEAD
migrate = Migrate(app, db)
=======
string = 'ViniciusViadao'
>>>>>>> 3ae36097188f7dd41406aeab5bd3db46fc0f6c5c
