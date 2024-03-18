import os
from google.cloud import vision
from google.cloud.vision import types
import io

# Crea una instancia del cliente de Google Cloud Vision
client = vision.ImageAnnotatorClient()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_image(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    
    # Usa el cliente de Google Cloud Vision para realizar OCR en la imagen
    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    # Extrae el texto detectado de la respuesta
    if texts:
        return texts[0].description
    else:
        return ""

def search_keywords(text, user_keywords):
    found_keywords = [keyword for keyword in user_keywords if keyword.lower() in text.lower()]
    return found_keywords

def visualize_document_content(archivo, texto_documento):
    print(f"\nContenido de {archivo}:")
    print(texto_documento)

def open_file(file_path):
    try:
        os.startfile(file_path)
    except OSError as e:
        print(f"No se pudo abrir el archivo. Error: {e}")

def main():
    # Solicitar al usuario ingresar palabras clave separadas por comas
    user_keywords_input = input("Ingresa las palabras clave separadas por comas: ")
    user_keywords = [keyword.strip() for keyword in user_keywords_input.split(',')]

    # Definir la carpeta de trabajo local
    carpeta_local = r'C:\Users\PAULINA G\Desktop\SEMESTRE23\TEXTOS\DOCUMENTOS'
    os.chdir(carpeta_local)

    archivos = [
        r'archivo1.png',
        r'archivo2.pdf',
        r'archivo3.pdf',
        r'archivo4.jpg'
    ]

    # Realizar el análisis para cada archivo
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_local, archivo)
        
        if archivo.lower().endswith((".png", ".jpg", ".jpeg")):
            texto_documento = extract_text_from_image(ruta_completa)
        elif archivo.lower().endswith(".pdf"):
            texto_documento = extract_text_from_pdf(ruta_completa)
        else:
            texto_documento = ""

        palabras_clave_encontradas = search_keywords(texto_documento, user_keywords)

        if palabras_clave_encontradas:
            print(f"\nPalabras clave encontradas en {archivo}:")
            print(palabras_clave_encontradas)

            # Visualizar el contenido del documento en la consola
            visualize_document_content(archivo, texto_documento)

            # Abrir el archivo con la aplicación predeterminada
            open_file(ruta_completa)

if __name__ == "__main__":
    main()
