from flask import Flask, jsonify
from config import Config
from models import db

import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Importação dos modelos (User, Campanha, Pessoa, Rifa, Sorteio)
from models import User, Campanha, Pessoa, Rifa, Sorteio

# Criação das tabelas se não existirem
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
