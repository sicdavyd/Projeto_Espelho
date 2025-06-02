from flask import Flask, request, render_template, url_for
import os
import uuid
from utils import detecta_pessoa, carregar_nosso_modelo, gerar_resultado

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
nosso_modelo = carregar_nosso_modelo()

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
                resultado = gerar_resultado(path_arquivo=path_arquivo, nosso_modelo=nosso_modelo)
            else:
                resultado = "Imagem inválida: nenhuma pessoa detectada."
                nome_arquivo = 'default.jpg'
            return render_template('resultado.html',
                                   dados_analise=resultado,
                                   imagem=url_for('static', filename='uploads/' + nome_arquivo))
        
        else:
            resultado = 'Nenhum arquivo enviado.'
            return render_template('resultado.html',
                                   dados_analise=resultado,
                                   imagem=url_for('static', filename='uploads/default.jpg'))

    return render_template('index.html', resultado=resultado)
    ...
if __name__ == "__main__":
    app.run(debug=True)