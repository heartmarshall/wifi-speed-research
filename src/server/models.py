from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()

class File(db.Model):
    __tablename__ = "File"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {'id': self.id, 'filename': self.filename, 'filepath': self.filepath}

def add_files_from_localstorage():
    localstorage_path = os.path.join(os.getcwd(), 'localstorage')
    for filename in os.listdir(localstorage_path):
        filepath = os.path.join(localstorage_path, filename)
        if os.path.isfile(filepath):
            existing_file = File.query.filter_by(filename=filename).first()
            if not existing_file:
                new_file = File(filename=filename, filepath=filepath)
                db.session.add(new_file)
    db.session.commit()

