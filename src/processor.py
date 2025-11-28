"""Lógica de procesamiento de imágenes: resize, renombrado y guardado."""

import os
from PIL import Image
from utils import get_first_five_letters, ensure_directory


class ImageProcessor:
    """Procesa imágenes: resize, renombrado y guardado."""
    
    TARGET_WIDTH = 720
    TARGET_HEIGHT = 480
    OUTPUT_FORMAT = 'JPEG'
    OUTPUT_EXTENSION = '.jpg'
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        Inicializa el procesador de imágenes.
        
        Args:
            input_dir: Directorio de entrada con imágenes originales
            output_dir: Directorio de salida para imágenes procesadas
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.processed_names = set()
        
        ensure_directory(self.output_dir)
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """
        Redimensiona una imagen de forma adaptativa a 720x480 px.
        
        Mantiene la relación de aspecto original, escala la imagen al máximo
        posible dentro de 720x480 y la centra en un canvas del tamaño objetivo.
        
        Args:
            image: Objeto PIL Image
            
        Returns:
            Imagen redimensionada y centrada
        """
        # Obtener dimensiones originales
        orig_width, orig_height = image.size
        
        # Calcular ratios de escala para ancho y alto
        scale_w = self.TARGET_WIDTH / orig_width
        scale_h = self.TARGET_HEIGHT / orig_height
        
        # Usar la escala menor para mantener la imagen completa
        scale = min(scale_w, scale_h)
        
        # Calcular nuevas dimensiones escaladas
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        # Redimensionar la imagen manteniendo la relación de aspecto
        scaled_image = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )
        
        # Crear un canvas de fondo blanco con las dimensiones objetivo
        canvas: Image.Image = Image.new('RGB', (self.TARGET_WIDTH, self.TARGET_HEIGHT))
        # Rellenar con blanco
        canvas.paste((255, 255, 255), (0, 0, self.TARGET_WIDTH, self.TARGET_HEIGHT))
        
        # Calcular posición para centrar la imagen
        x_offset = (self.TARGET_WIDTH - new_width) // 2
        y_offset = (self.TARGET_HEIGHT - new_height) // 2
        
        # Pegar la imagen escalada en el centro del canvas
        canvas.paste(scaled_image, (x_offset, y_offset))
        
        return canvas
    
    def _get_output_filename(self, original_filename: str) -> str:
        """
        Genera el nombre de salida usando las primeras 5 letras.
        
        Args:
            original_filename: Nombre del archivo original
            
        Returns:
            Nombre del archivo de salida
        """
        first_five = get_first_five_letters(original_filename)
        return first_five + self.OUTPUT_EXTENSION
    
    def process_image(self, input_path: str) -> bool:
        """
        Procesa una imagen individual: resize, renombrado y guardado.
        
        Args:
            input_path: Ruta completa del archivo de imagen
            
        Returns:
            True si se procesó exitosamente, False en caso contrario
        """
        try:
            filename = os.path.basename(input_path)
            output_filename = self._get_output_filename(filename)
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Control de duplicados: si el nombre ya existe, lo omitimos
            if output_filename in self.processed_names:
                print(f"⚠️  Omitido (duplicado): {filename} → {output_filename} (ya existe)")
                return False
            
            # Abrir imagen
            image = Image.open(input_path)
            
            # Convertir a RGB si es necesario (para PNG con transparencia, etc.)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Redimensionar
            resized_image = self._resize_image(image)
            
            # Guardar como JPG
            resized_image.save(output_path, self.OUTPUT_FORMAT, quality=90)
            
            # Registrar el nombre procesado
            self.processed_names.add(output_filename)
            
            print(f"✅ Procesada: {filename} → {output_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error al procesar {filename}: {str(e)}")
            return False
    
    def process_all(self, image_files: list) -> dict:
        """
        Procesa todas las imágenes de una lista.
        
        Args:
            image_files: Lista de rutas de archivos de imagen
            
        Returns:
            Diccionario con estadísticas de procesamiento
        """
        stats = {
            'total': len(image_files),
            'successful': 0,
            'skipped': 0,
            'failed': 0
        }
        
        for image_path in image_files:
            success = self.process_image(image_path)
            if success:
                stats['successful'] += 1
            else:
                # Podría ser duplicado o error
                if os.path.basename(image_path) in self.processed_names:
                    stats['skipped'] += 1
                else:
                    stats['failed'] += 1
        
        return stats
