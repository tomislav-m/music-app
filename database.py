from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask

app = Flask(__name__)

DB_URL = 'postgresql://postgres:postgres@localhost:5432/Music'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    image_url = db.Column(db.String, unique=False, nullable=True)


if __name__ == '__main__':
    manager.run()
