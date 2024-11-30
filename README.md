# TP Base de Datos - Cátedra Merlino. Bases de Datos Relacionales y NoSQL
# ¿Cómo levantar el proyecto?
Desde Windows
  - Instalar MongoDB como servicio. Enlace al instalador oficial: https://www.mongodb.com/try/download/community
  - Iniciar ejecución del servicio (si no está en ejecución):
    * Buscar el servicio en la lista de Servicios e iniciarlo
    * Desde CMD/Powershell (como administrador):
      ```
      > net start MongoDB
      ```
   
  - Abrir CMD/Powershell desde el directorio con el proyecto
    * Crear directorio que va a usar MongoDB:
      ```
      > mkdir mongodb-data
      ```
    * Establecer conexión con MongoDB:
      ```
      > mongod --dbpath mongodb-data
      ```
    * Esta terminal permanece en ejecución
   
  - Abrir una segunda terminal CMD/Powershell desde el directorio con el proyecto
    * Levantar el proyecto:
      ```
      > python manage.py runserver
      ```
    * Acceder al proyecto para interactuar con el mismo: http://127.0.0.1:8000/
