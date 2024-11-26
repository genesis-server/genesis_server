import os
import socket
import subprocess
import platform
import json
import io
import pickle
import zipfile
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import shutil
import sys

def is_server_online(host, port=25565):
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def start_server(ram_max_mb, ram_min_mb, download_path):
    server_jar = os.path.join(download_path, 'server.jar')
    subprocess.run(['java', f'-Xmx{ram_max_mb}M', f'-Xms{ram_min_mb}M', '-jar', server_jar, 'nogui'], cwd=download_path)

def get_executable_path():
    # Obtener la ruta del ejecutable, considerando si se está ejecutando desde un .exe o como un script.
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def save_config(config):
    config_path = os.path.join(get_executable_path(), 'config.json')
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)

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


def print_config(config):
    print("\n===== Configuración local del Servidor =====")
    print(f"ID del archivo de Google Drive: {config['drive_file_id']}")
    print(f"Ruta de descarga: {config['download_path']}")
    print(f"RAM máxima: {config['ram_max_gb']} GB")
    print(f"RAM mínima: {config['ram_min_gb']} GB")
    print(f"Distancia de renderizado: {config['render_distance']} chunks")
    print(f"Distancia de visualización: {config['view_distance']} chunks")
    print(f"Host: {config['host']}")
    print(f"Puerto: {config['port']}")
    print("============================================\n")


def authenticate_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/drive.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_latest_file_in_folder(folder_id):
    creds = authenticate_drive()
    service = build('drive', 'v3', credentials=creds)
    
    query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, orderBy="createdTime desc", pageSize=1, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if items:
        return items[0]  # Devuelve el primer (y más reciente) archivo
    else:
        print("No se encontraron archivos en la carpeta.")
        return None
    
def download_from_drive(file_id, destination_path):
    creds = authenticate_drive()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Descargando... {int(status.progress() * 100)}%')
    print(f'Archivo descargado en: {destination_path}')
    
def download_latest_file(folder_id, destination_path):
    latest_file = get_latest_file_in_folder(folder_id)
    if latest_file:
        print(f"Archivo encontrado: {latest_file['name']} (ID: {latest_file['id']})")
        download_from_drive(latest_file['id'], destination_path)
    else:
        print("No se pudo descargar el archivo más reciente.")
        return False  # Retorna False si no se encontró ningún archivo
    return True  # Retorna True si el archivo se descargó correctamentes

def unzip_file(zip_path, extract_to, folders_to_replace):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Solo extraer las carpetas que están en folders_to_replace
            if any(member.startswith(folder) for folder in folders_to_replace):
                zip_ref.extract(member, extract_to)
                print(f'Extrayendo {member}')
    print(f'Archivos seleccionados descomprimidos en: {extract_to}')

def delete_existing_folders(directory, folders_to_replace):
    for folder in folders_to_replace:
        folder_path = os.path.join(directory, folder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f'Carpeta eliminada: {folder_path}')
            except Exception as e:
                print(f'Error eliminando {folder_path}: {e}')

def update_server_properties(download_path, render_distance, view_distance):
    properties_file = os.path.join(download_path, 'server.properties')

    # Leer y modificar el archivo server.properties
    if os.path.exists(properties_file):
        with open(properties_file, 'r') as file:
            lines = file.readlines()
        
        with open(properties_file, 'w') as file:
            for line in lines:
                if line.startswith('view-distance='):
                    file.write(f'view-distance={view_distance}\n')
                elif line.startswith('render-distance='):
                    file.write(f'render-distance={render_distance}\n')
                else:
                    file.write(line)

    else:
        print(f"No se encontró el archivo server.properties en {download_path}")

# Función para iniciar el servidor en modo oculto
def start_server_hidden(ram_max_mb, ram_min_mb, download_path):
    server_jar = os.path.join(download_path, 'server.jar')
    # Determinar el sistema operativo
    if platform.system() == "Windows":
        # Para Windows, ocultar la ventana de la consola
        creation_flags = subprocess.CREATE_NO_WINDOW
        subprocess.Popen(
            ['java', f'-Xmx{ram_max_mb}M', f'-Xms{ram_min_mb}M', '-jar', server_jar, 'nogui'],
            cwd=download_path,
            creationflags=creation_flags
        )
    else:
        # Para Linux y macOS, redirigir la salida a devnull
        with open(os.devnull, 'w') as devnull:
            subprocess.Popen(
                ['java', f'-Xmx{ram_max_mb}M', f'-Xms{ram_min_mb}M', '-jar', server_jar, 'nogui'],
                cwd=download_path,
                stdout=devnull,
                stderr=devnull
            )

if __name__ == "__main__":

    print("""
 ________         __                                 _______        
|  |  |  |.-----.|  |.----.-----.--------.-----.    |_     _|.-----.
|  |  |  ||  -__||  ||  __|  _  |        |  -__|      |   |  |  _  |
|________||_____||__||____|_____|__|__|__|_____|      |___|  |_____|
                                                                    
 _______                           __                               
|     __|.-----.-----.-----.-----.|__|.-----.                       
|    |  ||  -__|     |  -__|__ --||  ||__ --|                       
|_______||_____|__|__|_____|_____||__||_____|                       
""")
    print()
    print()
    config = read_config()
    
    if not config:
        drive_file_id = input("Ingresa el ID del archivo de Google Drive del servidor: ")
        drive_folder_id = input("Ingresa el ID de la carpeta de Google Drive del servidor: ")
        download_path = input("Ingresa la ruta donde quieres descargar el servidor: ")
        ram_max_gb = input("Cuánta RAM máxima (en GB) deseas asignar al servidor: ")
        ram_min_gb = input("Cuánta RAM mínima (en GB) deseas asignar al servidor: ")
        render_distance = input("Configura la distancia de renderizado (en chunks): ")
        view_distance = input("Configura la distancia de visualización (en chunks): ")

        config = {
            "drive_file_id": drive_file_id,
            "drive_folder_id": drive_folder_id,
            "download_path": download_path,
            "ram_max_gb": ram_max_gb,
            "ram_min_gb": ram_min_gb,
            "render_distance": render_distance,
            "view_distance": view_distance,
            "host": "genesis.serveminecraft.net",
            "port": 25565
        }
        save_config(config)

    else:
        print_config(config)

    ram_max_mb = int(config['ram_max_gb']) * 1024  # Convertir a MB
    ram_min_mb = int(config['ram_min_gb']) * 1024  # Convertir a MB
    
    # Actualizar el archivo server.properties
    update_server_properties(config['download_path'], config['render_distance'], config['view_distance'])
    # Definir las carpetas que deseas sincronizar
    folders_to_replace = ['world', 'world_nether', 'world_the_end', 'plugins']

    if is_server_online(config['host'], config['port']):  
        print(f"El servidor está encendido. Dirección IP: {config['host']}:{config['port']}")
    else:
        print("El servidor está apagado.")
        print("¿Desea descargar las carpetas 'world', 'world_nether', 'world_the_end' y 'plugins' del archivo de Google Drive?")
        print(f"Esas carpetas en <{config['download_path']}> serán reemplazadas.")
        confirm = input("(y / n): ").strip().lower()

        if confirm == "y":
            server_zip_path = os.path.join(config['download_path'], 'server_sync.zip')  # Nombre del archivo ZIP a descargar
            print("Descargando el archivo más reciente desde Google Drive...")
            
            if download_latest_file(config['drive_folder_id'], server_zip_path):
                try:
                    unzip_file(server_zip_path, config['download_path'], folders_to_replace)
                    # Solo eliminar el archivo ZIP si la descompresión fue exitosa
                    if os.path.exists(server_zip_path):
                        os.remove(server_zip_path)
                        print(f'Archivo ZIP eliminado: {server_zip_path}')
                except zipfile.BadZipFile:
                    print("Error: El archivo descargado no es un archivo ZIP válido.")
                except FileNotFoundError:
                    print("Error: El archivo ZIP no se encontró después de la descarga.")
            else:
                print("No se realizó ninguna descarga o la descarga falló.")

                
        elif confirm == "n":
            print("No se realizará ninguna descarga.")
        else:
            print("Por favor, conteste con 'y' o 'n'.")
        
        input_password = input("Por favor, introduce la contraseña para iniciar el servidor en modo debug: ").strip()
        password = "PASSWORD"

        if input_password == password:
            print("Contraseña correcta. Iniciando el servidor...")
            print(f"Iniciando el servidor con {config['ram_max_gb']} GB máxima y {config['ram_min_gb']} GB mínima de RAM...")
            start_server(ram_max_mb, ram_min_mb, config['download_path'])
        else:
            print("Contraseña incorrecta. Iniciando el servidor en modo oculto...")
            start_server_hidden(ram_max_mb, ram_min_mb, config['download_path'])

        input("Persiona enter para cerrar: ")
