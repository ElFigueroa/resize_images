"""Funciones auxiliares para el procesamiento de imágenes."""

import os
import shutil
import re
from pathlib import Path


def get_first_five_letters(filename: str) -> str:
    """
    Extrae caracteres del nombre del archivo sin extensión.
    
    Elimina espacios en blanco y caracteres especiales, convierte a mayúsculas
    y toma los primeros 7 caracteres alfanuméricos.
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        Primeros 7 caracteres alfanuméricos sin espacios en mayúsculas
    """
    name_without_ext = os.path.splitext(filename)[0]
    # Eliminar caracteres especiales, dejar solo letras, números y espacios
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s]', '', name_without_ext)
    # Eliminar espacios y convertir a mayúsculas
    cleaned_name = cleaned_name.replace(' ', '').upper()
    # Tomar solo los primeros 7 caracteres
    return cleaned_name[:8]


def ensure_directory(directory: str) -> None:
    """
    Crea un directorio si no existe.
    
    Args:
        directory: Ruta del directorio a crear
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_image_files(input_dir: str) -> list:
    """
    Obtiene todos los archivos de imagen .png, .jpg, .jpeg y .jfif de un directorio.
    
    Args:
        input_dir: Ruta del directorio de entrada
        
    Returns:
        Lista de rutas completas a los archivos de imagen
    """
    image_files = []
    valid_extensions = {'.png', '.jpg', '.jpeg', '.jfif'}
    
    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in valid_extensions:
                image_files.append(os.path.join(input_dir, filename))
    image_files.sort()
    return image_files


def clean_directory(directory: str) -> None:
    """
    Elimina todo el contenido de un directorio.
    
    Args:
        directory: Ruta del directorio a limpiar
    """
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {file_path}: {str(e)}")
