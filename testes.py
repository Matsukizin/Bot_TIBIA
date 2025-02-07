import cv2
import pytesseract
import numpy as np
import re
# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Carrega a imagem
imagem = cv2.imread("prints/medicines2.png")

# Aumenta o tamanho da imagem para melhorar o OCR
largura = imagem.shape[1] * 2  # Dobra a largura
altura = imagem.shape[0] * 2  # Dobra a altura
imagem = cv2.resize(imagem, (largura, altura), interpolation=cv2.INTER_CUBIC)

# Converte para escala de cinza
imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplica um filtro para remover ruídos
imagem = cv2.GaussianBlur(imagem, (3, 3), 0)

# Ajusta o contraste (opcional, pode testar sem)
imagem = cv2.convertScaleAbs(imagem, alpha=1.5, beta=0)  # Alpha > 1 aumenta o contraste

# Testa diferentes métodos de limiarização para ver qual funciona melhor
_, imagem_bin = cv2.threshold(imagem, 150, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

# Salva a imagem processada para análise
cv2.imwrite("processed.png", imagem_bin)

# Exibe a imagem processada (opcional)
cv2.imshow("Imagem Processada", imagem_bin)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Usa o Tesseract para extrair o texto
texto = pytesseract.image_to_string(imagem_bin, config='--psm 6', lang="eng")

# Extrai o primeiro número encontrado no texto
numeros = re.findall(r'\d+', texto)

# Converte para inteiro e salva na variável 'medicines'
medicines = int(numeros[0]) if numeros else None

# Exibe o resultado
print("Medicines:", medicines)

