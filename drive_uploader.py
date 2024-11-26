import os
import json
import sys
import zipfile
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_executable_path():
    # Obtener la ruta del ejecutable, considerando si se está ejecutando desde un .exe o como un script.
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def read_config():
    config_path = os.path.join(get_executable_path(), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: El archivo config.json no tiene un formato JSON válido.")
            return {}
    else:
        return {}

# Configuración del alcance (scope) para Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

# Función para autenticar con Google Drive
def authenticate_drive():
    print("Iniciando autenticación con Google Drive...")
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        print("Credenciales cargadas desde token.pickle")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Credenciales refrescadas.")
        else:
            print("No se encontraron credenciales válidas, iniciando flujo de autenticación...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("Credenciales obtenidas a través de la autenticación de Google.")
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print("Credenciales guardadas en token.pickle.")
    
    print("Autenticación completada.")
    return creds

def check_access_to_folder(service, folder_id):
    try:
        # Obtener información sobre la carpeta
        file = service.files().get(fileId=folder_id, fields='id, name, mimeType, permissions').execute()
        
        # Verificar si es una carpeta
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"Acceso confirmado a la carpeta: {file['name']} (ID: {file['id']})")
            return True
        else:
            print("El ID especificado no corresponde a una carpeta.")
            return False
    except Exception as e:
        print(f"Error al acceder a la carpeta: {e}")
        return False


# Función para comprimir la carpeta del servidor en un archivo ZIP
def zip_server_folder(server_folder_path, output_zip_path):
    print(f"Comprimiendo las carpetas específicas del servidor desde: {server_folder_path}...")
    folders_to_zip = ['world', 'world_the_end', 'world_nether', 'heaven', 'plugins']
    
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for folder in folders_to_zip:
            folder_path = os.path.join(server_folder_path, folder)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, server_folder_path))
                        if debug == "debug":
                            print(f"[DEBUG] Archivo agregado al ZIP: {file_path}")
            else:
                print(f"La carpeta {folder} no existe o no es un directorio.")
    print(f"Carpeta comprimida en: {output_zip_path}")

def delete_files_in_drive_folder(service, folder_id):
    try:
        # Buscar todos los archivos en la carpeta especificada
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if not files:
            print("No hay archivos para eliminar en la carpeta.")
        else:
            # Eliminar cada archivo encontrado
            for file in files:
                try:
                    service.files().delete(fileId=file['id']).execute()
                    print(f"Archivo eliminado: {file['name']} (ID: {file['id']})")
                except Exception as e:
                    print(f"Error al eliminar el archivo {file['name']}: {e}")
    except Exception as e:
        print(f"Error al listar los archivos en la carpeta: {e}")

# Función para subir el archivo ZIP a Google Drive
def upload_to_drive(file_name, folder_id, new_file_name):
    if debug == "debug":
        print(f"[DEBUG] Iniciando subida de {file_name} a Google Drive...")
    creds = authenticate_drive()
    service = build('drive', 'v3', credentials=creds)
    
    # Comprobar acceso a la carpeta
    if not check_access_to_folder(service, folder_id):
        print("No se puede subir el archivo, no tienes acceso a la carpeta.")
        return
    
    # Eliminar archivos existentes en la carpeta antes de subir el nuevo archivo
    print("Eliminando archivos existentes en la carpeta de Google Drive...")
    delete_files_in_drive_folder(service, folder_id)
    
    # Configurar los metadatos del archivo
    file_metadata = {
        'name': new_file_name,  # Nombre que tendrá el archivo en Google Drive
        'parents': [folder_id]  # Carpeta donde se subirá el archivo
    }
    
    media = MediaFileUpload(file_name, mimetype='application/zip', resumable=True)
    
    print(f"Subiendo el archivo a la carpeta de Google Drive con ID: {folder_id}")
    
    # Iniciar la subida con seguimiento de progreso
    request = service.files().create(body=file_metadata, media_body=media)

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Progreso de subida: {int(status.progress() * 100)}%")
        except Exception as e:
            print(f"Error al subir el archivo: {e}")
            break

    if response:
        print(f"Archivo subido a Google Drive con ID: {response.get('id')}")
    else:
        print(f"Error: No se completó la subida del archivo.")


# Lógica principal
if __name__ == "__main__":
    print(r"""
 _______                           __             _____        __              
|     __|.-----.-----.-----.-----.|__|.-----.    |     \.----.|__|.--.--.-----.
|    |  ||  -__|     |  -__|__ --||  ||__ --|    |  --  |   _||  ||  |  |  -__|
|_______||_____|__|__|_____|_____||__||_____|    |_____/|__|  |__| \___/|_____|
                                                                               
 _______         __                 __                                         
|   |   |.-----.|  |.-----.---.-.--|  |.-----.----.                            
|   |   ||  _  ||  ||  _  |  _  |  _  ||  -__|   _|                            
|_______||   __||__||_____|___._|_____||_____|__|                              
         |__|                                                                  
""")
    
    print()

    config = read_config()
    # Configura la ruta de la carpeta del servidor y el archivo ZIP
    server_folder_path = config['download_path']  # Ruta de la carpeta del servidor
    output_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server_backup.zip')  # Ruta del archivo ZIP
    
    # ID de la carpeta en Google Drive donde se subirá el archivo
    folder_id = config['drive_folder_id']  # Cambia por el ID de tu carpeta en Google Drive
    
    # Nombre del archivo ZIP que se subirá a Google Drive
    new_file_name = 'server_backup.zip'

    # Información adicional
    print("\n========= Configuración de subida ==========")
    print(f"Ruta de la carpeta del servidor: {server_folder_path}")
    print(f"Ruta del archivo ZIP de respaldo: {output_zip_path}")
    print(f"ID de la carpeta en Google Drive: {folder_id}")
    print(f"Nombre del archivo que se subirá a Google Drive: {new_file_name}")
    print("============================================\n")

    debug = input("Presiona enter para comenzar: ")

    print("Comenzando el proceso de compresión y subida a Google Drive...")

    # Comprimir la carpeta del servidor
    zip_server_folder(server_folder_path, output_zip_path)
    
    # Subir el archivo comprimido a Google Drive
    upload_to_drive(output_zip_path, folder_id, new_file_name)

    print("Proceso completado.")

    input("Persiona enter para cerrar: ")
