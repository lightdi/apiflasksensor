from flask import Flask, request, jsonify, render_template
import sqlite3 as sqlite


app = Flask(__name__)

ip_local = '192.168.1.101'
porta_Local = 5000

def cria_tabela():
    conn = sqlite.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados_sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipe TEXT NOT NULL,
            distancia FLOAT NOT NULL,
            envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

cria_tabela()


class DadosSensor():
    def __init__(self, equipe, distancia, id=None, envio=None):
        self.equipe = equipe
        self.distancia = distancia
        self.id = id
        self.envio = envio
    
    def salvar(self):
        conn = sqlite.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dados_sensor (equipe, distancia) VALUES (?, ?)
        ''', (self.equipe, self.distancia))
        conn.commit()
        conn.close()
    
    @staticmethod
    def buscar_todos():
        conn = sqlite.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dados_sensor order by id desc')
        dados = cursor.fetchall()
        objetos = []
        for dado in dados:
            objetos.append(DadosSensor(equipe=dado[1], distancia=dado[2], id=dado[0], envio=dado[3]))
        conn.close()
        return objetos
    


@app.route('/api/sensor', methods=['POST'])
def recebe_dados_sensor():
    data = request.json
    print(data)
   
    if 'distancia' not in data or 'equipe' not in data:
        return jsonify({'error': 'equipe ou distancia não informada'}), 400

    dados_sensor = DadosSensor(equipe=data['equipe'], distancia=data['distancia'])
    dados_sensor.salvar()

    return jsonify({'message': 'Dados salvos com sucesso'}), 201

@app.route('/', methods=['GET'])
def index():
    dados = DadosSensor.buscar_todos() 

    print(dados)
    return render_template('index.html', dados_sensor=dados)

if __name__ == '__main__':
    app.run(host=ip_local, port=porta_Local, debug=True)