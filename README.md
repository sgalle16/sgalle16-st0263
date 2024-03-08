# ST0263 Tópicos Especiales en Telemática

### Estudiante(s): Santiago Gallego Quintero, sgalle16@eafit.edu.co

### Profesor: Juan Carlos Montoya, jcmontoy@eafit.edu.co



## RETO 1 Y 2 SISTEMA P2P - Comunicación entre procesos mediante API REST, RPC y MOM 

Se plantea implementar un sistema de compartición de recursos (archivos) p2p totalmente descentralizado y no estructurado, usando protocolos de comunicación entre peers, como API REST, gRPC y MOM con RabbitMQ. 
Es una red peer to peer con una arquitectura de red distribuida. Los nodos de la red puede actuar tanto como cliente (activar consultas de búsqueda) como para el servidor (manejar las solicitudes recibidas). Este es un enfoque mucho más beneficioso que la arquitectura de servidor centralizado donde el servidor tiene todos los recursos y los nodos individuales solicitan recursos. 

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Lo que tenia pensado realizar no funciono, es decir que solo funcionan algunas conexiones entre peers, y validaciones usando gRPCs.


## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
No se cumplio con, uso de mom y api rest. tampoco con la localización de recursos ni descubrimientos.

Requisitos Funcionales

- Comunicación P2P Descentralizada: Cada nodo debe poder actuar como cliente y servidor, permitiendo la comunicación directa entre pares sin la necesidad de un servidor central.
- Descubrimiento de Pares: Implementar un mecanismo para que los nodos puedan descubrir otros nodos disponibles en la red P2P.
- Compartición de Archivos: Los nodos deben poder listar, solicitar y compartir archivos con otros nodos de la red.
- Soporte de Microservicios: El sistema debe dividirse en microservicios, incluyendo servicios para la gestión de archivos, comunicación entre nodos y descubrimiento de servicios.
- API REST para Interacción con el Cliente: Proveer una API REST para que los clientes puedan realizar operaciones como listar y solicitar archivos.
- Comunicación RPC: Utilizar llamadas a procedimiento remoto (RPC) para la comunicación entre los microservicios del sistema.
- Middleware Orientado a Mensajes (MOM): Implementar un MOM para manejar la comunicación asíncrona entre los microservicios.
  
Requisitos No Funcionales

- Escalabilidad: El sistema debe ser capaz de escalar horizontalmente para soportar un aumento en el número de nodos sin degradar el rendimiento.
- Rendimiento: El sistema debe minimizar la latencia en la comunicación entre nodos y la transferencia de archivos.
- Interoperabilidad: Capacidad para operar sobre diferentes plataformas y sistemas operativos sin requerir modificaciones.
- Mantenibilidad: El código debe ser modular, bien documentado y fácil de modificar para facilitar el mantenimiento y la incorporación de nuevas funcionalidades.
- Usabilidad: La interfaz de usuario para la interacción con el sistema debe ser intuitiva y fácil de usar.

  
# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

La arquitectura se basa en un sistema p2p totalmente descentralizado:
Los sistemas distribuidos peer-to-peer (P2P) no estructurados son una forma de red en la que todos los nodos (peers) tienen las mismas capacidades y responsabilidades. No hay una estructura de red fija o predefinida, y los nodos pueden unirse, dejar y reorganizar la red a voluntad.

En un sistema P2P no estructurado, la búsqueda de recursos (como archivos o servicios) puede ser más desafiante que en un sistema estructurado. Esto se debe a que no hay un índice central o una estructura de datos que facilite la búsqueda. En su lugar, las búsquedas suelen realizarse mediante técnicas de Flooding o Random Walks.




Diagrama para mostrar el flujo de interacción entre los componenetes de mas alto nivel.

![diagram-export-7-3-2024-11_26_24-p -m](https://github.com/sgalle16/sgalle16-st0263/assets/14111169/7d1d1172-00e6-491a-94db-e7e06314a739)


Topologia no estructurado, peer bootstrap para inicio de sistema p2p. Se plantea la arquitectura cliente/servidor y orientado a microservicios, bibliotecas de red, logica concurrencia, interfaz por consola, descarga y subida de archivos y localización de recursos.



# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
- En este caso decidí usar Python y Go, para la parte del cliente y servidor y microservicios respectivamente. Ya que permiten gran modularidad y escalidad en sistema distribuidos. 

En el modulo de servidor, estan los microservicios de lista y obtención de archivos, mediante api rest. Tambien las conexiones pertinentes para satisfacer mi sistema mediante gRPC. La cual ese para el manejo y gestiones de conexiones en la red.

En el modulo de cliente, estan la parte de la interfaz grafica y de como se gestionan las conexiones, las cuales llamo handhsake, para validar y tener seguimiento de las conexiones mediante un monitor de estados. Con esto manejo las lista de peers conectados a la red, y de cada peer..





## como se compila y ejecuta. 
-
## detalles del desarrollo.

La arquitectura se basa en los servicios específicos que ofrecerá cada componente del sistema, incluyendo los endpoints REST, las llamadas gRPC para el manejo y gestiones de conexiones, desconexiones y estados entre los peers, y cómo se integrará el MOM para la comunicación asincrónica.


## detalles técnicos
 

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
El proyecto se divide por carpetas con nombre descriptivos para entender y maneja correctamente la escalibidalida y modularidad del mismo
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS 
![image](https://github.com/sgalle16/sgalle16-st0263/assets/14111169/4bac98ab-ff16-4e82-9611-91b3cb4b945b)



# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Python:
- Lenguaje versátil y popular: Amplia comunidad y ecosistema de frameworks.
- Ideal para la capa de aplicación: Desarrollo del cliente, interfaz de usuario, lógica de negocio.
- Bibliotecas/librerias:Python version 3.8.10
Librerias
grpcio==1.62.0
grpcio-tools==1.62.0
protobuf==4.25.3


Go:
- Lenguaje moderno y eficiente: Concurrencia y rendimiento para redes exigentes.
- Ideal para la capa de red: Implementación de protocolos, gestión de conexiones, enrutamiento.
- Bibliotecas/librerias:
Go version=1.22.0
Librerias:
grpc⋅v1.62.0
protobuf⋅v1.32.0

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación
Se inicia el sistema y el peer iniciante intenta conectarse con los boostraps peer(bs), este peer siempre para iniciar y conectarse. Una vez conectado este le envia la lista de peers conocidos, y la lista de recursos. Dado el caso, el peer iniciante no logra conectarse con ningun bootstrap, este iniciaria como bootstrap(servidor). Y actuaria como tal, para recibir conexiones y llamadas de los peers entrante. 
Para esto el usuario ejecutaria el sistema, corriendo cualquiera de los bootstrap peer especificando su puerto e iniciando el client

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
https://faun.pub/4-types-of-grpc-communication-in-golang-c395df1f3cff
https://grpc.io/
https://github.com/anthdm/godistricas
