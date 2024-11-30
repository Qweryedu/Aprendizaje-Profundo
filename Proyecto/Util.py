'''
Archivo para las funciones de utilería
'''
# Bibliotecas necesarias
import os
import time
# import yt_dlp
import re
import shutil
from audioset_download import Downloader



# Función para la descarga de datos
def audioSet_download(lable_to_code, dataset='unbalanced_train'):
  # Checamos si el archivo ya existe
  if os.path.isdir('./Data/'):
    print('Se encontró el directorio de archivos')
    return
  # Checamos que haya una carpeta de Data
  os.makedirs('./Data/', exist_ok=True)
  # Iniciamos el downloader
  d = Downloader('./Data/AudioSet/', labels=[key for key in lable_to_code.keys()], n_jobs=4, download_type=dataset, copy_and_replicate=False)
  # tomamos el tiempo de la descarga
  t = time.time()
  # Iniciamos  la descarga
  d.download()
  print('Descarga completada!!!')
  print(f'Tiempo transcurrido {time.time() - t}')

def file_mover():
  archivos_disponibles = [] # Archivos que sí se pudieron descargar
  # Para obtener el ID 
  pattern = r"^[^_]+"
  check_dir = './Data/AudioSet/'
  moved = False

  if os.path.isdir(check_dir):
    ''' Movemos todos los archivos a una carpeta general'''
    target_dir   = './Data/Audios/'
    os.makedirs(target_dir, exist_ok=True)
  else:
    '''Los archivos ya se movieron'''
    check_dir = './Data/Audios/'
    moved = True

  # Recorremos los archivos 
  for root, _, files in os.walk(check_dir):
    for file in files:
      # Path al archivo
      source_file_path = os.path.join(root, file)  
      # Extraemos el ID
      match = re.match(pattern, file)
      if match:
        # Guardamos el nombre
        archivos_disponibles.append(match[0])
        if not moved:
          try:
            # Move the file to the target directory
            shutil.move(source_file_path, target_dir)
            # print(f"Moved: {source_file_path} -> {target_file_path}")
          except Exception as e:
            print(f"No se movió {source_file_path}: {e}")
  if not moved:
    # Eliminamos el directorio de AudioSet
    shutil.rmtree('./Data/AudioSet/')
    print(f'Todos los audios han sido movidos')
  return archivos_disponibles

def actual_df(df, archivos_disponibles):
  '''Checa por los archivos que se descargaron correctamente'''
  filtered_df = df[df['# YTID'].isin(archivos_disponibles)]
  return filtered_df