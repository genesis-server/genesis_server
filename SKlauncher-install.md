### Requisitos para el Launcher y Configuración de Java

El launcher disponible en [skmedix.pl](https://skmedix.pl/es/downloads) requiere **Java 17** o **Java 21** para funcionar correctamente. Aquí te explicamos cómo instalar y configurar Java siguiendo las recomendaciones.

#### 1. **Descargar e instalar Java 21 LTS o Java 17**
Puedes usar las siguientes opciones para descargar la versión adecuada de Java:

- **Temurin™ 21 LTS (recomendado)**: Descárgalo desde la página oficial de [Adoptium](https://adoptium.net/es/temurin/releases/?version=17&os=windows).
- **Oracle Java**: Descárgalo desde el sitio oficial de Oracle ([Java Downloads](https://www.oracle.com/java/technologies/downloads/)).

#### 2. **Configuración durante la instalación**
Durante el proceso de instalación, asegúrate de activar las siguientes opciones:

- **Add to PATH**: Esto agregará Java al sistema para que pueda ser usado desde la línea de comandos y por aplicaciones.
- **Set JAVA_HOME variable**: Configura automáticamente la variable de entorno `JAVA_HOME`, necesaria para muchos programas que dependen de Java.
- **JavaSoft (Oracle) registry keys**: Crea las claves de registro necesarias para que los programas identifiquen la instalación de Java.

#### 3. **Verificar la instalación**
Después de instalar, verifica que Java esté configurado correctamente:

1. Abre una terminal o el símbolo del sistema (**Win + R**, escribe `cmd` y presiona Enter).
2. Escribe el comando:  
   ```bash
   java -version
   ```
   Este debería mostrar la versión de Java instalada.

#### 4. **Configuración manual (si es necesario)**
Si alguna de las opciones anteriores no se configuró automáticamente:

- **Agregar Java a `PATH`**:
  1. Ve a **Configuración del sistema** > **Configuración avanzada del sistema**.
  2. En la pestaña **Opciones avanzadas**, haz clic en **Variables de entorno**.
  3. Busca la variable `Path`, edítala y agrega la ruta al directorio `bin` de tu instalación de Java. Ejemplo:  
     ```
     C:\Program Files\Eclipse Adoptium\jdk-21\bin
     ```
  
- **Configurar `JAVA_HOME`**:
  1. Crea una nueva variable de entorno llamada `JAVA_HOME`.
  2. Asigna como valor la ruta principal de la instalación de Java. Ejemplo:  
     ```
     C:\Program Files\Eclipse Adoptium\jdk-21
     ```

#### 5. **Actualizar el Launcher**
Después de configurar Java, ejecuta el launcher. Ahora debería funcionar correctamente. Si hay problemas, verifica que el launcher esté apuntando a la instalación correcta de Java.
