from flask import Flask, render_template, request
import openai
from werkzeug.utils import secure_filename
import docx
import os

app = Flask(__name__)
openai.api_key = 'sua_chave_api_aqui'

# Configurações para o upload de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/gerar_materia', methods=['POST'])
def gerar_materia():
    if 'transcricao' not in request.files or 'foto' not in request.files:
        return redirect(request.url)
    file = request.files['transcricao']
    foto = request.files['foto']
    if file.filename == '' or foto.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename) and foto and allowed_file(foto.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        foto_filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

        # Processa o arquivo .docx
        doc = docx.Document(filepath)
        texto_completo = []
        for paragrafo in doc.paragraphs:
            texto_completo.append(paragrafo.text)
        texto_transcricao = '\n'.join(texto_completo)

        # Aqui você inseriria o código para gerar a matéria com a API da OpenAI
        # ...

        # Remover ou comentar essas linhas caso você processe o texto e retorne a matéria
        return render_template('index.html', mensagem="Matéria gerada com sucesso!")
    return 'Arquivo não permitido', 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

