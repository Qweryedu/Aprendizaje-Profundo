'''
Archivo para las funciones de utilería
'''
# Bibliotecas necesarias
import os
import time
import yt_dlp
import re
import shutil
from audioset_download import Downloader



# Función para la descarga de datos
def AudioSet_download(lable_to_code):
  # Checamos que haya una carpeta de Data
  os.makedirs('./Data/', exist_ok=True)
  # Iniciamos el downloader
  d = Downloader('./Data/AudioSet/', labels=[key for key in lable_to_code.keys()], n_jobs=4, download_type='unbalanced_train', copy_and_replicate=False)
  # tomamos el tiempo de la descarga
  t = time.time()
  # Iniciamos  la descarga
  d.download()
  print(f'Tiempo transcurrido {time.time() - t}')

  ''' Movemos todos los archivos a una carpeta general'''
  target_dir   = './Data/Audios/'
  os.makedirs(target_dir, exist_ok=True)

  # Para obtener el ID 
  pattern = r"^[^_]+"
  # Recorremos los archivos 
  for root, _, files in os.walk('./Data/AudioSet/'):
    for file in files:
      # Path al archivo
      source_file_path = os.path.join(root, file)  
      # Extraemos el ID
      match = re.match(pattern, file)
      if match:

        try:
          # Move the file to the target directory
          shutil.move(source_file_path, target_dir)
          # print(f"Moved: {source_file_path} -> {target_file_path}")
        except Exception as e:
          print(f"No se movió {source_file_path}: {e}")

  # Eliminamos el directorio de AudioSet
  shutil.rmtree('./Data/AudioSet/')

  print('Descarga completada!!!')