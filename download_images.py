from bs4 import BeautifulSoup
import requests
import os

# Leia o conteúdo do arquivo HTML
with open('assinatura_original.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse o HTML
soup = BeautifulSoup(html_content, 'html.parser')
images = soup.find_all(['img', 'source'])

image_data = []

# Extraia as informações das imagens
for img in images:
    if img.name == 'img':
        src = img.get('src')
        if src:
            image_data.append(src)
    elif img.name == 'source':
        srcset = img.get('srcset')
        if srcset:
            for src in srcset.split(','):
                url = src.strip().split(' ')[0]
                image_data.append(url)

# Função para baixar as imagens
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)

# Crie um diretório para salvar as imagens baixadas
output_directory = "downloaded_images"
os.makedirs(output_directory, exist_ok=True)

# Baixe e salve as imagens
for url in image_data:
    filename = url.replace('/', '-').replace(':', '')  # Substitui barras por hífens e remove os dois pontos
    path = os.path.join(output_directory, filename)
    download_image(url, path)
    print(f"Downloaded {filename}")
