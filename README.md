# **Servidor de Minecraft**

![Foto Inicio](/images/mushroom.jpeg)
Este proyecto permite gestionar y hostear un servidor de Minecraft de manera local y gratuita, así como respaldar los archivos de este utlizando [Google Drive](https://drive.google.com/drive/u/0/my-drive), comprimiendo carpetas específicas y subiéndolas a la nube. Además, gestiona la configuración y el inicio de un servidor de Minecraft con configuraciones personalizadas.

## **Requisitos**

- Python 3.x (Yo utilizo 3.12.5)
- Librerías de Python:
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
  - `google-api-python-client`
  - `zipfile`
- [Java 1.17](https://javadl.oracle.com/webapps/download/AutoDL?BundleId=251391_0d8f12bc927a4e2c9f8568ca567db4ee) o superior
- [No-IP](https://www.noip.com/es-MX/download)
  
  Puedes instalar estas librerías ejecutando:
  
  ```bash
  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
  ```

- Archivo de credenciales de Google Drive (`credentials.json`), obtenido desde la consola de desarrolladores de Google o descargado de Drive.
- El archivo de configuración (`config.json`), obtenido y editado desde GitHub o Google Drive.

## **Estructura del Proyecto**

El proyecto consta de dos partes principales:

1. **Drive Uploader**: Gestiona la autenticación con Google Drive, comprime las carpetas específicas del servidor de Minecraft (`world`, `world_nether`, `world_the_end`, `heaven`, `plugins`) y las sube a Google Drive.

2. **Main Init**: Controla la configuración del servidor de Minecraft, gestionando el inicio y monitoreo del servidor, y almacenando configuraciones locales.

## **Archivos Importantes**

- `config.json`: Contiene la configuración del servidor de Minecraft, como la ruta de descarga, la RAM asignada, y el ID de la carpeta de Google Drive.
  
- `credentials.json`: Necesario para autenticar la conexión con la API de Google Drive. Debe descargarse desde la consola de Google. (Está en el drive)

## **Uso**

### **Configuración inicial**

1. **Configura tu servidor de Minecraft**:
   - Modifica el archivo `config.json` para incluir la ruta de la carpeta del servidor, el ID de la carpeta de Google Drive, la RAM máxima y mínima, etc.
   - 
> **Importante:** `download_path` debe tener el formato `"C:\\abcd\\efgh\\ijkl"` (carpetas separadas por \\)

> **Nota:** `ram_max_gb` y `ram_min_gb` debe oscilar entre la [RAM de tu dispositivo](/RAM/check-ram.md) - 2Gb y la [RAM de tu dipositivo](/RAM/check-ram.md) - 6Gb

2. **Configura tu router**
> **Nota:** Hay más información sobre cómo configurar el router [aquí](/port-redirect/port-redirect.md)
   - Accede a la configuración de tu router escribiendo `192.168.1.1`
   - Añade una redirección de puertos a tu IP local (puertos `25565` y `19132`)
       - El puerto `25565` en **TCP**
       - El puerto `19132` en **UDP**
       - Utiliza `ipconfig` para conocer la puerta de enlace y la IP local de tu dispositivo
   - [Establece una IP local fija](/IP-config/static-IP.md) para tu dispositivo (recomendado)
   - Añade una regla al firewall con los puertos `25565` y `19132` (entrada y salida)

4. **Obtén las credenciales de Google**:
(Innecesario, está en drive)
   - Dirígete a la [Consola de Google Developers](https://console.developers.google.com/), crea un proyecto y habilita la API de Google Drive.
   - Descarga el archivo `credentials.json` y colócalo en el directorio del proyecto.

### **Ejecutar el servidor y respaldar los archivos**

1. **Iniciar el servidor de Minecraft**:
   - Ejecuta el script `main_init.py` o `Genesis Server.exe` para iniciar el servidor de Minecraft. Este script verifica la conexión al servidor y, si está en línea, lo inicia con las configuraciones definidas.

3. **Juega**:
   - Inicia Minecraft con tu laucher de confianza, si no tienes puedes usar [Sklauncher](SKlauncher-install.md). Disfruta del juego. Para cerrar el server, ejecuta el comando `/stop`.

> **Nota**: El resto de comandos están [aquí](genaral-info.md)
   
2. **Subir los archivos a Google Drive**:
   - Ejecuta el script `drive_uploader.py` o `Drive Uploader.exe` para comprimir las carpetas importantes del servidor de Minecraft y subirlas a la carpeta de Google Drive especificada en `config.json`.

## **Funciones Principales**

- **Comprimir carpetas específicas del servidor**: El script `drive_uploader.py` comprime las carpetas `world`, `world_nether`, `world_the_end`, `heaven` y `plugins` en un archivo `.zip`.

- **Subir archivo comprimido a Google Drive**: Una vez comprimido el archivo, se sube automáticamente a la carpeta indicada en Google Drive, y los archivos previos en esa carpeta se eliminan.

- **Monitoreo del servidor**: El script `main_init.py` permite verificar si el servidor de Minecraft está en línea en el puerto 25565, y gestiona el inicio y parada del servidor con la configuración de RAM.

## **Errores comunes**

- **Credenciales de Google no válidas**: Asegúrate de que el archivo `credentials.json` esté correctamente configurado y que tengas acceso a la API de Google Drive.
  
- **Archivos no encontrados**: Verifica que las carpetas `world`, `world_the_end`, `world_nether`, `heaven` y `plugins` existan en la ruta especificada.
  
- **Error de autentificación**: Error en el archivo `token.pickle`, bórralo y vuelve a ejecutar el programa.
  
- **Error en la versión**: Si estáis en genesis, comprobad que la versión de Minecraft es la `1.21.1`
  
- **Error de conexión**: Comprueba la dirección del servidor, puedes utilizar el comando `ping "IP"` para ver si el servidor está online. Si estás jugando en Minecraft Bedrock PE, comprueba que tenéis habilitada la opción de usar datos móviles.
        Si tienes dudas de si el servidor está funcionando comprueba que los puertos `25565` y `19132` están abiertos en [Minecraft Server Status](https://mcsrvstat.us) o [Can U See Me](https://canyouseeme.org)
