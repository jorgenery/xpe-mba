import joblib
from flask import Flask, request, jsonify, render_template
from sklearn.ensemble import RandomForestRegressor
from sklearn import datasets
import numpy as np
from datetime import datetime
import sys

app = Flask(__name__,template_folder=".")

def previsao_passageiro(lista_valores_formulario):
    # RFregressor = RandomForestRegressor(n_estimators = 90, random_state = 0)
    modelo_salvo = joblib.load('modelo-rfr.joblib')
    prever = np.array(lista_valores_formulario).reshape(1,3)
    resultado = modelo_salvo.predict(prever)    
    return round(resultado[0])

@app.route('/')
def home():
    return render_template('formulario.html')

def uf_tipo_dia(d):
    tipo_dia = {
        0: 3,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 2
    }

def prepara(lista_recebida):
    data_str = lista_recebida[0]
    data = datetime.strptime(data_str, '%Y-%m-%d')
    diasemana = data.weekday()
    tipodia = uf_tipo_dia(diasemana)
    hora = lista_recebida[1]
    return [tipodia,hora,diasemana]

@app.route('/prev_passageiros',methods=['POST','GET'])
def result():    
    linha = request.args.get("linha")
    data = request.args.get("data")
    hora = request.args.get("hora")
    lista_preparada = prepara([data,hora,linha])
    previsao = previsao_passageiro(lista_preparada)
    return render_template("resultado.html",previsao=previsao)

if __name__ == "__main__":
    app.run(debug=True)