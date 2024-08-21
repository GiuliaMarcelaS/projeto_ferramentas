from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Caminho em que está o executável do Tesseract (deve ser mudado de acordo com o pc usado, para realizar testes)
caminho_tesseract = r"C:/Users/00208560246/AppData/Local/Programs/Tesseract-OCR"

pytesseract.pytesseract.tesseract_cmd = caminho_tesseract + r"/tesseract.exe"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar se o arquivo foi enviado
        if 'image' not in request.files:
            return "Nenhuma imagem foi enviada"

        file = request.files['image']

        if file.filename == '':
            return "Nenhuma imagem selecionada"

        # Carrega a imagem diretamente da memória usando o BytesIO
        imagem = Image.open(BytesIO(file.read()))

        # Converte para pdf
        pdf = pytesseract.image_to_pdf_or_hocr(imagem, extension='pdf')

        # Retornar o PDF como resposta
        return send_file(BytesIO(pdf),  download_name='Gerado.pdf', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
