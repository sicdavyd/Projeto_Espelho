import  torch
from torchvision import transforms
import tensorflow as tf
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
from pathlib import Path
from ultralytics import YOLO
from tensorflow.keras.metrics import MeanAbsoluteError
import logging

def draw_conf_matrix_clas_report(y_true, y_pred, name_labels='', name_model=''):

    c_m = confusion_matrix(y_true, y_pred)
    conf_matrix = pd.DataFrame(c_m, name_labels, name_labels)

    plt.figure(figsize = (9,9))

    group_counts = ['{0:0.0f}'.format(value) for value in
                  conf_matrix.values.flatten()]
    group_percentages = ['{0:.1%}'.format(value) for value in
                        conf_matrix.div(np.sum(conf_matrix, axis=1), axis=0).values.flatten()]

    labels = ['{}\n{}'.format(v1,v2) for v1,v2 in zip(group_counts, group_percentages)]

    labels = np.asarray(labels).reshape(c_m.shape)
    sns.set(font_scale=1.8)
    chart = sns.heatmap(conf_matrix,
              cbar=False ,
              annot=labels,
              square=True,
              fmt='',
              annot_kws={ 'size': 18},
              cmap="Blues",
              )
    chart.set_xticklabels(name_labels)
    chart.set_yticklabels(name_labels, rotation=360, verticalalignment='center')
    plt.savefig('confusion_matrix_{}.png'.format(name_model), bbox_inches='tight', pad_inches=0)
    
def tf_processing(fp):
    def preprocess_input(x):
        x_temp = np.copy(x)
        x_temp = x_temp[..., ::-1]
        x_temp[..., 0] -= 91.4953
        x_temp[..., 1] -= 103.8827
        x_temp[..., 2] -= 131.0912
        return x_temp

    def get_img_tf(path):
        img = tf.keras.utils.load_img(
                    path,
                    target_size=(224,224),
                )
        img = tf.keras.utils.img_to_array(img)
        img = preprocess_input(img)
        img = np.array([img])
        return img
    return get_img_tf(fp)


def pth_processing(fp):
    class PreprocessInput(torch.nn.Module):
        def init(self):
            super(PreprocessInput, self).init()

        def forward(self, x):
            x = x.to(torch.float32)
            x = torch.flip(x, dims=(0,))
            x[0, :, :] -= 91.4953
            x[1, :, :] -= 103.8827
            x[2, :, :] -= 131.0912
            return x

    def get_img_torch(path):
        img = Image.open(path)
        img = img.resize((224, 224), Image.Resampling.NEAREST)
        
        ttransform = transforms.Compose([
            transforms.PILToTensor(),
            PreprocessInput()
        ])
        
        img = ttransform(img)
        img = torch.unsqueeze(img, 0)
        return img
    return get_img_torch(fp)

dict_name_labels = {
    0: 'Neutro',
    1: 'Felicidade',
    2: 'Tristeza',
    3: 'Surpresa',
    4: 'Medo',
    5: 'Nojo',
    6: 'Raiva'
}

#Caminho do modelo treinado
caminho_raiz = Path(__file__).absolute().parent
caminho_pth = caminho_raiz / "models" / "torchscript_model_0_66_49_wo_gl.pth"
pth_model = torch.jit.load(caminho_pth)

def rotular_imagens(caminho_imagem:str, dict_name_labels=dict_name_labels) -> tuple:
    imagem_processada = pth_processing(caminho_imagem)
    try:    
        with torch.no_grad(): # Desabilita o cálculo de gradientes para inferência
            predicoes_pth_logits = pth_model(imagem_processada)
            predicoes_pth_probs = torch.nn.functional.softmax(predicoes_pth_logits, dim=1).detach().numpy()
        
        # A saída 'predicoes_pth_probs' será um array de probabilidades
        emocao_indice = np.argmax(predicoes_pth_probs[0])
        nome_emocao_predita = dict_name_labels[emocao_indice]
        confianca =  predicoes_pth_probs[0][emocao_indice]
        return (nome_emocao_predita, confianca)
    except:
        return f'Erro ao analisar imagem --flag Torch'
    

modelo_yolo = caminho_raiz / "models" / "yolov5su.pt"
modelo_yolo = YOLO(modelo_yolo)
def detecta_pessoa(imagem_path, limiar_conf=0.3, modelo_yolo=modelo_yolo):
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

def carregar_nosso_modelo():
    custom_objects = {
        'mae': MeanAbsoluteError()
    }
    caminho_raiz = Path(__file__).absolute().parent
    nosso_modelo = caminho_raiz / "models" / "modelo.h5"
    modelo = tf.keras.models.load_model(nosso_modelo, custom_objects=custom_objects)
    return modelo

def gerar_resultado(path_arquivo, nosso_modelo) -> str:
    """
    Processa uma imagem para prever idade, gênero e emoção,
    retornando os resultados em um dicionário estruturado.
    """
    resultados = {
        "idade": "N/A",
        "genero": "N/A",
        "emocao": "N/A",
        "confianca_emocao": "N/A",
        "erro": None  # Para armazenar mensagens de erro, se houver
    }
    try:
        imagem = Image.open(path_arquivo).convert('RGB')
        # Idealmente, tratar_imagem também teria tratamento de erro ou ser robusta
        imagem_tratada = tratar_imagem(imagem)

        # Predição de idade e gênero
        predicao_idade_genero = nosso_modelo.predict(imagem_tratada)

        # Validação básica da predição (ajuste conforme a saída do seu modelo)
        if predicao_idade_genero and len(predicao_idade_genero) >= 2:
            idade_bruta = float(predicao_idade_genero[0][0])
            genero_prob = float(predicao_idade_genero[1][0])

            resultados["idade"] = f"{idade_bruta:.0f}" 
            resultados["genero"] = "Mulher" if genero_prob > 0.5 else "Homem"
        else:
            resultados["erro"] = "Formato de predição de idade/gênero inesperado."
            # Você pode optar por retornar aqui ou continuar para a predição de emoção

        # Predição de emoção
        # Se 'rotular_imagens' puder usar a 'imagem' ou 'imagem_tratada' já carregada, seria mais eficiente
        # do que reler o 'path_arquivo'. Ex: rotulo_info = rotular_imagens(imagem)
        rotulo_info = rotular_imagens(path_arquivo)

        if rotulo_info and isinstance(rotulo_info, (list, tuple)) and len(rotulo_info) == 2:
            emocao, confianca = rotulo_info
            resultados["emocao"] = str(emocao)
            resultados["confianca_emocao"] = f"{float(confianca):.2f}" # Formata para 2 casas decimais
        elif rotulo_info: # Se retornou algo, mas não no formato esperado
            resultados["emocao"] = "Dados de emoção incompletos"
            if resultados["erro"]: # Concatena erros se já houver um
                resultados["erro"] += " | Dados de emoção incompletos."
            else:
                resultados["erro"] = "Dados de emoção incompletos."
        # Se rotulo_info for None, os valores "N/A" padrão permanecem

    except FileNotFoundError:
        resultados["erro"] = f"Arquivo não encontrado: {path_arquivo}"
    except Exception as e:        
        resultados["erro"] = logging.exception(f"Erro ao processar imagem {path_arquivo}. Erro: {e}:")

    return resultados