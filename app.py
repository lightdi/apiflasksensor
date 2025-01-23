from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class DadosSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distancia = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route('/api/sensor', methods=['POST'])
def recebe_dados_sensor():
    data = request.json

    if 'distancia' not in data:
        return jsonify({'error': 'distancia não informada'}), 400
    dados_sensor = DadosSensor(distancia=data['distancia'])
    db.session.add(dados_sensor)
    db.session.commit()

    return jsonify({'message': 'Dados salvos com sucesso'}), 201

@app.route('/', methods=['GET'])
def index():
    data = DadosSensor.query.all()  # Fetch all data from the DadosSensor table
    return render_template('index.html', dados_sensor=data)

if __name__ == '__main__':
    app.run()
    #app.run(host='192.168.1.185', port=5000, debug=True)
