from ultralytics import YOLO
import cv2
import tensorflow as tf
from tensorflow.keras.metrics import MeanAbsoluteError
import numpy as np  
import os
import uuid
from PIL import Image

custom_objects = {
    'mae': MeanAbsoluteError()
}
meu_modelo = modelo = tf.keras.models.load_model('modelo.h5', custom_objects=custom_objects)
modelo_yolo = YOLO('yolov5s.pt')

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
    if detecta_pessoa(imagem):
        imagem = Image.open(imagem).convert('RGB')
        imagem = np.array(imagem) / 255.0
        if imagem.shape[-1] == 4:
            imagem = imagem[..., :3]
        imagem_tratada = tf.image.resize(imagem,(224, 224))
        img = tf.expand_dims(imagem_tratada, axis=0)
        return img
    else:
        return 'imagem invalida'

caminho = r'C:\Users\Davyd\Desktop\EmoVision\EmoVisionProjeto\dataset_idade\ImagensTeste'
path_imagens = [img for img in os.listdir(caminho) if img.endswith('.jpeg')]
for img in path_imagens:
    print(f'{img}')

img = caminho +'/'+ path_imagens[-3]
resulta = tratar_imagem(img)
predicao = meu_modelo.predict(resulta)
idade = float(predicao[0][0])
genero_prob = float(predicao[1][0])
genero = "Mulher" if genero_prob > 0.5 else "Homem"
resultado = f'Idade: {idade:.0f} anos.\nGênero: {genero}.'
print(resultado)


