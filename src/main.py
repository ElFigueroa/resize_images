"""Script principal para procesar imágenes."""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from processor import ImageProcessor
from utils import get_image_files, ensure_directory, clean_directory


def main():
    """Función principal del script."""
    
    # Definir directorios
    project_root = Path(__file__).parent.parent
    input_dir = os.path.join(project_root, 'input')
    output_dir = os.path.join(project_root, 'output')
    
    print("=" * 60)
    print("🖼️  IMAGE RESIZER 720x480")
    print("=" * 60)
    print()
    
    # Asegurar que existen los directorios
    ensure_directory(input_dir)
    ensure_directory(output_dir)
    
    # Obtener archivos de imagen
    print(f"📂 Buscando imágenes en: {input_dir}")
    image_files = get_image_files(input_dir)
    
    if not image_files:
        print("⚠️  No se encontraron archivos .png o .jpg en la carpeta de entrada")
        print()
        return
    
    print(f"📸 Se encontraron {len(image_files)} imagen(es)\n")
    
    # Procesar imágenes
    processor = ImageProcessor(input_dir, output_dir)
    stats = processor.process_all(image_files)
    
    # Mostrar resumen
    print()
    print("=" * 60)
    print("📊 RESUMEN DEL PROCESAMIENTO")
    print("=" * 60)
    print(f"Total procesadas:     {stats['successful']}")
    print(f"Duplicadas omitidas:  {stats['skipped']}")
    print(f"Errores:              {stats['failed']}")
    print(f"Total:                {stats['total']}")
    print()
    print(f"✨ Las imágenes se encuentran en: {output_dir}")
    print("=" * 60)
    print()
    
    # Limpiar la carpeta de entrada
    print("🧹 Limpiando carpeta de entrada...")
    clean_directory(input_dir)
    print("✅ Carpeta de entrada vaciada")
    print()


if __name__ == '__main__':
    main()
