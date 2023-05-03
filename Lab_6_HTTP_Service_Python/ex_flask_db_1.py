from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создаем Flask-приложение, загружаем конфигурацию и создаем обьект SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
db = SQLAlchemy(app)
app.app_context().push() # WARNING

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(120), index=True)
    vendor = db.Column(db.String(40))

    def __init__(self, hostname, vendor):
        self.hostname = hostname
        self. vendor = vendor

    def __repr__(self):
        return '<Device %r>' % self.hostname

if __name__ == '__main__':
    db.create_all()
    r1 = Device('msk-dc1-core1', 'Juniper')
    r2 = Device('spb-dc1-core1', 'Cisco')
    db.session.add(r1)
    db.session.add(r2)
    db.session.commit()