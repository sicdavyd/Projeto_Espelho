# 🪞 Projeto Espelho Interativo  
*Um espelho inteligente com reconhecimento de emoções usando TensorFlow/PyTorch e YOLO.*  
## **🧠 Como funciona**
- 📤 **Envio de Imagem:** O usuário envia uma imagem atravéns da página inicial.
- 🔍 **Detecção de Pessoa:** A imagem é processada para verificar a presença de uma pessoa.
- 😊 **Classificação de Emoção:** se uma pessoa for detectada, a imagem é analisada para identificar a emoção.
- 📊 **Exibição de Resultado:** O resultado da análise é exibido na página de resultados.

---
## 🚀 Como Executar o Projeto  

### 📋 Pré-requisitos  
- Python 3.8+  
- Git (opcional)  

---

## ⚙️ Configuração Inicial  

### 1. Criar o Ambiente Virtual  
```bash
python -m venv venv
```
### 2. Ativar o Ambiente Virtual
- **Windows**
```bash
.\venv\Scripts\activate
```
- **Linux/MacOS**
```bash
source venv/bin/activate
```
### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```
### 4. Executar a Aplicação
```bash
python app.py
```
## 🌐 Acessando a Aplicação  
Abra no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📁 Estrutura do Projeto
```text
Projeto_Espelho/
│
├── app.py                # Arquivo principal da aplicação Flask
├── requirements.txt      # Dependências do projeto
├── utils.py              # Funções auxiliares para detecção e classificação
├── models/               # Pasta contendo todos os modelos de ML
│   ├── modelo.h5         # Modelo customizado para gênero e idade
│   ├── torchscript_model_0_66_49_wo_gl  # Modelo TorchScript de emoções
│   └── yolov5/           # Framework YOLOv5 para detecção facial
├── templates/
│   ├── index.html        # Página inicial para envio de imagens
│   └── resultado.html    # Página para exibição dos resultados
└── static/
    └── uploads/          # Pasta para armazenamento de imagens
```


## Grupo
Amanda Soares Souza - 202302597
Deivison Oliveira da Silva - 202302602
Leonardo Côrtes Filho - 202302616
Mateus de Almeida Souza - 202302622
Thiago Nascente Borges - 202302630
Vinicius Silva Benevides - 202302633