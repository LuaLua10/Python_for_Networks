from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'You are at Index'

@app.route('/routers/')
def routers():
    return 'You are at routers()'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=49160, debug=True)