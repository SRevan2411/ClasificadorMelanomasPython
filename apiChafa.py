from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import tensorflow_hub as hub
import tf_keras
import requests
from io import BytesIO
from PIL import Image

# Inicializar Flask
app = Flask(__name__)

# Configuración del modelo
imagen_tam = 224
modelo = tf_keras.models.load_model("clasificador.keras", custom_objects={'KerasLayer': hub.KerasLayer})

# Función para preprocesar la imagen
def procesar_imagen(url_imagen):
    # Descargar la imagen desde la URL
    respuesta = requests.get(url_imagen)
    imagen = Image.open(BytesIO(respuesta.content))
    
    # Ajustar tamaño y convertir a array
    imagen = imagen.resize((imagen_tam, imagen_tam))
    input_arr = tf.keras.utils.img_to_array(imagen)
    input_arr = np.array([input_arr])  # Convertir la imagen en un lote de una sola imagen
    return input_arr

# Ruta de predicción
@app.route('/predict', methods=['POST'])
def predict():
    # Obtener URL de la imagen del JSON de la petición
    datos = request.get_json()
    url_imagen = datos.get("url")
    
    # Validar URL
    if not url_imagen:
        return jsonify({"error": "No se proporcionó URL de imagen"}), 400
    
    # Procesar la imagen y realizar la predicción
    try:
        input_arr = procesar_imagen(url_imagen)
        prediccion = modelo.predict(input_arr)
        clase_predicha = np.argmax(prediccion, axis=1)
        
        # Interpretar el resultado
        resultado = "Potencialmente lunar" if clase_predicha == 0 else "Potencialmente Cancer"
        
        # Devolver la predicción en formato JSON
        return jsonify({
            "prediccion": prediccion.tolist(),
            "clase": resultado
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar la API
if __name__ == '__main__':
    app.run(debug=True)