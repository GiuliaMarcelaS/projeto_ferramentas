from flask import Flask, render_template, request, send_file
import pytesseract
from PIL import Image
import os
from io import BytesIO
from pdf2image import convert_from_bytes
from PyPDF2 import PdfMerger 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Caminho em que está o executável do Tesseract (deve ser mudado de acordo com o pc usado, para realizar testes)
caminho_tesseract = r"C:/Users/01917955260/AppData/Local/Programs/Tesseract-OCR"

pytesseract.pytesseract.tesseract_cmd = caminho_tesseract + r"/tesseract.exe"

# Caminho do Poppler no Windows
caminho_poppler = r"c:/Users/01917955260/Documents/poppler-24.07.0/Library/bin"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar se o arquivo foi enviado
        if 'arquivo' not in request.files:
            return "Nenhum arquivo foi enviada"

        file = request.files['arquivo']

        if file.filename == '':
            return "Nenhuma arquivo selecionada"
        
        if not file.filename.endswith('.pdf'):
            return "Arquivo enviado não é pdf. Por favor, envie um arquivo pdf"
        
        # Carrega as páginas do pdf para imagem
        imagens = convert_from_bytes(file.read(), poppler_path = caminho_poppler)


        pdfs = []
        for imagem in imagens:
            # Converte cada imagem em PDF usando Tesseract
            pdf = pytesseract.image_to_pdf_or_hocr(imagem, extension='pdf')
            pdfs.append(BytesIO(pdf))

        # Mescla os PDFs usando PdfMerger do PyPDF2
        output_pdf = BytesIO()
        merger = PdfMerger()

        for pdf in pdfs:
            pdf.seek(0)
            merger.append(pdf)

        merger.write(output_pdf)
        merger.close()
        output_pdf.seek(0)

        # Retornar o PDF como resposta
        return send_file(output_pdf,  download_name='Gerado.pdf', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
