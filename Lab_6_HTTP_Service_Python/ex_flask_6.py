from flask import Flask, jsonify, url_for, request
from flask_sqlalchemy import SQLAlchemy
from ex_flask_pexpect_1 import show_version


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
db = SQLAlchemy(app)
app.app_context().push() # WARNING

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), unique=True)
    loopback = db.Column(db.String(120), unique=True)
    mgmt_ip = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(64))
    vendor = db.Column(db.String(64))
    os = db.Column(db.String(64))

    def get_url(self):
        return url_for('get_device', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'hostname': self.hostname,
            'loopback': self.loopback,
            'mgmt_ip': self.mgmt_ip,
            'role': self.role,
            'vendor': self.vendor,
            'os': self.os
        }

    def import_data(self, data):
        try:
            self.hostname = data['hostname']
            self.loopback = data['loopback']
            self.mgmt_ip = data['mgmt_ip']
            self.role = data['role']
            self.vendor = data['vendor']
            self.os = data['os']
        except KeyError as error:
            raise ValidationError('Invalid device: missing ' + error.args[0])
        return self

@app.route('/devices/', methods=['GET'])
def get_devices():
    return jsonify({'device': [device.get_url() for device in Device.query.all()]})

@app.route('/devices/', methods=['POST'])
def new_device():
    device = Device()
    device.import_data(request.json)
    db.session.add(device)
    db.session.commit()
    return jsonify({}), 201, {'Location': device.get_url()}

@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    return jsonify(Device.query.get_or_404(id).export_data())

@app.route('/devices/<int:id>/version', methods=['GET'])
def get_device_version(id):
    device = Device.query.get_or_404(id)
    hostname = device.hostname
    ip = device.mgmt_ip
    prompt = hostname+"#"
    result = show_version(hostname, prompt, ip, 'admin', 'ciscocisco')
    return jsonify({"version": str(result)})

@app.route('/devices/<device_role>/version', methods=['GET'])
def get_role_version(device_role):
    device_id_list = [device.id for device in Device.query.all() if device.role == device_role]
    # Использование Device.query.all() с большими БД не желательно. Нужно рассматривать вариант с SQL запросом.
    result = {}
    for id in device_id_list:
        device = Device.query.get_or_404(id)
        hostname = device.hostname
        ip = device.mgmt_ip
        prompt = hostname + "#"
        device_result = show_version(hostname, prompt, ip, 'admin', 'ciscocisco')
        result[hostname] = str(device_result)
    return jsonify(result)

@app.route('/devices/<int:id>', methods=['PUT'])
def edit_device(id):
    device = Device.query.get_or_404(id)
    device.import_data(request.json)
    db.session.add(device)
    db.session.commit()
    return jsonify({})

def ValidationError(ValueError):
    pass

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', debug=True)