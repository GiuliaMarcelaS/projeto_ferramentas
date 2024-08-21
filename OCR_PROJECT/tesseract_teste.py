import pytesseract
from PIL import Image 

# Caminho em que está o executável do Tesseract 
caminho_tesseract = r"C:/Users/01917955260/AppData/Local/Programs/Tesseract-OCR"

pytesseract.pytesseract.tesseract_cmd = caminho_tesseract + r"/tesseract.exe"

# Leitura da Imagem 
imagem_path = "C:/Users/01917955260/Documents/OCR PROJECT/image.png"
imagem = Image.open(imagem_path)

# Conversão da imagem em pdf
pdf = pytesseract.image_to_pdf_or_hocr(imagem, extension='pdf')

# Salvando o pdf gerado
with open ('gerado.pdf', 'wb') as f : 
    f.write(pdf)