# Usa la imagen base de Ubuntu 22.04
FROM ubuntu:22.04

# Copia el script SQL a la imagen
COPY init.sql /init.sql

# Actualiza los repositorios e instala Python 3.10, libzbar0 y MariaDB Server
RUN apt-get update && apt-get install -y \
    python3.10 

RUN apt-get install python3.10-venv -y

RUN apt-get install mariadb-server -y

RUN apt-get install python3-pip -y

RUN apt-get install libzbar0 -y


# Establece python3.10 como el intérprete por defecto
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Inicia el servicio de MariaDB al arrancar el contenedor
RUN service mariadb start && \
    mariadb -u root < /init.sql

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar la aplicación
COPY app/ .

# Copia los archivos necesarios a la imagen de Docker
COPY requirements.txt .  
COPY app/app.py .

# Crea y activa un entorno virtual
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instalar pip
RUN python -m ensurepip

# Actualizar pip a la última versión
RUN pip install --no-cache-dir --upgrade pip

RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Instala las dependencias de tu aplicación
RUN pip install -r requirements.txt  # Si tienes un archivo requirements.txt

# Expone el puerto en el que tu aplicación Flask está ejecutándose
EXPOSE 5000  

# Copia el script de inicio al contenedor
COPY start_services.sh /start_services.sh

# Otorga permisos de ejecución al script
RUN chmod +x /start_services.sh

# Comando por defecto al ejecutar el contenedor
CMD ["/bin/bash", "/start_services.sh"]