import tensorflow as tf 
import tensorflow_hub as hub
import tf_keras
import matplotlib.pyplot as plt

imagen_tam = 224
batch_tam = 32
epocas = 5
n_clases = 2

#Obtenemos el modelo
url = "https://www.kaggle.com/models/google/mobilenet-v2/TensorFlow2/tf2-preview-feature-vector/4"
#input_shape(base,altura,canales (3 indican RGB))
mobilenet2 = hub.KerasLayer(url,input_shape=(imagen_tam,imagen_tam,3))
#Como es un modelo pre entrenado debemos congelarlo
mobilenet2.trainable = False

train_dir = "dataset/train"
test_dir = "dataset/test"

#Creamos el set de datos
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(imagen_tam,imagen_tam),
    batch_size=batch_tam,
    label_mode='int'
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(imagen_tam,imagen_tam),
    batch_size=batch_tam,
    label_mode='int'
)

#Definimos el modelo y añadimos una capa de salida con la función softmax (para clasificiación)
modelo = tf_keras.models.Sequential([
    mobilenet2,
    tf_keras.layers.Dense(n_clases,activation='softmax')
])

#Compilamos el modelo
modelo.compile(
    optimizer='adam',
    loss = 'sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#Mostrar datos del modelo
modelo.summary()

#Entrenamos el modelo
historial = modelo.fit(
    train_dataset,
    validation_data=test_dataset,
    epochs=epocas
)

#Guardamos el modelo
modelo.save("clasificador.keras")

#Grafico del history
plt.figure(figsize=(12,5))

#Perdida
plt.subplot(1,2,1)
plt.plot(historial.history['loss'], label='Pérdida en entrenamiento')
plt.plot(historial.history['val_loss'], label='Pérdida en validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.title('Pérdida durante el entrenamiento y la validación')

#precision
plt.subplot(1, 2, 2)
plt.plot(historial.history['accuracy'], label='Precisión en entrenamiento')
plt.plot(historial.history['val_accuracy'], label='Precisión en validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.title('Precisión durante el entrenamiento y la validación')

plt.tight_layout()
plt.show()