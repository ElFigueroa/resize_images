# 📸 Image Resizer 720x480 (Python)

Pequeño script en Python que procesa imágenes en formato .png y .jpg, realiza un resize uniforme a 720×480 px, renombra las imágenes usando las primeras 5 letras del nombre original, convierte todo a .jpg, y evita duplicados conservando solo la primera imagen encontrada.

## 🚀 Características principales

- 🖼️ Acepta imágenes .png y .jpg
- 🔄 Resize automático a 720 x 480 px
- 📝 Renombrado automático
  - Usa las primeras 5 letras del nombre original
  - Ejemplo: `fotografia_campo.png` → `fotor.jpg`
- 📤 Salida en formato .jpg
- 🛑 Control de duplicados
  - Si un nombre resultante ya existe, solo se mantiene la primera imagen
- 📂 Procesa todo el contenido de la carpeta `input_images/`
- 💾 Guarda las imágenes procesadas en `output_images/`
- ⚠️ Manejo de errores para archivos corruptos o tipos no válidos

## 📁 Estructura del proyecto

``` bash
resize_images/
│
├── src/
│ ├── init.py
│ ├── main.py # Punto de entrada del script
│ ├── processor.py # Lógica de resize, renombrado y guardado
│ └── utils.py # Funciones auxiliares
│
├── input_images/ # Carpeta con las imágenes originales
├── output_images/ # Carpeta donde se guardarán las imágenes procesadas
│
├── requirements.txt # Librerías necesarias
├── README.md # Documentación del proyecto
└── .gitignore # Archivos y carpetas ignoradas por Git
```

## 🛠️ Requisitos

- Python 3.9+
- Librerías (instalación abajo):
  - Pillow
