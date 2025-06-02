# 🪞 Projeto Espelho Interativo  
*Um espelho inteligente com reconhecimento de emoções usando TensorFlow/PyTorch e YOLO.*  

## 🧠 Como funciona
📤 Envio de Imagem: O usuário envia uma imagem atravéns da página inicial.
🔍 Detecção de Pessoa: A imagem é processada para verificar a presença de uma pessoa.
😊 Classificação de Emoção: se uma pessoa for detectada, a imagem é analisada para identificar a emoção.
📊 Exibição de Resultado: O resultado da análise é exibido na página de resultados.
---
## 🚀 Como Executar o Projeto  

### 📋 Pré-requisitos  
- Python 3.8+  
- Git (opcional)  

---

## ⚙️ Configuração Inicial  

### 1. Criar e Ativar o Ambiente Virtual  
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```
### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```
### 3. Executar a Aplicação
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
├── templates/
│   ├── index.html        # Página inicial para envio de imagens
│   └── resultado.html    # Página para exibição dos resultados
└── static/
    └── uploads/          # Pasta para armazenar imagens enviadas
```


