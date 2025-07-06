import base64
import io
import uuid
from PIL import Image

def convertir_imagen_a_webp(imagen_base64):
    try:
        image = Image.open(io.BytesIO(imagen_base64))
        rgb_image = image.convert('RGB')
        image_name = f'{uuid.uuid4().hex}.webp'
        ruta_webp = f'app/static/fotos/{image_name}.webp'
        rgb_image.save(ruta_webp, format='WebP')
        
    except Exception as e:
        raise Exception(f"Error al convertir la imagen a webp: {str(e)}")
    return image_name
