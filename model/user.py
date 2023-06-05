from database import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, role, password):
        self.name = name
        self.email = email
        self.role = role
        self.password = password

    def __repr__(self):
        return f"<User {self.id}: {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }