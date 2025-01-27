import tensorflow as tf
import numpy as np
import tensorflow_hub as hub
import tf_keras

# Cargar el modelo
imagen_tam = 224
batch_tam = 32

modelo = tf_keras.models.load_model("clasificador.keras",custom_objects={'KerasLayer': hub.KerasLayer})

# Ruta de la imagen a predecir
ruta_imagen = "pruebas.jpg"

image = tf.keras.utils.load_img(ruta_imagen,target_size=(224, 224,3))
input_arr = tf.keras.utils.img_to_array(image)
input_arr = np.array([input_arr])  # Convert single image to a batch.

prediccion = modelo.predict(input_arr)
clase_predicha = np.argmax(prediccion, axis=1)
if clase_predicha == 0:
    print("Potencialmente lunar")
else:
    print("Potencialmente Cancer")
print(f"Prediccion {prediccion}")