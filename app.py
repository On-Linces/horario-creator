# app.py
from flask import Flask, render_template, request
import utils.algoritm as algoritm #-- Aquí importas tu archivo de lógica

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    if request.method == 'POST':
        file = request.files['file']
        # Leer los filtros del formulario web
        filtros = {
            'f_traslado': 'traslado' in request.form,
            'f_7am': 'no_7am' in request.form,
            'f_libre': 'dia_libre' in request.form
        }
        
        # Llamamos a la función principal de tu algoritmo
        contenido_html = file.read()
        resultados = algoritm.obtener_mejores_opciones(
            contenido_html, 
            filtros['f_traslado'], 
            filtros['f_7am'], 
            filtros['f_libre']
        )

    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)