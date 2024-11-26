# Configuración de una IP Estática en Windows

Para configurar una dirección IP estática en Windows, sigue estos pasos:

## 1. Acceder al Panel de Control
- Presiona las teclas **Windows + R** al mismo tiempo, escribe `ncpa.cpl` en la ventana que aparece y haz clic en **Aceptar**.
> **Nota:** Las conexiones de red mostrarán los adaptadores de red que están actualmente conectados a tu ordenador.
<br>

![Acceder al Panel de Control](/IP-config/01.png)

## 2. Seleccionar el Adaptador de Red
- Haz clic con el botón derecho en el adaptador de red que está actualmente conectado a tu dispositivo. Generalmente será el adaptador con la palabra **Ethernet** en el nombre.
<br>

![Seleccionar el Adaptador de Red](/IP-config/02.png)

## 3. Seleccionar Propiedades
- En el menú desplegable, selecciona **Propiedades**.
<br>

![Seleccionar Propiedades](/IP-config/03.png)

## 4. Seleccionar Protocolo de Internet versión 4 (TCP/IPv4)
- En la lista de elementos, busca **Protocolo de Internet versión 4 (TCP/IPv4)** y haz doble clic sobre él.
- <br>

![Seleccionar TCP/IPv4](/IP-config/04.png)

## 5. Introducir Manualmente la Dirección IP y la Máscara de Subred
- Selecciona la opción **Usar la siguiente dirección IP**.
- Ingresa la siguiente información en los campos correspondientes:
  - **Dirección IP**: Debes ingresar una dirección IP válida dentro de la red a la que estás conectado. Los primeros tres grupos de dígitos deben coincidir con los del dispositivo al que te estás conectando. Ejemplo: `192.168.10.10`.
  - **Máscara de subred**: La máscara de subred debe coincidir con la del dispositivo al que estás conectado. Un valor común es `255.255.255.0`.
<br>
  
![Introducir IP y Máscara](/IP-config/05.png)

## 6. Guardar la Configuración
- Haz clic en **Aceptar** en la ventana **Propiedades del Protocolo de Internet versión 4 (TCP/IPv4)**.
- Haz clic en **Aceptar** nuevamente en la ventana **Propiedades de Ethernet**.
> **Nota:** Asegúrate de presionar **Aceptar** en ambas ventanas para que los ajustes se guarden correctamente.

Ahora tu dispositivo debería estar configurado con una IP estática. Puedes verificar la conexión volviendo a acceder a **ncpa.cpl** y comprobando que el adaptador tiene la nueva IP asignada.
