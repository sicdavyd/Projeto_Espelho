from flask import Flask, request, render_template, redirect, url_for
import tensorflow as tf 
from tensorflow.keras.metrics import MeanAbsoluteError
import numpy as np  
import os
import uuid
from PIL import Image
from ultralytics import YOLO
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
custom_objects = {
    'mae': MeanAbsoluteError()
}
modelo = tf.keras.models.load_model('modelo.h5', custom_objects=custom_objects)
modelo_yolo = YOLO('yolov5su.pt')
def detecta_pessoa(imagem_path, limiar_conf=0.3):
    """
    Retorna True se a imagem contiver ao menos uma pessoa detectada com confiança suficiente.
    """
    resultados = modelo_yolo(imagem_path)[0]

    for cls_id, conf in zip(resultados.boxes.cls, resultados.boxes.conf):
        if int(cls_id) == 0 and conf >= limiar_conf:  # classe 0 = "person"
            return True
    return False

def tratar_imagem(imagem):
    imagem = np.array(imagem) / 255.0
    if imagem.shape[-1] == 4:
        imagem = imagem[..., :3]
    imagem_tratada = tf.image.resize(imagem,(224, 224))
    img = tf.expand_dims(imagem_tratada, axis=0)
    return img

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        arquivo = request.files.get('imagem')
        
        if arquivo:
            # Gera um nome único para o arquivo
            nome_arquivo = str(uuid.uuid4()) + os.path.splitext(arquivo.filename)[-1]
            path_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            arquivo.save(path_arquivo)
            
            # Usa o caminho salvo no YOLO e no tratamento
            if detecta_pessoa(path_arquivo):
                imagem = Image.open(path_arquivo).convert('RGB') 
                imagem_tratada = tratar_imagem(imagem)  
                predicao = modelo.predict(imagem_tratada)
                idade = float(predicao[0][0])
                genero_prob = float(predicao[1][0])
                genero = "Mulher" if genero_prob > 0.5 else "Homem"
                resultado = f'Idade: {idade:.0f} anos.'+f'\nGênero: {genero}.'
            else:
                resultado = "Imagem inválida: nenhuma pessoa detectada."
                nome_arquivo = 'default.jpg'
            
            return render_template('resultado.html',
                                   resultado=resultado,
                                   imagem=url_for('static', filename='uploads/' + nome_arquivo))
        
        else:
            resultado = 'Nenhum arquivo enviado.'
            return render_template('resultado.html',
                                   resultado=resultado,
                                   imagem=url_for('static', filename='uploads/default.jpg'))

    return render_template('index.html', resultado=resultado)
    ...
if __name__ == "__main__":
    app.run(debug=True)